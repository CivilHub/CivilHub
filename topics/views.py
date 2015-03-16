# -*- coding: utf-8 -*-
import json, datetime
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from actstream import action
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from places_core.helpers import SimplePaginator, truncatehtml, truncatesmart
from maps.models import MapPointer
from locations.mixins import LocationContextMixin, SearchableListMixin
from locations.models import Location
from locations.links import LINKS_MAP as links
from .models import Discussion, Entry, EntryVote, Category
from .forms import DiscussionForm, ReplyForm, ConfirmDeleteForm


class TopicsContextMixin(LocationContextMixin):
    """ """
    def get_context_data(self):
        context = super(TopicsContextMixin, self).get_context_data()
        context['links'] = links['discussions']
        return context


class DiscussionListView(TopicsContextMixin, SearchableListMixin):
    """ """
    model = Discussion
    paginate_by = 25

    def get_queryset(self):
        qs = super(DiscussionListView, self).get_queryset()
        return qs.filter(question__icontains=self.request.GET.get('haystack', ''))

    def get_context_data(self):
        context = super(DiscussionListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context


class DiscussionDetailView(DetailView):
    """ Single discussion page as forum page. """
    model = Discussion

    def get_context_data(self, **kwargs):
        from maps.forms import AjaxPointerForm
        topic = super(DiscussionDetailView, self).get_object()
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        replies = Entry.objects.filter(discussion=topic)
        paginator = Paginator(replies, settings.PAGE_PAGINATION_LIMIT)
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
    """ Allow owner user to update and change their discussions. """
    model = Discussion
    form_class = DiscussionForm
    template_name = 'locations/location_forum_create.html'

    def get_context_data(self, **kwargs):
        obj = super(DiscussionUpdateView, self).get_object()
        context = super(DiscussionUpdateView, self).get_context_data(**kwargs)
        moderator = is_moderator(self.request.user, obj.location)
        if self.request.user != obj.creator and not moderator:
            raise PermissionDenied
        context['title'] = obj.question
        context['subtitle'] = _('Edit this topic')
        context['location'] = obj.location
        context['links'] = links['discussions']
        context['is_moderator'] = moderator
        return context


class DeleteDiscussionView(LoginRequiredMixin, View):
    """ Delete single discussion in 'classic' way. """
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
    """ Update entry in static form. """
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
    """ Delete topic from discussion list via AJAX request. """
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
    """ Create forum reply. """
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
        
        entry.save()
        action.send(
            request.user,
            action_object=entry,
            target = topic,
            verb= _('posted')
        )
        
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
