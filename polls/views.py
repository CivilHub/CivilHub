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


class BasicPollSerializer(object):
    """
    Serialize object instance into JSON format. It takes Poll object instance
    as mandatory argument for __init__ function.
    """
    data = {}

    def __init__(self, obj):
        tags = []

        #~ for tag in obj.tags.all():
            #~ tags.append({
                #~ 'name': tag.name,
                #~ 'url': reverse('locations:tag_search',
                               #~ kwargs={'slug':obj.location.slug,
                                       #~ 'tag':tag.name})
            #~ })

        self.data = {
            'id'            : obj.pk,
            'title'         : obj.title,
            'slug'          : obj.slug,
            'url'           : obj.get_absolute_url(),
            'question'      : truncatehtml(obj.question, 240),
            'username'      : obj.creator.username,
            'user_full_name': obj.creator.get_full_name(),
            'creator_url'   : obj.creator.profile.get_absolute_url(),
            'user_id'       : obj.creator.pk,
            'avatar'        : obj.creator.profile.avatar.url,
            'date_created'  : timesince(obj.date_created),
            #'tags'          : tags,
        }

        self.data['answers_url'] = reverse('polls:results',
                                            kwargs={'pk': obj.pk})

        try:
            self.data['date_edited'] = timesince(obj.date_edited)
        except Exception:
            self.data['date_edited'] = ''


class BasicPollView(View):
    """
    Basic view for our JSON api.
    """
    def get_queryset(self, request, queryset):
        order = request.GET.get('order')
        time  = request.GET.get('time')
        haystack = request.GET.get('haystack')

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
            queryset = queryset.filter(title__icontains=haystack)
        
        if order == 'title':
            return queryset.order_by('title')
        elif order == 'latest':
            return queryset.order_by('-date_created')
        elif order == 'oldest':
            return queryset.order_by('date_created')
        elif order == 'username':
            l = list(queryset);
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l

        return queryset.order_by('-date_created')

    def get(self, request, slug=None, pk=None, *args, **kwargs):

        ctx = {'results': []}

        if not pk:
            if not slug:
                polls = Poll.objects.all()
            else:
                location = Location.objects.get(slug=slug)
                polls = Poll.objects.filter(location=location)

            polls = self.get_queryset(request, polls)

            for poll in polls:
                ctx['results'].append(BasicPollSerializer(poll).data)

            paginator = SimplePaginator(ctx['results'], 50)
            page = request.GET.get('page') if request.GET.get('page') else 1
            ctx['current_page'] = page
            ctx['total_pages'] = paginator.count()
            ctx['results'] = paginator.page(page)
        else:
            news = get_object_or_404(Poll, pk=pk)
            ctx['results'] = BasicPollSerializer(news).data
            ctx['current_page'] = 1
            ctx['total_pages'] = 1

        return HttpResponse(json.dumps(ctx))


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

    def calculate_answsers(self, **kwargs):
        """
        Policz głosy za poszczególnymi odpowiedziami.
        """
        result = []
        obj = self.object
        asets = AnswerSet.objects.filter(poll=obj)
        for a in obj.answer_set.all():
            counter = 0
            answer = a.answer
            for aset in asets:
                if a in aset.answers.all():
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
