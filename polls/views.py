# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Poll, AnswerSet
from .forms import PollEntryAnswerForm


class PollDetails(DetailView):
    """
    Detailed poll view.
    """
    model = Poll
    template_name = 'polls/poll-details.html'

    def get_context_data(self, **kwargs):
        context = super(PollDetails, self).get_context_data(**kwargs)
        context['location'] = self.object.location
        context['title'] = self.object.title
        context['form'] = PollEntryAnswerForm(self.object)
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
    for key, val in request.POST.iteritems():
        if 'answer_' in key:
            answers.append(key[7:])
        elif 'answers' in key:
            answers.append(val)
    aset = AnswerSet(
        poll = poll,
        user = user,
        answers = ",".join(answers)
    )
    aset.save()
    return redirect('locations:results', slug=poll.location.slug, pk=poll.pk)


@login_required
@require_http_methods(["POST"])
def delete_poll(request, pk):
    """
    Delete poll from list via AJAX request - only owner or superadmin.
    TODO: get_object_or_404 tutaj nie pasuje, bo wtedy json nie ma jak
    wyrzucić odpowiedzi zgłaszającej błąd. Lepszy będzie try/except.
    """
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.creator and not request.user.is_superuser:
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
        poll.delete()
    return HttpResponse(json.dumps(resp))
