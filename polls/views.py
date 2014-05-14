# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, ProcessFormView
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from places_core.mixins import LoginRequiredMixin
from locations.models import Location
from .models import Category, Poll, Question, Answer
from .forms import CategoryForm, PollEntryAnswerForm


class CreateCategoryView(LoginRequiredMixin, CreateView):
    """
    Create new category for polls.
    """
    model = Category
    template_name = 'polls/category-create.html'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super(CreateCategoryView, self).get_context_data(**kwargs)
        context['title'] = _('Create poll category')
        return context

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        return reverse('polls:categories')


class CategoryList(ListView):
    """
    List all polls categories on one page to have some redirect for browser
    that don't support AJAX or Javascript.
    """
    model = Category
    template_name = 'polls/category-list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['title'] = _('Poll categories')
        return context


class PollDetails(DetailView):
    """
    Detailed poll view - get participated.
    """
    model = Poll
    template_name = 'polls/poll-details.html'

    def get_context_data(self, **kwargs):
        context = super(PollDetails, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        context['location'] = self.object.location
        context['form'] = PollEntryAnswerForm(self.object.question_set.all())
        return context


class PollAnswerSet(ProcessFormView):
    """
    Get answers from user and check if their are correct.
    """
    def post(self, request, *args, **kwargs):
        valid_answers = []
        invalid_answers = []
        current_poll = None
        for key, val in request.POST.iteritems():
            if 'question' in key:
                qid = key[9:]
                if current_poll == None:
                    question     = Question.objects.get(pk=qid)
                    current_poll = question.poll
                answer = Answer.objects.get(pk=val)
                if answer.correct:
                    valid_answers.append(answer)
                else:
                    invalid_answers.append(answer)
        title = _('Poll results')
        return render(request, 'polls/poll-results.html', {
            'valid'   : valid_answers,
            'invalid' : invalid_answers,
            'title'   : title,
            'location': current_poll.location,
        })


@login_required
@require_http_methods(["POST"])
def verify_poll(request):
    """
    Custom method to create poll via POST data - allow us to add as many
    question fields as we want (at least I hope so).
    """
    questions = {}
    title = request.POST.get('title')
    tags  = request.POST.get('tags')
    category = Category.objects.get(pk=request.POST.get('category'))
    location = Location.objects.get(pk=request.POST.get('location'))
    description = request.POST.get('description')
    # Create new poll without questions (for now)
    poll = Poll(
        title = title,
        description = description,
        category    = category,
        creator     = request.user,
        location    = location
    )
    poll.save()
    # Add questions and answers in proper order
    for key, val in request.POST.iteritems():
        if 'question' in key:
            qid = key[9:]
            multi = request.POST.get('multiple_' + str(qid))
            q = Question(
                poll = poll,
                question = request.POST.get('question_' + str(qid)),
                multiple = True if multi else False
            )
            q.save()
            # Fixme: znaleźć bardziej wydajną metodę
            for key, val in request.POST.iteritems():
                if 'answer_parent' in key and val == qid:
                    aid = key[14:]
                    chk = request.POST.get('is_correct_' + str(aid))
                    a = Answer(
                        question = q,
                        answer   = request.POST.get('answer_txt_' + str(aid)),
                        correct  = True if chk else False
                    )
                    a.save()
    return redirect(reverse('locations:polls', kwargs={'slug': location.slug}))


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
