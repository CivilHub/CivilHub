from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
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
