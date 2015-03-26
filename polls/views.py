# -*- coding: utf-8 -*-
import json, datetime
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
from django.views.generic import View, DetailView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from maps.models import MapPointer
from userspace.models import UserProfile
from locations.models import Location
from locations.links import LINKS_MAP as links
from places_core.helpers import SimplePaginator, truncatehtml
from .models import Poll, Answer, AnswerSet
from .forms import PollEntryAnswerForm


from locations.mixins import LocationContextMixin, SearchableListMixin


class PollsContextMixin(LocationContextMixin):
    """ """
    def get_context_data(self, form=None, object=None):
        context = super(PollsContextMixin, self).get_context_data()
        context['links'] = links['polls']
        if form is not None:
            context['form'] = form
        return context


class PollListView(PollsContextMixin, SearchableListMixin):
    """ """
    model = Poll
    paginate_by = 25

    def get_queryset(self):
        qs = super(PollListView, self).get_queryset()
        return qs.filter(title__icontains=self.request.GET.get('haystack', ''))


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
        context['links'] = links['polls']
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(Poll)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(Poll),
                'object_pk'   : self.object.pk,
            })
        context['can_vote'] = True
        try:
            chk = AnswerSet.objects.filter(user=self.request.user).filter(poll=self.object)
            if len(chk) > 0:
                context['can_vote'] = False
        except:
            context['can_vote'] = False
        return context


class PollResults(DetailView):
    """
    Detailed poll view modified exclusively to show poll answers.
    """
    model = Poll
    template_name = 'polls/poll-results.html'

    def calculate_answsers(self, **kwargs):
        """
        Count the votes of respective anwsers.
        """
        result = []
        obj = self.object
        asets = AnswerSet.objects.filter(poll=obj)
        for a in obj.answer_set.all():
            counter = 0
            answer = a.answer
            for aset in asets:
                if aset.answers.filter(pk=a.pk).exists():
                    counter += 1
            result.append({
                'answer': answer,
                'counter': counter,
            })
        return result

    def get_context_data(self, **kwargs):
        context = super(PollResults, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        context['location'] = self.object.location
        context['answers'] = AnswerSet.objects.filter(poll=self.object)[:10]
        context['answer_set'] = self.calculate_answsers()
        context['links'] = links['polls']
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
    prof = UserProfile.objects.get(user=user)
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
        prof.rank_pts += 1
        prof.save()

    return redirect(reverse('polls:results', kwargs={'pk': poll.pk}))


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
