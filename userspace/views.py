# -*- coding: utf-8 -*-
import hashlib, datetime, random, string, os
from json import dumps
from PIL import Image
from datetime import timedelta
from django.utils import timezone
from bookmarks.models import Bookmark
from ipware.ip import get_ip
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe, require_POST
from django.contrib.auth.decorators import login_required
from actstream.models import model_stream
from civmail import messages as emails
from djmail.template_mail import MagicMailBuilder as mails
from models import UserProfile, RegisterDemand, LoginData
from helpers import UserActionStream
from places_core.tasks import send_poll_email
from places_core.helpers import truncatesmart, process_background_image
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
        'appname': 'userarea',
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
    user = get_object_or_404(User, username=username)
    prof = get_object_or_404(UserProfile, user=user)
    # Custom action stream
    stream  = UserActionStream(user)
    actions = stream.get_actions(action_type  = 'actor')
    ctx = {
        'cuser'  : user,
        'profile': prof,
        'title'  : _("User Profile"),
        'stream' : actions,
    }
    return render(request, 'userspace/profile.html', ctx)


def register(request):
    """
    Register new user via django system.
    """
    if request.method == 'POST':
        f = RegisterForm(request.POST)

        if f.is_valid():
            lang = translation.get_language()
            user = User()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user.username = username
            user.set_password(password)
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name  = request.POST.get('last_name')
            user.is_active = False
            try:
                user.save()
            except Exception:
                # Form valid, but user already exists
                ctx = {
                    'form': RegisterForm(initial={
                        'username': request.POST.get('username'),
                        'email':    request.POST.get('email')
                    }),
                    'title' : _("Registration"),
                    'errors': _("Selected username already exists. Please provide another one."),
                }
                return render(request, 'userspace/register.html', ctx)
            # Re-fetch user object from DB
            user = User.objects.latest('id')

            try:
                # Create register demand object in DB
                salt = hashlib.md5()
                salt.update(settings.SECRET_KEY + str(datetime.datetime.now().time))
                register_demand = RegisterDemand(
                    activation_link = salt.hexdigest(),
                    ip_address      = get_ip(request),
                    user            = user,
                    email           = user.email,
                    lang            = translation.get_language()
                )
                register_demand.save()
                register_demand = RegisterDemand.objects.latest('pk')
            except Exception as ex:
                # if something goes wrong, delete created user to avoid future
                # name conflicts (and allow another registration).
                user.delete()
                print str(ex)
                return render(request, 'userspace/register-failed.html', {
                    'title': _("Registration failed")
                })

            # Create activation link
            site_url = request.build_absolute_uri('/user/activate/')
            link = site_url + str(register_demand.activation_link)

            try:
                # Send email with activation link.
                translation.activate(register_demand.lang)
                email = emails.ActivationLink()
                email.send(register_demand.email, {'link':link})
                # Show confirmation
                return render(request, 'userspace/register-success.html', {
                    'title': _("Message send"),
                })
            except Exception as ex:
                # User is registered and link is created, but there was errors
                # during sanding email, so just show static page with link.
                print str(ex)
                return render(request, 'userspace/register-errors.html', {
                    'title': _("Registration"),
                    'link' : link,
                })
    
        # Form invalid
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

    # Display registration form.
    ctx = {
        'form' : RegisterForm,
        'title': _("Registration"),
    }
    return render(request, 'userspace/register.html', ctx)


def activate(request, activation_link=None):
    """ Activate new user account and delete related user demand object. """
    from rest_framework.authtoken.models import Token
    if activation_link == None:
        ctx = {
            'form': RegisterForm,
            'title': _('Sign Up'),
        }
        return render(request, 'userspace/register.html', ctx)
    demand = RegisterDemand.objects.get(activation_link=activation_link)
    user = demand.user
    lang = demand.lang
    if user is not None:
        user_id = user.pk
        user.is_active = True
        user.save()
        demand.delete()
        user = User.objects.get(pk=user_id)
        user = auth.authenticate(username=user.username,
                                      password=user.password)
        delta_t = timezone.now() + timedelta(days=3)
        send_poll_email.apply_async(args=(user_id,), eta=delta_t)
        # Create auth token for REST api:
        token = Token.objects.create(user=user)
        token.save()
        return redirect('user:active', lang=lang)


def active(request, lang=None):
    """
    Statyczny widok podziękowania za zarejestrowanie w serwisie
    i zaproszenie do pierwszego logowania.
    """
    ctx = {
        'title': _("Thank you for registration")
    }
    ctx['lang'] = lang if lang else settings.LANGUAGE_CODE
    return render(request, 'userspace/active.html', ctx)


def passet(request):
    """
    Set credentials for new users registered with social auth.
    """
    ctx = {
        'title': _("Set your password"),
    }
    if request.method == 'POST':
        f = SocialAuthPassetForm(request.POST)
        if f.is_valid():
            user = User(request.user.id)
            user.username = f.cleaned_data['username']
            user.set_password(f.cleaned_data['password'])
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
        ctx['form'] = SocialAuthPassetForm(request.POST)
        return render(request, 'userspace/pass.html', ctx)
    ctx['form'] = SocialAuthPassetForm()
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
        #~ response = captcha.client.submit(
            #~ request.POST.get('recaptcha_challenge_field'),
            #~ request.POST.get('recaptcha_response_field'),
            #~ settings.RECAPTCHA_PRIVATE_KEY,
            #~ request.META['REMOTE_ADDR'],)

        if f.is_valid:
            try:
                # If user does not exist, there is no need to do all this stuff.
                user = User.objects.get(email=request.POST.get('email'))
                new_pass = ''.join(random.choice(string.letters + string.digits) for _ in range(8))
                user.set_password(new_pass)
                ctx = {
                    'username': user.username,
                    'password': new_pass
                }
                translation.activate(user.profile.lang)
                email = emails.PasswordResetMail()
                email.send(user.email, ctx)
                user.save()
            except ObjectDoesNotExist as ex:
                # If user does not exist, pretend that everything is OK. This
                # way no one will be able to find if given email exists in db.
                pass

            return render(request, 'userspace/passremind-confirm.html', ctx)

        else:
            ctx['errors'] = f.errors

    ctx['title'] = _("Reset password")
    ctx['form'] = PasswordRemindForm()
    return render(request, 'userspace/passremind-form.html', ctx)


@csrf_exempt
def login(request):
    """
    Login form. Performs user login and record login data with basic info
    about user IP address. It also keeps 5 last login datas in database for
    each user.
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
                    datas = LoginData.objects.filter(user=user).order_by('-date')
                    if len(datas) > 5:
                        for i in range (len(datas) - 5):
                            datas[i].delete()
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
    return HttpResponse(dumps({
        'avatar': user.avatar.url
    }));
    #return redirect('user:index')


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
            'label': truncatesmart(target.__unicode__(), 30),
        })
    return HttpResponse(dumps({
        'success': True,
        'bookmarks': bookmarks,
    }))


class UserFollowedLocations(DetailView):
    """
    Present list of followed locations.
    """
    model = UserProfile
    template_name = 'userspace/followed-locations.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        ctx = super(UserFollowedLocations, self).get_context_data()
        ctx['title'] = _("My places")
        return ctx


def test_view(request):
    """
    Do testowania różnych rzeczy.
    """
    import json
    if request.is_ajax():
        return HttpResponse(json.dumps({'info':'Yes, is AJAX request'}))
    else:
        return HttpResponse("No, it's not AJAX request")


@login_required
@require_POST
def change_background(request):
    """
    Allow users to customize their profiles.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            profile = request.user.profile
        else:
            return HttpResponseForbidden()
        try:
            os.unlink(profile.background_image.path)
        except Exception:
            pass
        profile.background_image = process_background_image(request.FILES['background'], 'img/backgrounds')
        profile.save()
        return redirect(request.META['HTTP_REFERER'])
