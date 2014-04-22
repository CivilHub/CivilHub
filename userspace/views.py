from django.shortcuts import render

def index(request):
    return render(request, 'userspace/base.html', {'title': 'Test'})
