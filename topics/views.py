from django.http import HttpResponse
from django.shortcuts import render

def index_view(self):
    """
    Dummy view to avoid warnings during urls.py include.
    """
    return HttpResponse('This is forum index page')
