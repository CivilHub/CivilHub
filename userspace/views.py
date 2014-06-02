# -*- coding: utf-8 -*-
import hashlib, datetime, random, string, os, captcha
from json import dumps
from PIL import Image
from bookmarks.models import Bookmark
from ipware.ip import get_ip
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe
from models import UserProfile, RegisterDemand, LoginData
from forms import *


def index(request):
    """
    User profile / settings
    """
    if not request.user.is_authenticated():
        return redirect('user:login')
    user = User.objects.get(pk=request.user.id)
    try:
        prof = UserProfile.objects.get(user=user.id)
    except:
        prof = UserProfile()
        prof.user = user
        prof.save()
        prof = UserProfile.objects.latest()
    ctx = {
        'user': user,
        'profile': prof,
        'form': UserProfileForm(initial={
                  'first_name': user.first_name,
                  'last_name':  user.last_name,
                  'email':      user.email,
                  'description':prof.description,
                  'birth_date': prof.birth_date,
              }),
        'avatar_form': AvatarUploadForm(),
        'title': _('User Area'),
    }
    return render(request, 'userspace/index.html', ctx)

    
def profile(request, username):
    """
    Show user info to other allowed users
    """
    if not request.user.is_authenticated():
        return redirect('user:login')
    user = get_object_or_404(User, username=username)
    prof = get_object_or_404(UserProfile, user=user)
    # TODO - to jest żywcem przeniesione z panelu edycji, trzeba
    # utworzyć nowe templaty
    ctx = {
        'cuser': user,
        'profile': prof,
        'title': _('User Profile'),
    }
    return render(request, 'userspace/profile.html', ctx)


def register(request):
    """
    Register new user via django system.
    """
    if request.method == 'POST':
        f = RegisterForm(request.POST)

        # talk to the reCAPTCHA service
        #~ response = captcha.client.submit(
            #~ request.POST.get('recaptcha_challenge_field'),
            #~ request.POST.get('recaptcha_response_field'),
            #~ settings.RECAPTCHA_PRIVATE_KEY,
            #~ request.META['REMOTE_ADDR'],)

        #if response.is_valid:
        if f.is_valid():
            user = User()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user.username = username
            user.set_password(password)
            user.email = request.POST.get('email')
            user.is_active = False
            user.save()
            # Re-fetch user object from DB
            user = User.objects.latest('id')
            # Create user profile
            salt = hashlib.md5()
            salt.update(str(datetime.datetime.now().time))
            register_demand = RegisterDemand(
                activation_link = salt.hexdigest(),
                ip_address = get_ip(request),
                user = user
            )
            register_demand.save()
            site_url = request.build_absolute_uri('/user/activate/')
            # TODO: wysłać adres_strony/user/activate/ + activation_link
            # mailem.
            return render(request, 'userspace/test.html', {
                'link': site_url + str(register_demand.activation_link)
            })
        else:
            ctx = {
                'form': RegisterForm(initial={
                    'username': request.POST.get('username'),
                    'email':    request.POST.get('email')
                }),
                'title': _("Registration"),
                'errors': f.errors,
            }
            return render(request, 'userspace/register.html', ctx)
    ctx = {
        'form': RegisterForm,
        'title': _("Registration"),
    }
    return render(request, 'userspace/register.html', ctx)


def activate(request, activation_link=None):
    if activation_link == None:
        ctx = {
            'form': RegisterForm,
            'title': _('Sign Up'),
        }
        return render(request, 'userspace/register.html', ctx)
    demand = RegisterDemand.objects.get(activation_link=activation_link)
    user = demand.user
    if user is not None:
        user_id = user.pk
        user.is_active = True
        user.save()
        demand.delete()
        user = User.objects.get(pk=user_id)
        auth_user = auth.authenticate(username=user.username,
                                      password=user.password)
        return redirect('user:index')


def passet(request):
    """
    Set credentials for new users registered with social auth
    """
    ctx = {
        'title': _("Set your password"),
    }
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            user = User(request.user.id)
            user.username = f.cleaned_data['username']
            user.set_password(f.cleaned_data['password'])
            user.save()
            # Re-fetch user object from DB
            user = User.objects.get(pk=request.user.id)
            # Create user profile if not exists
            try:
                prof = UserProfile.objects.get(user=request.user.id)
            except:
                prof = UserProfile()
                prof.user = user
                prof.save()
            return redirect('user:index')
    ctx['form'] = RegisterForm()
    return render(request, 'userspace/pass.html', ctx)


@csrf_exempt
def pass_reset(request):
    """
    Pozwól zarejestrowanym użytkownikom zresetować zapomniane
    hasło na podstawie adresu email.
    """
    ctx = {}
    if request.method == 'POST':
        f = PasswordRemindForm(request.POST)
        
        # talk to the reCAPTCHA service
        response = captcha.client.submit(
            request.POST.get('recaptcha_challenge_field'),
            request.POST.get('recaptcha_response_field'),
            settings.RECAPTCHA_PRIVATE_KEY,
            request.META['REMOTE_ADDR'],)

        if response.is_valid:
            try:
                user = User.objects.get(email=request.POST.get('email'))
                new_pass = ''.join(random.choice(string.letters + string.digits) for _ in range(8))
                user.set_password(new_pass)
                user.save()
                ctx = {
                    'username': user.username,
                    'password': new_pass
                }
                return render(request, 'userspace/passremind-confirm.html', ctx)
            except ObjectDoesNotExist as ex:
                pass

        else:
            ctx['errors'] = f.errors

    ctx['title'] = _("Reset password")
    ctx['form'] = PasswordRemindForm()
    return render(request, 'userspace/passremind-form.html', ctx)


@csrf_exempt
def login(request):
    """
    Login form
    """
    if request.user.is_authenticated():
        return redirect('user:index')
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            try:
                user = User.objects.get(email=f.cleaned_data['email'])
            except User.DoesNotExist as ex:
                messages.add_message(request, messages.ERROR, _('Login credentials invalid.'))
                return redirect(reverse('user:login'))
            username = user.username
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    login_data = LoginData(
                        user = user,
                        address = get_ip(request)
                    )
                    login_data.save()
                    return redirect('activities:actstream')
        messages.add_message(request, messages.ERROR, _('Login credentials invalid.'))
        return redirect(reverse('user:login'))
    f = LoginForm()
    ctx = {
        'title': _('Login'),
        'form': f,
    }
    return render(request, 'userspace/login.html', ctx)


def logout(request):
    """
    Logout currently logged in user
    """
    auth.logout(request)
    return redirect('user:login')


def save_settings(request):
    """
    Save changes made by user in his/her profile
    """
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        prof = UserProfile.objects.get(user = user.id)
        f = UserProfileForm(request.POST)
        if f.is_valid():
            user.first_name = f.cleaned_data['first_name']
            user.last_name  = f.cleaned_data['last_name']
            prof.birth_date = f.cleaned_data['birth_date']
            prof.description= f.cleaned_data['description']
            error = None
            if error != None:
                ctx = {
                    'user': user,
                    'profile': prof,
                    'form': f,
                    'avatar_form': AvatarUploadForm(),
                    'errors': f.errors,
                    'title': _('User Area'),
                }
                return render(request, 'userspace/index.html', ctx)
            user.save()
            prof.save()
            messages.add_message(request, messages.SUCCESS, _('Settings saved'))
            return redirect('user:index')
    return HttpResponse(_('Form invalid'))


def chpass(request):
    """
    Change user's password
    """
    if request.method == 'POST':
        f = PasswordResetForm(request.POST)
        if f.is_valid():
            current = f.cleaned_data['current']
            password = f.cleaned_data['password']
            user = User.objects.get(pk=request.user.id)
            username = user.username
            chk = auth.authenticate(username = username, password = current)
            if chk is not None:
                if chk.is_active:
                    user.set_password(password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, _('Settings saved'))
                    return redirect('user:index')
            else:
                messages.add_message(request, messages.ERROR, _('Your current password is invalid.'))
                return redirect(reverse('user:chpass'))
        else:
            return HttpResponse(_('Form invalid'))
    f = PasswordResetForm()
    ctx = {
        'title': _('Change password'),
        'form': f,
    }
    return render(request, 'userspace/chpass.html', ctx)


def upload_avatar(request):
    """
    Upload/change user avatar
    """
    if request.method == 'POST':
        f = AvatarUploadForm(request.POST, request.FILES)
        if f.is_valid():
            user = UserProfile.objects.get(user=request.user.id)
            user.avatar = request.FILES['avatar']
            size = 30, 30
            path = os.path.join(settings.MEDIA_ROOT, 'img/avatars')
            file, ext = os.path.splitext(request.FILES['avatar'].name)
            thumbname = '30x30_' + file + ext
            img = Image.open(user.avatar)
            tmp = img.copy()
            tmp.thumbnail(size, Image.ANTIALIAS)
            tmp.save(os.path.join(path, thumbname))
            user.thumbnail = 'img/avatars/' + thumbname
            user.save()
            messages.add_message(request, messages.SUCCESS, _('Settings saved'))
    return redirect('user:index')


@require_safe
def my_bookmarks(request):
    """
    Return list of bookmarked elements belonging to
    currently logged in user in form of JSON objects.
    """
    if not request.is_ajax(): return HttpResponseBadRequest()

    bookmarks = []
    queryset = Bookmark.objects.filter(user=request.user)
    for b in queryset:
        target = b.content_object
        target_content_type = ContentType.objects.get_for_model(target)
        bookmarks.append({
            'id': b.pk,
            'content_type': target_content_type.pk,
            'target': target.get_absolute_url(),
            'label': target.__unicode__(),
        })
    return HttpResponse(dumps({
        'success': True,
        'bookmarks': bookmarks,
    }))
