from django.shortcuts import render, redirect
from django.contrib import auth

def index(request):
    return render(request, 'userspace/index.html', {'title': 'Test'})

def login(request):
    if request.user.is_authenticated():
        return redirect('user:index')
    return render(request, 'userspace/login.html', {'title': 'Login'})

def logout(request):
    auth.logout(request)
    return redirect('user:index')
