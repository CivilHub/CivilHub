# -*- coding: utf-8 -*-
import json, datetime
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from actstream import action
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from places_core.helpers import SimplePaginator, truncatehtml, truncatesmart
from maps.models import MapPointer
from locations.models import Location
from locations.links import LINKS_MAP as links
from .models import Discussion, Entry, EntryVote, Category
from .forms import DiscussionForm, ReplyForm, ConfirmDeleteForm

# REST API
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from serializers import ForumCategorySimpleSerializer, ForumTopicSimpleSerializer, ForumEntrySimpleSerializer


class ForumTopicAPIViewSet(viewsets.ModelViewSet):
    """
    This is simplified discussion view set for mobile app.
    """
    queryset = Discussion.objects.all()
    serializer_class = ForumTopicSimpleSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.creator = self.request.user


class BasicDiscussionSerializer(object):
    """
    This is simple serializer to convert Discussion object instances into
    JSON format.
    """
    data = {}

    def __init__(self, obj):
        tags = []

        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':obj.location.slug,
                                       'tag':tag.name})
            })

        self.data = {
            'id'           : obj.pk,
            'question'     : truncatesmart(obj.question, 28),
            'intro'        : truncatehtml(obj.intro, 240),
            'url'          : obj.get_absolute_url(),
            'date_created' : timesince(obj.date_created),
            'creator'      : obj.creator.get_full_name(),
            'creator_id'   : obj.creator.pk,
            'creator_url'  : obj.creator.get_absolute_url(),
            'avatar'       : obj.creator.profile.thumbnail.url,
            'status'       : obj.status,
            'category_id'  : obj.category.pk,
            'category_name': obj.category.name,
            'answers'      : obj.entry_set.count(),
            'tags'         : tags,
        }

        if obj.category:
            self.data['category']     = obj.category.name
            self.data['category_url'] = reverse('locations:category_search',
                kwargs={
                    'slug'    : obj.location.slug,
                    'app'     : 'topics',
                    'model'   : 'discussion',
                    'category': obj.category.pk,
                })
        else:
            self.data['category'] = ''
            self.data['category_url'] = ''


class DiscussionListView(View):
    """
    Basic view for discussions REST api.
    """
    def get_queryset(self, request, queryset):
        order    = request.GET.get('order')
        time     = request.GET.get('time')
        status   = request.GET.get('state')
        category = request.GET.get('category')
        haystack = request.GET.get('haystack')

        if category and category != 'all':
            category = Category.objects.get(pk=request.GET.get('category'))
            queryset = queryset.filter(category=category)

        time_delta = None

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

        if haystack and haystack != 'false':
            queryset = queryset.filter(question__icontains=haystack)

        if status == 'False':
            queryset = queryset.filter(status=False)
        elif status == 'True':
            queryset = queryset.filter(status=True)
        
        if order == 'question':
            return queryset.order_by('question')
        elif order == 'latest':
            return queryset.order_by('-date_created')
        elif order == 'oldest':
            return queryset.order_by('date_created')
        elif order == 'category':
            return queryset.order_by('category__name')
        elif order == 'username':
            l = list(queryset);
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l

        return queryset.order_by('-date_created')

    def get(self, request, slug=None):
        if slug:
            location = Location.objects.get(slug=slug)
            topics = Discussion.objects.filter(location=location)
        else:
            topics = Discussion.objects.all()
        context = {'results': []}
        topics = self.get_queryset(request, topics)
        for topic in topics:
            context['results'].append(BasicDiscussionSerializer(topic).data)
        paginator = SimplePaginator(context['results'], 50)
        if request.GET.get('page'):
            page = request.GET.get('page')
        else:
            page = 1
        context['results'] = paginator.page(page)
        context['current_page'] = page
        context['total_pages'] = paginator.count()
        return HttpResponse(json.dumps(context))


class DiscussionDetailView(DetailView):
    """
    Single discussion page as forum page.
    """
    model = Discussion

    def get_context_data(self, **kwargs):
        from maps.forms import AjaxPointerForm
        topic = super(DiscussionDetailView, self).get_object()
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        replies = Entry.objects.filter(discussion=topic)
        paginator = Paginator(replies, 2)
        page = self.request.GET.get('page')
        moderator = is_moderator(self.request.user, topic.location)
        try:
            context['replies'] = paginator.page(page)
        except PageNotAnInteger:
            context['replies'] = paginator.page(1)
        except EmptyPage:
            context['replies'] = paginator.page(paginator.num_pages)
        context['form'] = ReplyForm(initial={
            'discussion': topic.slug
        })
        context['title'] = topic.question
        context['location'] = topic.location
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(self.object)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator or moderator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(Discussion),
                'object_pk'   : self.object.pk,
            })
        context['is_moderator'] = moderator
        context['links'] = links['discussions']
        context['content_type'] = ContentType.objects.get_for_model(Discussion).pk
        context['ct'] = ContentType.objects.get_for_model(Entry).pk
        return context


class DiscussionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allow owner user to update and change their discussions.
    """
    model = Discussion
    form_class = DiscussionForm

    def get_context_data(self, **kwargs):
        obj = super(DiscussionUpdateView, self).get_object()
        context = super(DiscussionUpdateView, self).get_context_data(**kwargs)
        moderator = is_moderator(self.request.user, obj.location)
        if self.request.user != obj.creator and not moderator:
            raise PermissionDenied
        context['title'] = obj.question
        context['subtitle'] = _('Edit this topic')
        context['location'] = obj.location
        context['is_moderator'] = moderator
        return context


class DeleteDiscussionView(LoginRequiredMixin, View):
    """
    Delete single discussion in 'classic' way.
    """
    template_name = 'topics/delete.html'

    def get(self, request, pk):
        discussion = get_object_or_404(Discussion, pk=pk)
        ctx = {
            'form' : ConfirmDeleteForm(initial={'confirm':True}),
            'title': _("Delete discussion"),
            'location': discussion.location,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        discussion = get_object_or_404(Discussion, pk=pk)
        try:
            with transaction.commit_on_success(): discussion.delete()
            ctx = {
                'title': _("Entry deleted"),
                'location': discussion.location,
            }
            return redirect(reverse('locations:discussions', kwargs={
                'slug': discussion.location.slug
            }))
        except Exception as ex:
            ctx = {
                'title': _("Error"),
                'error': str(ex),
                'location': discussion.location,
            }
            return render(request, 'topics/delete-confirm.html', ctx)


class EntryUpdateView(LoginRequiredMixin, View):
    """
    Update entry in static form.
    """
    def post(self, request, slug, pk):
        entry = get_object_or_404(Entry, pk=pk)
        entry.content = request.POST.get('content')
        entry.save()
        return redirect(request.META['HTTP_REFERER'] + '#reply-' + str(entry.pk))


@login_required
@require_POST
@transaction.non_atomic_requests
@transaction.autocommit
def delete_topic(request):
    """
    Delete topic from discussion list via AJAX request.
    """
    pk = request.POST.get('object_pk')

    if not pk:
        return HttpResponse(json.dumps({
            'success': False,
            'message': _("No entry ID provided"),
            'level': 'danger',
        }))

    try:
        topic = Discussion.objects.get(pk=pk)
    except Discussion.DoesNotExist as ex:
        return HttpResponse(json.dumps({
            'success': False,
            'message': str(ex),
            'level': 'danger',
        }))

    moderator = is_moderator(request.user, topic.location)
    if request.user != topic.creator and not moderator:
        return HttpResponse(json.dumps({
            'success': False,
            'message': _("Permission required!"),
            'level': 'danger',
        }))

    try:
        with transaction.commit_on_success(): topic.delete()
        return HttpResponse(json.dumps({
            'success': True,
            'message': _("Entry deleted"),
            'level': 'success',
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            'success': False,
            'message': str(ex),
            'level': 'danger',
        }))


def reply(request, slug):
    """
    Create forum reply.
    """
    if request.method == 'POST' and request.POST:
        post = request.POST
        topic = Discussion.objects.get(slug=post['discussion'])
        if not topic.status:
            return HttpResponse(_('This discussion is closed.'))
        entry = Entry(
            content = post['content'],
            creator = request.user,
            discussion = topic,
        )
        try:
            entry.save()
            action.send(
                request.user,
                action_object=entry,
                target = topic,
                verb= _('posted')
            )
        except:
            return HttpResponse(_('An error occured'))
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'] + '#reply-' + str(entry.pk))


@login_required
@require_POST
@transaction.non_atomic_requests
@transaction.autocommit
def vote(request, pk):
    """ Vote for reply. """
    entry = Entry.objects.get(pk=pk)
    vote  = False if request.POST.get('vote') == 'false' else True
    user  = request.user
    check = EntryVote.objects.filter(entry=entry).filter(user=user)
    if not len(check):
        entry_vote = EntryVote.objects.create(
            entry = entry,
            user  = user,
            vote  = vote)
        try:
            entry_vote.save()
            context = {
                'success': True,
                'message': _("Vote saved"),
                'votes'  : Entry.objects.get(pk=pk).calculate_votes(),
                'level'  : "success",
            }
        except Exception as ex:
            context = {
                'success': False,
                'message': str(ex),
                'level'  : "danger",
            }
    else:
        context = {
            'success': False,
            'message': _("You already voted on this entry."),
            'level'  : "warning",
        }
    return HttpResponse(json.dumps(context))
