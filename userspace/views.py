# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from forms import RegisterForm, LoginForm

def index(request):
    """
    User profile / settings
    """
    if not request.user.is_authenticated():
        return redirect('user:login')
    ctx = {
        'user': request.user,
        'title': 'User Area',
    }
    return render(request, 'userspace/index.html', ctx)

def register(request):
    """
    Register new user via django system
    """
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            user = User()
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()
            auth.authenticate(username = username, password = password)
            return redirect('user:index')
        else:
            return HttpResponse('Invalid data')
    ctx = {
        'form': RegisterForm,
        'title': 'Sign Up',
    }
    return render(request, 'userspace/register.html', ctx)

def passet(request):
    """
    Set credentials for new users registered with social auth
    """
    ctx = {
        'title': "Set your password",
    }
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            user = User(request.user.id)
            user.username = f.cleaned_data['username']
            user.set_password(f.cleaned_data['password'])
            user.save()
            return redirect('user:index')
    else:
        ctx['form'] = RegisterForm()
        return render(request, 'userspace/pass.html', ctx)

def login(request):
    """
    Login form
    """
    if request.user.is_authenticated():
        return redirect('user:index')
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('user:index')
        else:
            return redirect(reverse('user:login'))
    f = LoginForm()
    ctx = {
        'title': 'Login',
        'form': f,
    }
    return render(request, 'userspace/login.html', ctx)

def logout(request):
    """
    Logout currently logged in user
    """
    auth.logout(request)
    return redirect('user:index')
