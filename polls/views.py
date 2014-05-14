# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from places_core.mixins import LoginRequiredMixin
from .models import Category, Poll
from .forms import CategoryForm


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
        return context


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
