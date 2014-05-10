from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from places_core.mixins import LoginRequiredMixin
from .models import Discussion


def index_view(self):
    """
    Dummy view to avoid warnings during urls.py include.
    """
    return HttpResponse('This is forum index page')


class DiscussionDetailView(DetailView):
    """
    Single discussion page as forum page.
    """
    model = Discussion

    def get_context_data(self, **kwargs):
        topic = super(DiscussionDetailView, self).get_object()
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        context['title'] = topic.question
        return context
