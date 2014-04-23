from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from forms import RegisterForm

def index(request):
    return render(request, 'userspace/index.html', {'title': 'Test'})

def register(request):
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            user = User()
            user.username = f.cleaned_data['username']
            user.password = f.cleaned_data['password']
            user.save()
            return redirect('user:index')
        else:
            return HttpResponse('Invalid data')
    ctx = {
        'form': RegisterForm,
        'title': 'Sign Up',
    }
    return render(request, 'userspace/register.html', ctx)

def login(request):
    if request.user.is_authenticated():
        return redirect('user:index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                redirect('user:index')
    return render(request, 'userspace/login.html', {'title': 'Login'})

def logout(request):
    auth.logout(request)
    return redirect('user:index')
