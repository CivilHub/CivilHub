# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta
from django.http import Http404
from django.utils import timezone
from django.utils.html import escape
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import authentication, viewsets, permissions, renderers
from rest_framework import views as rest_views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest.serializers import *
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import link, api_view, renderer_classes
from rest_framework.pagination import PaginationSerializer
from locations.models import Location
from taggit.models import Tag
from blog.models import News, Category
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from ideas.models import Vote as IdeaVote
from comments.models import CustomComment, CommentVote
from topics.models import Category as ForumCategory
from topics.models import Discussion, Entry
from userspace.models import Badge, UserProfile
from gallery.models import LocationGalleryItem, UserGalleryItem
from polls.models import Poll
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from places_core.models import AbuseReport
from places_core.mixins import AtomicFreeTransactionMixin
from places_core.helpers import sort_by_locale
from actstream import action


class UserActionsRestViewSet(viewsets.ViewSet):
    """
    This class uses rest framework serializer to send data related to user
    profile (static view enabled as 'profile' page).
    """
    serializer_class = MyActionsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    
    def get_queryset(self, pk=None, ct=None):
        from userspace.helpers import UserActionStream
        if self.request.user.is_anonymous(): return None
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = self.request.user
        if not ct:
            return UserActionStream(user).get_actions()
        elif ct == 'idea':
            return UserActionStream(user).get_actions('ideas.idea')
        elif ct == 'news':
            return UserActionStream(user).get_actions('blog.news')
        elif ct == 'poll':
            return UserActionStream(user).get_actions('polls.poll')
        elif ct == 'discussion':
            return UserActionStream(user).get_actions('topics.discussion')
        elif ct == 'gallery':
            return UserActionStream(user).get_actions('gallery.locationgalleryitem')
        
    def list(self, request):
        pk = request.QUERY_PARAMS.get('pk') or None
        ct = request.QUERY_PARAMS.get('content') or None        
        queryset = self.get_queryset(pk, ct)
        
        if request.user.is_anonymous():
            raise Http404()
        
        page = request.QUERY_PARAMS.get('page')
        paginator = Paginator(queryset, settings.STREAM_PAGINATOR_LIMIT)
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            actions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            actions = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedActionSerializer(actions,
                                             context=serializer_context)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    paginate_by = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        search = self.request.QUERY_PARAMS.get('term', None)
        if search is None:
            return super(TagViewSet, self).get_queryset()
        return Tag.objects.filter(name__icontains=search)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        username = request.QUERY_PARAMS.get('username')
        if username is None:
            return super(UserViewSet, self).list(request)
        try:
            user = User.objects.get(username=username)
            return redirect('/rest/users/%s/' % user.pk)
        except User.DoesNotExist:
            raise Http404


class CurrentUserViewSet(viewsets.ModelViewSet):
    """
    Przekazanie informacji o aktywnym użytkowniku do zewnętrznej aplikacji.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def list(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = request.user
        serializer = self.serializer_class(user)
        if user.is_anonymous():
            return Response({'test':'TEST'})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    paginate_by = None


class SimpleNewsViewSet(viewsets.ViewSet):
    """
    Widok dla aplikacji mobilnej. Podstawowy serializer dla bloga. Get można
    brać spokojnie z następnego viewsa, tutaj ułatwiamy POST. Nie mam czasu
    dopisywać funkcji zwrotnych.
    """
    serializer_class = NewsSimpleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def list(self, request, *args, **kwargs):
        serializer = NewsSerializer(News.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        news = News.objects.create(
            title = request.DATA.get('title'),
            content = request.DATA.get('content'),
            creator = self.request.user,
            category = Category.objects.get(pk=request.DATA.get('category')),
            location = Location.objects.get(pk=request.DATA.get('location'))
        )
        news.save()
        serializer = NewsSerializer(news)
        return Response(serializer.data)


class NewsViewSet(viewsets.ModelViewSet):
    """
    News viewset - API endpoint for news Backbone application.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    paginate_by = settings.PAGE_PAGINATION_LIMIT
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.QUERY_PARAMS.get('pk'):
            pk = self.request.QUERY_PARAMS.get('pk')
            location = get_object_or_404(Location, pk=pk)
            cached_qs = cache.get(location.slug + '_newset', None)
            if cached_qs is None or not settings.USE_CACHE:
                newset = News.objects \
                    .filter(location__pk__in=location.get_children_id_list())
                newset = newset | News.objects.filter(location=location)
                cache.set(location.slug + '_newset', newset, timeout=None)
            else:
                newset = cached_qs
        else:
            newset = News.objects.all()

        if self.request.QUERY_PARAMS.get('haystack'):
            haystack = self.request.QUERY_PARAMS.get('haystack')
            newset = newset.filter(title__icontains=haystack)

        category_pk = self.request.QUERY_PARAMS.get('category')
        if category_pk and category_pk != 'all':
            category = get_object_or_404(Category, pk=category_pk)
            newset = newset.filter(category=category)

        time_delta = None
        time = self.request.QUERY_PARAMS.get('time')

        if time == 'day':
            time_delta = datetime.date.today() - datetime.timedelta(days=1)
        if time == 'week':
            time_delta = datetime.date.today() - datetime.timedelta(days=7)
        if time == 'month':
            time_delta = datetime.date.today() - relativedelta(months=1)
        if time == 'year':
            time_delta = datetime.date.today() - relativedelta(years=1)

        if time_delta:
            newset = newset.filter(date_created__gte=time_delta)

        sortby = self.request.QUERY_PARAMS.get('sortby')
        if sortby == 'title':
            return sort_by_locale(newset, lambda x: x.title, get_language())
        elif sortby == 'oldest':
            return newset.order_by('date_created')
        elif sortby == 'category':
            return newset.order_by('category__name')
        elif sortby == 'username':
            l = list(newset)
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l

        return newset.order_by('-date_created')

    def pre_save(self, obj):
        obj.creator = self.request.user


class PollListViewSet(viewsets.ModelViewSet):
    """ Vieset to manage entire location's polls list. """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    paginate_by = settings.LIST_PAGINATION_LIMIT
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.QUERY_PARAMS.get('pk'):
            pk = self.request.QUERY_PARAMS.get('pk')
            location = get_object_or_404(Location, pk=pk)
            cached_qs = cache.get(location.slug+'_polls', None)
            if cached_qs is None or not settings.USE_CACHE:
                newset = Poll.objects \
                    .filter(location__pk__in=location.get_children_id_list())
                newset = newset | Poll.objects.filter(location=location)
                cache.set(location.slug+'_polls', newset, timeout=None)
            else:
                newset = cached_qs
        else:
            newset = Poll.objects.all()

        if self.request.QUERY_PARAMS.get('haystack'):
            haystack = self.request.QUERY_PARAMS.get('haystack')
            newset = newset.filter(title__icontains=haystack)

        time_delta = None
        time = self.request.QUERY_PARAMS.get('time')

        if time == 'day':
            time_delta = datetime.date.today() - datetime.timedelta(days=1)
        if time == 'week':
            time_delta = datetime.date.today() - datetime.timedelta(days=7)
        if time == 'month':
            time_delta = datetime.date.today() - relativedelta(months=1)
        if time == 'year':
            time_delta = datetime.date.today() - relativedelta(years=1)

        if time_delta:
            newset = newset.filter(date_created__gte=time_delta)

        sortby = self.request.QUERY_PARAMS.get('sortby')
        if sortby == 'question':
            return sort_by_locale(newset, lambda x: x.question, get_language())
        elif sortby == 'oldest':
            return newset.order_by('date_created')
        elif sortby == 'username':
            l = list(newset)
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l

        return newset.order_by('-date_created')

    def pre_save(self, obj):
        obj.creator = self.request.user


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Intended to use with comment tree related to selected item
    """
    queryset = CustomComment.objects.all()
    paginate_by = settings.COMMENT_PAGINATOR_LIMIT
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def set_element_order(self):
        if self.request.QUERY_PARAMS.get('filter'):
            return self.request.QUERY_PARAMS.get('filter')
        return '-submit_date'

    def get_queryset(self):
        if self.request.GET.get('content-type'):
            order = self.set_element_order()
            content_label = self.request.GET.get('content-label')
            total_comments = CustomComment.objects.filter(
                content_type = ContentType.objects.get(pk=self.request.GET['content-type']),
                object_pk = int(self.request.GET['content-id']),
                parent__isnull = True
            )
            return total_comments.order_by(order)
        else:
            return super(CommentsViewSet, self).get_queryset()

    def partial_update(self, request, pk=None):
        if not pk: return False
        comment = get_object_or_404(CustomComment, pk=pk)
        comment.comment = request.DATA.get('comment')
        comment.submit_date = timezone.now()
        try:
            comment.save()
        except Exception as ex:
            return Response({
                'success': False,
                'message': str(ex),
                'level'  : 'danger',
            })
        return Response({
            'success': True,
            'message': _("Changes saved"),
            'level'  : 'success',
        })

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.site_id = 1
        obj.object_pk = int(self.request.DATA['content_id'])
        obj.submit_date = timezone.now()
        obj.comment = escape(self.request.DATA['comment'])

    @link(renderer_classes=[renderers.JSONRenderer, renderers.JSONPRenderer])
    def replies(self, request, pk):
        replies = CustomComment.objects.filter(parent=pk)
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)


class CommentVoteViewSet(viewsets.ModelViewSet):
    """
    Vote for other user's comments.
    """
    queryset = CommentVote.objects.all()
    serializer_class = CommentVoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def check_valid_vote(self, user, comment):
        chk = CommentVote.objects.filter(user=user, comment=comment)
        return len(chk) <= 0

    def create(self, request):
        if self.check_valid_vote(self.request.user, self.request.POST['comment']):
            vote = CommentVote(vote=True if self.request.POST.get('vote') == 'up' else False,
                               user=self.request.user,
                               date_voted = timezone.now(),
                               comment=CustomComment.objects.get(pk=self.request.POST['comment']))
            vote.save()
            action.send(
                request.user,
                action_object=vote.comment,
                verb= _(u"voted on"),
                vote = True if request.POST.get('vote') == 'up' else False
            )
            return Response({
                'success': True,
                'message': _('Vote saved')
            })
        else:
            return Response({
                'success': False,
                'message': _('Already voted on this comment')
            })

    def pre_save(self, obj):
        obj.user = self.request.user


class ForumCategoryViewSet(viewsets.ModelViewSet):
    """
    Allow superusers to create new forum categories dynamically.
    """
    queryset = ForumCategory.objects.all()
    serializer_class = ForumCategorySerializer
    permission_classes = (permissions.IsAdminUser,)


class ForumViewSet(viewsets.ModelViewSet):
    """ View for location's forum list. """
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    paginate_by = settings.LIST_PAGINATION_LIMIT
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.QUERY_PARAMS.get('pk'):
            pk = self.request.QUERY_PARAMS.get('pk')
            location = get_object_or_404(Location, pk=pk)
            cached_qs = cache.get(location.slug + '_forum', None)
            if cached_qs is None or not settings.USE_CACHE:
                queryset = Discussion.objects \
                    .filter(location__pk__in=location.get_children_id_list())
                queryset = queryset | Discussion.objects.filter(location=location)
                cache.set(location.slug + '_forum', queryset, timeout=None)
            else:
                queryset = cached_qs
        else:
            queryset = Discussion.objects.all()

        if self.request.QUERY_PARAMS.get('haystack'):
            haystack = self.request.QUERY_PARAMS.get('haystack')
            queryset = queryset.filter(question__icontains=haystack)

        category_pk = self.request.QUERY_PARAMS.get('category')
        if category_pk and category_pk != 'all':
            category = get_object_or_404(ForumCategory, pk=category_pk)
            queryset = queryset.filter(category=category)

        status = self.request.QUERY_PARAMS.get('state')
        if status and status != 'all':
            s = True if status == 'True' else False
            queryset = queryset.filter(status=s)

        time_delta = None
        time = self.request.QUERY_PARAMS.get('time')

        if time == 'day':
            time_delta = datetime.date.today() - datetime.timedelta(days=1)
        if time == 'week':
            time_delta = datetime.date.today() - datetime.timedelta(days=7)
        if time == 'month':
            time_delta = datetime.date.today() - relativedelta(months=1)
        if time == 'year':
            time_delta = datetime.date.today() - relativedelta(years=1)

        if time_delta:
            queryset = queryset.filter(date_created__gte=time_delta)

        sortby = self.request.QUERY_PARAMS.get('sortby')
        if sortby == 'question':
            return sort_by_locale(queryset, lambda x: x.question, get_language())
        elif sortby == 'oldest':
            return queryset.order_by('date_created')
        elif sortby == 'category':
            return queryset.order_by('category__name')
        elif sortby == 'username':
            l = list(queryset)
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l

        return queryset.order_by('-date_created')

    def pre_save(self, obj):
        obj.creator = self.request.user


class DiscussionRepliesViewSet(viewsets.ModelViewSet):
    """
    List of replies for discussion.
    """
    queryset = Entry.objects.all()
    serializer_class = DiscussionReplySerializer
    paginate_by = settings.PAGE_PAGINATION_LIMIT
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        topic_pk = self.request.QUERY_PARAMS.get('pk')
        if topic_pk:
            discussion = get_object_or_404(Discussion, pk=topic_pk)
            return Entry.objects.filter(discussion=discussion)
        return Entry.objects.all()


class IdeaCategoryViewSet(viewsets.ModelViewSet):
    """
    Allow superusers to create new forum categories dynamically.
    """
    queryset = IdeaCategory.objects.all()
    serializer_class = IdeaCategorySerializer
    permission_classes = (permissions.IsAdminUser,)


class IdeaListViewSet(viewsets.ModelViewSet):
    """ Idea list viewset. """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    paginate_by = settings.PAGE_PAGINATION_LIMIT
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.QUERY_PARAMS.get('pk'):
            pk = self.request.QUERY_PARAMS.get('pk')
            location = get_object_or_404(Location, pk=pk)
            cached_qs = cache.get(location.slug + '_ideas', None)
            if cached_qs is None or not settings.USE_CACHE:
                queryset = Idea.objects \
                    .filter(location__pk__in=location.get_children_id_list())
                queryset = queryset | Idea.objects.filter(location=location)
                cache.set(location.slug + '_ideas', queryset, timeout=None)
            else:
                queryset = cached_qs
        else:
            queryset = Idea.objects.all()

        if self.request.QUERY_PARAMS.get('haystack'):
            haystack = self.request.QUERY_PARAMS.get('haystack')
            queryset = queryset.filter(name__icontains=haystack)

        category_pk = self.request.QUERY_PARAMS.get('category')
        if category_pk and category_pk != 'all':
            queryset = queryset.filter(category__pk=category_pk)

        status = self.request.QUERY_PARAMS.get('state')
        if status and status != 'all':
            s = True if status == 'True' else False
            queryset = queryset.filter(status=s)

        time_delta = None
        time = self.request.QUERY_PARAMS.get('time')

        if time == 'day':
            time_delta = datetime.date.today() - datetime.timedelta(days=1)
        if time == 'week':
            time_delta = datetime.date.today() - datetime.timedelta(days=7)
        if time == 'month':
            time_delta = datetime.date.today() - relativedelta(months=1)
        if time == 'year':
            time_delta = datetime.date.today() - relativedelta(years=1)

        if time_delta:
            queryset = queryset.filter(date_created__gte=time_delta)

        sortby = self.request.QUERY_PARAMS.get('sortby')
        if sortby == 'title':
            return sort_by_locale(queryset, lambda x: x.name, get_language())
        elif sortby == 'oldest':
            return queryset.order_by('date_created')
        elif sortby == 'category':
            return queryset.order_by('category__name')
        elif sortby == 'username':
            l = list(queryset)
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l
        elif sortby == 'answers':
            l = list(queryset)
            l.sort(key=lambda x: x.get_votes())
            l = l[::-1]
            return l

        return queryset
        #return queryset.order_by('-date_created')

    def pre_save(self, obj):
        obj.creator = self.request.user


class IdeaVoteCounterViewSet(viewsets.ViewSet):
    """
    Get list of users that voted for and against idea.
    """
    queryset = IdeaVote.objects.all()

    def list(self, request):
        if request.GET.get('pk'):
            idea = Idea.objects.get(pk=request.GET.get('pk'))
            queryset = IdeaVote.objects.filter(idea=idea)
        else:
            queryset = IdeaVote.objects.all()
        serializer = IdeaVoteCounterSerializer(queryset, many=True)
        return Response(serializer.data)


class AbuseReportViewSet(viewsets.ModelViewSet):
    """
    Abuse reports to show to admins and moderators. All registered users
    can send reports, but no one except superadmins is allowed to delete
    and edit them.
    """
    queryset = AbuseReport.objects.all()
    serializer_class = AbuseReportSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.sender = self.request.user
        obj.site_id = settings.SITE_ID


class BadgeViewSet(viewsets.ModelViewSet):
    """
    Viewset for user badges.
    """
    queryset = Badge.objects.all()
    serializer_class   = BadgeSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def put(self, request, *args, **kwargs):
        badge_pk = request.DATA.get('id')
        user_pk  = request.DATA.get('user')
        errors   = []

        try:
            badge = Badge.objects.get(pk=badge_pk)
        except Badge.DoesNotExist:
            errors.append(_("Requested badge does not exist"))
        try:
            user = UserProfile.objects.get(user__pk=user_pk)
        except UserProfile.DoesNotExist:
            errors.append(_("Requested user does not exist"))
        try:
            badge.user.add(user)
        except Exception as ex:
            errors.append(str(ex))

        if len(errors) > 0:
            ctx = {
                'success': False,
                'errors' : errors,
                'message': _("Operation failed"),
            }
        else:
            ctx = {
                'success': True,
                'message': _("Badge saved"),
            }
            action.send(
                request.user,
                verb   = _("gave badge to"),
                target = user
            )

        return Response(ctx)


class GalleryViewSet(viewsets.ModelViewSet):
    """ Location gallery item viewset. """
    queryset = LocationGalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        if self.request.QUERY_PARAMS.get('pk'):
            pk = self.request.QUERY_PARAMS.get('pk')
            queryset = LocationGalleryItem.objects.filter(location__pk=pk)
        else:
            queryset = LocationGalleryItem.objects.all()
        return queryset

    def delete(self, request):
        itm = get_object_or_404(LocationGalleryItem, pk=request.DATA.get('pk'))
        itm.delete()
        return Response({
            'success': True,
            'level'  : 'success',
            'message': _("Item deleted"),
        })


class MediaViewSet(viewsets.ModelViewSet):
    """ Handle user media for uploader. """
    queryset = UserGalleryItem.objects.all()
    serializer_class = UserMediaSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = UserGalleryItem.objects.filter(user=request.user)
        serializer = UserMediaSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request):
        itm = UserGalleryItem.objects.get(pk=request.DATA.get('pk'))
        itm.delete()
        return Response({
            'success': True,
            'level'  : 'success',
            'message': _("Item deleted"),
        })

    def pre_save(self, obj):
        obj.user = self.request.user


class LocationBasicViewSet(viewsets.ModelViewSet):
    """
    Viewset dla lokalizacji - listuje podstawowe informacje.
    """
    queryset = Location.objects.all()
    serializer_class = LocationBasicSerializer
    permission_classes = (IsModeratorOrReadOnly,)
