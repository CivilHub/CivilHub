# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from places_core.mixins import LoginRequiredMixin
from .models import Discussion, Entry
from .forms import DiscussionForm, ReplyForm


class DiscussionDetailView(DetailView):
    """
    Single discussion page as forum page.
    """
    model = Discussion

    def get_context_data(self, **kwargs):
        topic = super(DiscussionDetailView, self).get_object()
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        replies = Entry.objects.filter(discussion=topic)
        paginator = Paginator(replies, 25)
        page = self.request.GET.get('page')
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
        context['title'] = obj.question
        context['subtitle'] = _('Edit this topic')
        return context


@login_required
@require_http_methods(["POST"])
def delete_topic(request, slug):
    """
    Delete topic from list via AJAX request.
    """
    topic = get_object_or_404(Discussion, slug=slug)
    if request.user != topic.creator and not request.user.is_superuser:
        resp = {
            'success': False,
            'message': _('Permission required'),
            'level': 'danger',
        }
    else:
        resp = {
            'success': True,
            'message': _('Entry deleted'),
            'level': 'success',
        }
        topic.delete()
    return HttpResponse(json.dumps(resp))


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
        except:
            return HttpResponse(_('An error occured'))
    return HttpResponseRedirect(reverse('discussion:details',
                                kwargs={'slug': topic.slug,}))
