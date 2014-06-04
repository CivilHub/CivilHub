# -*- coding: utf-8 -*-
import json
from django.db import transaction
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from maps.models import MapPointer
from .models import Poll, Answer, AnswerSet
from .forms import PollEntryAnswerForm


class PollDetails(DetailView):
    """
    Detailed poll view.
    """
    model = Poll
    template_name = 'polls/poll-details.html'

    def get_context_data(self, **kwargs):
        from maps.forms import AjaxPointerForm
        context = super(PollDetails, self).get_context_data(**kwargs)
        context['location'] = self.object.location
        context['title'] = self.object.title
        context['form'] = PollEntryAnswerForm(self.object)
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(Poll)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(Poll),
                'object_pk'   : self.object.pk,
            })
        context['can_vote'] = True
        chk = AnswerSet.objects.filter(user=self.request.user).filter(poll=self.object)
        if len(chk) > 0:
            context['can_vote'] = False
        return context


class PollResults(DetailView):
    """
    Detailed poll view modified exclusively to show poll answers.
    """
    model = Poll
    template_name = 'polls/poll-results.html'

    def get_context_data(self, **kwargs):
        context = super(PollResults, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        context['location'] = self.object.location
        context['answers'] = AnswerSet.objects.filter(poll=self.object)
        return context


@login_required
@require_http_methods(["POST"])
def save_answers(request, pk):
    """
    Save user's answers.
    """
    answers = []
    poll = get_object_or_404(Poll, pk=request.POST.get('poll'))
    user = request.user
    chk = AnswerSet.objects.filter(user=user).filter(poll=poll)
    if len(chk) > 0:
        messages.add_message(request, messages.ERROR, _('You already voted on this poll.'))
    else:
        aset = AnswerSet(
            poll = poll,
            user = user
        )
        aset.save()
        for key, val in request.POST.iteritems():
            if 'answer_' in key:
                aset.answers.add(Answer.objects.get(pk=int(key[7:])))
            elif 'answers' in key:
                aset.answers.add(Answer.objects.get(pk=int(val)))
        aset.save()

    return redirect('locations:results', slug=poll.location.slug, pk=poll.pk)


@login_required
@require_http_methods(["POST"])
@transaction.non_atomic_requests
@transaction.autocommit
def delete_poll(request, pk):
    """
    Delete poll from list via AJAX request - only owner or superadmin.
    Fixme: "This is forbidden when an 'atomic' block is active" error.
    """
    try:
        poll = Poll.objects.get(pk=pk)
    except Poll.DoesNotExist as ex:
        resp = {
            'success': False,
            'message': str(ex),
            'level': 'danger',
        }
        return HttpResponse(json.dumps(resp))

    if request.user != poll.creator and not request.user.is_superuser:
        resp = {
            'success': False,
            'message': _('Permission required'),
            'level': 'danger',
        }
    else:
        try:
            with transaction.commit_on_success(): poll.delete()
            resp = {
                'success': True,
                'message': _('Entry deleted'),
                'level': 'success',
            }
        except Exception as ex:
            resp = {
                'success': False,
                'message': str(ex),
                'level': 'danger',
            }
    return HttpResponse(json.dumps(resp))
