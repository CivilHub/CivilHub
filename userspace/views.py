from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from forms import RegisterForm

def index(request):
    return render(request, 'userspace/index.html', {'title': 'Test'})

def register(request):
    ctx = {
        'form': RegisterForm,
        'title': 'Sign Up',
    }
    return render(request, 'userspace/register.html', ctx)

def create(request):
    f = RegisterForm(request.POST)
    if f.is_valid():
        pass
    return HttpResponse(f.is_valid())

def login(request):
    if request.user.is_authenticated():
        return redirect('user:index')
    return render(request, 'userspace/login.html', {'title': 'Login'})

def logout(request):
    auth.logout(request)
    return redirect('user:index')
