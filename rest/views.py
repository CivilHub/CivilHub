# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.utils.html import escape
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import authentication, viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest.serializers import *
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import link, api_view, renderer_classes
from rest_framework.pagination import PaginationSerializer
from locations.models import Location
from taggit.models import Tag
from blog.models import News
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from ideas.models import Vote as IdeaVote
from comments.models import CustomComment, CommentVote
from topics.models import Category as ForumCategory
from topics.models import Discussion
from userspace.models import Badge, UserProfile
from gallery.models import LocationGalleryItem
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from places_core.models import AbuseReport
from places_core.mixins import AtomicFreeTransactionMixin
from actstream import action


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    News viewset - API endpoint for news Backbone application.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    paginate_by = 2
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        order = '-date_created'
        if self.request.GET.get('pk'):
            pk = self.request.GET.get('pk')
            location = get_object_or_404(Location, pk=pk)
            newset = News.objects.filter(location=location)
        else:
            newset = super(NewsViewSet, self).get_queryset()
        if self.request.GET.get('order'):
            order = self.request.GET.get('order')
        if self.request.GET.get('keywords'):
            keywords = self.request.GET.get('keywords')
            newset = newset.filter(title__icontains=keywords)
        return newset.order_by(order)

    def pre_save(self, obj):
        obj.creator = self.request.user


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Intended to use with comment tree related to selected item
    """
    queryset = CustomComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def set_element_order(self):
        if self.request.GET.get('order'):
            return self.request.GET.get('order')
        return 'submit_date'

    def get_queryset(self):
        if self.request.GET:
            order = self.set_element_order()
            content_label = self.request.GET['content-label']
            content_type = ContentType.objects.get(pk=self.request.GET['content-type'])
            content_id = int(self.request.GET['content-id'])
            total_comments = CustomComment.objects.filter(content_type=content_type)
            total_comments = total_comments.filter(object_pk=content_id)
            total_comments = total_comments.filter(parent__isnull=True)
            return total_comments.order_by(order)
        else:
            queryset = super(CommentsViewSet, self).get_queryset()

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


class IdeaCategoryViewSet(viewsets.ModelViewSet):
    """
    Allow superusers to create new forum categories dynamically.
    """
    queryset = IdeaCategory.objects.all()
    serializer_class = IdeaCategorySerializer
    permission_classes = (permissions.IsAdminUser,)


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

    def delete(self, request):
        itm = get_object_or_404(LocationGalleryItem, pk=request.DATA.get('pk'))
        itm.delete()
        return Response({
            'success': True,
            'level'  : 'success',
            'message': _("Item deleted"),
        })
