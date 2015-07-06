# -*- coding: utf-8 -*-
import hashlib, datetime, random, string, os, json, re
from json import dumps
from PIL import Image
from datetime import timedelta
from django.utils import timezone
from ipware import ip
from django.http import HttpResponse, HttpResponseBadRequest, \
                         HttpResponseForbidden, HttpResponseNotFound, Http404
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, UpdateView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.gis.geoip import GeoIP
from django.utils.translation import ugettext as _
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe, require_POST
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.apps.django_app.default.models import UserSocialAuth
from actstream.models import model_stream, user_stream, following
from actstream.actions import follow, unfollow
from rest_framework.authtoken.models import Token

from civmail import messages as emails
from djmail.template_mail import MagicMailBuilder as mails
from helpers import UserActionStream, random_password
from places_core.helpers import truncatesmart, process_background_image
from places_core.mixins import LoginRequiredMixin
from gallery.forms import BackgroundForm
from blog.models import News
from ideas.models import Idea
from organizations.models import Invitation, Organization
from polls.models import Poll
from topics.models import Discussion
from bookmarks.models import Bookmark
from locations.models import Location
from locations.helpers import get_most_followed
from locations.serializers import ContentPaginatedSerializer, SimpleLocationSerializer
from forms import *
from utils.http import set_cookie

from .models import CloseAccountDemand, UserProfile, RegisterDemand, LoginData
from .helpers import profile_activation, random_username, \
                     create_username, update_profile_picture, \
                     get_gravatar_image

import logging
logger = logging.getLogger('userspace')


class SocialAuthErrorView(TemplateView):
    """ Redirect social users here when he didnt' provided proper email
        address from their social accounts.
    """
    template_name = 'userspace/s_auth_error.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('auth_error'):
            return redirect('/')
        self.request.session.pop('auth_error')
        logger.info(u"[%s] Ktoś tu był" % str(timezone.now()))
        return super(SocialAuthErrorView, self).dispatch(*args, **kwargs)


class SwitchUserImages(LoginRequiredMixin, View):
    """ This view is dedicated for admins - they can bring back default user
        avatar image for users whose images are 'inappropriate'.
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        return super(SwitchUserImages, self).dispatch(*args, **kwargs)

    def post(self, request, **kwargs):
        user = User.objects.get(pk=request.POST.get('user'))
        if request.POST.get('action') == 'background':
            user.profile.set_default_background()
        else:
            user.profile.set_default_avatar()
        return redirect(user.profile.get_absolute_url())


class DeleteAccountView(LoginRequiredMixin, View):
    """ Delete user account. In fact, we are not removing user data from database,
        as this could have some complications. Here, we create or delete existing
        CloseAccountDemand instance.
    """
    template_name = 'userspace/delete_account.html'

    def dispatch(self, *args, **kwargs):
        self.object = self.request.user
        if self.object.is_anonymous():
            raise Http404
        return super(DeleteAccountView, self).dispatch(*args, **kwargs)

    def get_demand(self):
        try:
            return CloseAccountDemand.objects.get(user=self.request.user)
        except CloseAccountDemand.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        return {
            'profile': self.request.user.profile,
            'demand': self.get_demand(), }

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        demand = self.get_demand()
        if demand is None:
            demand = CloseAccountDemand.objects.create(user=self.request.user)
            message = _(u"Your account will be deleted in 7 days")
        else:
            demand.delete()
            message = _(u"Your demand has been rejected")
        messages.success(request, message)
        return redirect(request.user.profile.get_absolute_url())


class ReloginView(SingleObjectMixin, View):
    """ This view helps us to relogin user and set additional session data
        before redirecting him to another page. This is used when we try to
        force user to login via Facebook or Google account to get access to
        additional functions, like following Facebook friends etc.
    """
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.relogin_data = self.request.session.pop('relogin')
        except KeyError:
            raise Http404
        self.relogin_data = json.loads(self.relogin_data)
        return super(ReloginView, self).dispatch(*args, **kwargs)

    def post(self, request, **kwargs):
        auth.logout(request)
        backend = request.POST.get('backend')
        return redirect("{}?next={}".format(
            reverse('social:begin', kwargs={
                'backend': request.POST.get('backend'), }),
            self.relogin_data['next_url']))

    def get_context_data(self):
        return {'profile': self.object.profile, }


class UserActivityView(TemplateView):
    """
    Static view of user activity list (aka the dashboard).
    Loading a template and a list of the last five elements of each type
    content. In addition, a separate view of the API are loaded user actions.
    """
    template_name = 'userspace/activity.html'

    def get_latest(self, actstream, item_type):
        """ Get latest items of selected type from user activity stream. """
        if item_type   == 'blog':
            ct = ContentType.objects.get_for_model(News).pk
        elif item_type == 'ideas':
            ct = ContentType.objects.get_for_model(Idea).pk
        elif item_type == 'topics':
            ct = ContentType.objects.get_for_model(Discussion).pk
        elif item_type == 'polls':
            ct = ContentType.objects.get_for_model(Poll).pk
        raw_set = actstream.filter(action_object_content_type_id=ct) \
                .distinct('action_object_object_id') \
                .order_by('action_object_object_id')[:5]
        return [x.action_object for x in raw_set]

    def get_context_data(self, **kwargs):
        context = super(UserActivityView, self).get_context_data(**kwargs)
        if len(following(self.request.user)) > 0:
            actstream = user_stream(self.request.user)
            context['blog']   = self.get_latest(actstream, 'blog')
            context['ideas']  = self.get_latest(actstream, 'ideas')
            context['topics'] = self.get_latest(actstream, 'topics')
            context['polls']  = self.get_latest(actstream, 'polls')
        return context

    def get(self, request):
        if request.user.is_anonymous():
            return redirect('/')
        return super(UserActivityView, self).get(request)


def register_credentials_check(request):
    """
    Check your username and email for the purpose of the registration form.
    """
    if not request.method == 'POST':
        raise Http404
    email = request.POST.get('email')
    uname = request.POST.get('uname')
    ctx = {'errors': []}
    if email and User.objects.filter(email=email).count():
        ctx['errors'].append({'label': 'email',
            'message': u"User with this email address already exists"})
    if uname and User.objects.filter(username=uname).count():
        ctx['errors'].append({'label': 'username',
            'message': u"User with this username already exists"})
    return HttpResponse(json.dumps(ctx), content_type="application/json")


class SetTwitterEmailView(FormView):
    """
    In this view, the user who registers with Twitter accounts
    sets your email address. The address is required and must be unique
    the whole system.
    """
    form_class = TwitterEmailForm
    template_name = 'userspace/twitter-email-form.html'

    def get_context_data(self, **kwargs):
        context = super(SetTwitterEmailView, self).get_context_data(**kwargs)
        context['title'] = _("Set email")
        return context

    def form_valid(self, form, **kwargs):
        self.request.session['account_email'] = form.cleaned_data['account_email']
        return redirect(reverse('social:complete', kwargs={'backend':'twitter'}))


@require_POST
@login_required
def upload_avatar(request):
    """ Change user profile picture. """
    form = BackgroundForm(request.POST, request.FILES)
    if form.is_valid():
        profile = UserProfile.objects.get(user=request.user)
        box = (
            form.cleaned_data['x'],
            form.cleaned_data['y'],
            form.cleaned_data['x2'],
            form.cleaned_data['y2'],
        )
        image = Image.open(form.cleaned_data['image'])
        image = image.crop(box)
        update_profile_picture(profile, image)
    return redirect(reverse('user:index'))


class UserProfileView(DetailView):
    """ Show user info to other allowed users. """
    model = UserProfile
    context_object_name = 'profile'
    slug_field = 'clean_username'
    slug_url_kwarg = 'username'
    template_name = 'userspace/profile.html'

    def get_context_data(self, object=None):
        context = super(UserProfileView, self).get_context_data()
        context['cuser'] = object.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ User profile settings. """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'userspace/index.html'
    context_object_name = 'profile'

    def get_object(self):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse('user:index')

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial.update({
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context.update({
            'title': self.object.user.get_full_name(),
            'passform': PasswordResetForm(),
            'avatar_form': BackgroundForm(),
        })
        return context

    def form_valid(self, form):
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        return super(ProfileUpdateView, self).form_valid(form)


class RegisterFormView(FormView):
    """ Register new user via standard form. """
    form_class = RegisterForm
    template_name = 'userspace/register.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/activity/')
        return super(RegisterFormView, self).get(request)

    def form_valid(self, form):
        # Create user instance with fixed username
        form.instance.username = create_username(
            form.instance.first_name,
            form.instance.last_name
        )
        form.instance.is_active = False
        form.instance.set_password(form.cleaned_data['password1'])
        form.instance.save()
        # Create token for mobile API
        Token.objects.create(user=form.instance)
        # Create registration link and save along with request params
        salt = hashlib.md5()
        salt.update(settings.SECRET_KEY + str(datetime.datetime.now().time))
        register_demand = RegisterDemand.objects.create(
            activation_link = salt.hexdigest(),
            ip_address = ip.get_ip(self.request),
            user = form.instance,
            email = form.instance.email,
            lang = translation.get_language_from_request(self.request)
        )
        # Create full link to activation page for new user
        site_url = self.request.build_absolute_uri('/user/activate/')
        link = site_url + str(register_demand.activation_link)
        # Send email in user's own language if possible
        email = emails.ActivationLink()
        email_context = {'link': link}
        if translation.check_for_language(register_demand.lang):
            email_context.update({'lang': register_demand.lang})
        email.send(register_demand.email, email_context)
        return render(self.request, 'userspace/register-success.html',
                                        {'title': _("Message send"),})


def activate(request, activation_link=None):
    """ Activate new user account and delete related user demand object. """
    if activation_link == None:
        ctx = {
            'form': RegisterForm,
            'title': _('Sign Up'),
        }
        return render(request, 'userspace/register.html', ctx)
    try:
        demand = RegisterDemand.objects.get(activation_link=activation_link)
    except RegisterDemand.DoesNotExist:
        # TODO wypadałoby coś tutaj pokazać.
        return HttpResponse(_("Activation link invalid"))
    user = demand.user
    lang = demand.lang
    if user is not None:
        user.is_active = True
        user.save()
        user.profile.lang = lang
        user.profile.save()
        demand.delete()
        update_profile_picture(user.profile, get_gravatar_image(user.email))
        system_user = auth.authenticate(username=user.username)
        if system_user is not None:
            auth.login(request, system_user)
        request.session['new_user'] = True
        return redirect(reverse('user:active'))


class NewUserView(TemplateView):
    """
    Welcome new user and introduce him to locations that would want to
    observe. The view is "one-use". It only show the newly-logged.
    Redirect method is GET.
    """
    template_name = 'userspace/active.html'

    def get_context_data(self):
        country_code = GeoIP().country_code(ip.get_ip(self.request))
        if country_code is None:
            country_code = settings.DEFAULT_COUNTRY_CODE
        context = super(NewUserView, self).get_context_data()
        context['locations'] = get_most_followed(country_code)
        return context

    def get(self, request):
        if request.session.get('new_user') is None:
            return redirect('/activity/')
        invitations = Invitation.objects.filter(email=request.user.email,
                                                is_accepted=False)
        if len(invitations):
            return redirect(reverse('organizations:invitations'))
        del request.session['new_user']
        return super(NewUserView, self).get(request)


def passet(request):
    """ Set credentials for new users registered with social auth. """
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
    Allow registered users to reset forgotten
    password based on email address.
    """
    if request.user.is_authenticated():
        return redirect('/')

    ctx = {'form': PasswordRemindForm()}
    if request.method == 'POST':
        f = PasswordRemindForm(request.POST)

        if f.is_valid():
            try:
                # If user does not exist, there is no need to do all this stuff.
                user = User.objects.get(email=request.POST.get('email'))
                new_pass = ''.join(random.choice(string.letters + string.digits) for _ in range(8))
                user.set_password(new_pass)
                ctx = {
                    'username': user.username,
                    'password': new_pass,
                    'lang': user.profile.lang,
                }
                email = emails.PasswordResetMail()
                email.send(user.email, ctx)
                user.save()
            except ObjectDoesNotExist as ex:
                # If user does not exist, pretend that everything is OK. This
                # way no one will be able to find if given email exists in db.
                pass

            return render(request, 'userspace/passremind-confirm.html', ctx)

        else:
            ctx['form'] = PasswordRemindForm(request.POST)
            ctx['errors'] = f.errors

    return render(request, 'userspace/passremind-form.html', ctx)


class LoginFormView(FormView):
    """
    Zastępujemy natywny widok logowania Django swoim własnym.
    Tutaj rejestrujemy aktywność naszych użytkowników.
    """
    form_class = LoginForm
    template_name = 'userspace/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/activity/')
        return super(LoginFormView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(LoginFormView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get('next', None)
        if next_url:
            context.update({'next': next_url})
        return context

    def form_valid(self, form):
        auth.login(self.request, form.instance)
        info = LoginData.objects.create(user=form.instance,
                                        address=ip.get_ip(self.request))
        next_url = self.request.POST.get('next')
        if len(next_url):
            return redirect(next_url)
        return redirect('/activity/')


def logout(request):
    """ Logout currently logged in user. """
    auth.logout(request)
    return redirect('user:login')


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


class UserFollowedLocations(DetailView):
    """
    Present list of followed locations.
    """
    model = UserProfile
    template_name = 'userspace/followed-locations.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'clean_username'

    def get_context_data(self, **kwargs):
        ctx = super(UserFollowedLocations, self).get_context_data()
        ctx['title'] = _("My places")
        return ctx


class UserBackgroundView(FormView):
    """
    Static view allows the user to select and crop the image background for
    user profile.
    """
    template_name = 'userspace/background-form.html'
    form_class = BackgroundForm

    def form_valid(self, form):
        from gallery.image import handle_tmp_image
        box = (
            form.cleaned_data['x'],
            form.cleaned_data['y'],
            form.cleaned_data['x2'],
            form.cleaned_data['y2'],
        )
        image = Image.open(form.cleaned_data['image'])
        image = image.crop(box)
        profile = UserProfile.objects.get(user=self.request.user)
        profile.image = handle_tmp_image(image)
        profile.save()
        return redirect(self.request.user.profile.get_absolute_url())


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
        profile.background_image = request.FILES['background']
        profile.save()
        return redirect(request.META['HTTP_REFERER'])


class AccountManagementView(View):
    """ Allows users to add social accounts to their profile.
    """
    template_name = 'userspace/manage_accounts.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous():
            raise Http404
        self.request.session['relogin'] = json.dumps({
            'next_url': self.request.path, })
        return super(AccountManagementView, self).dispatch(*args, **kwargs)

    def get_context_data(self):
        return {
            'profile': self.request.user.profile,
            'cuser': self.request.user, }

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# NGO related views
# -----------------


class UserNGOList(DetailView):
    """ List all organizations created by selected user.
    """
    model = UserProfile
    slug_url_kwarg = 'username'
    slug_field = 'clean_username'
    context_object_name = 'profile'
    template_name = 'userspace/organization_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserNGOList, self).get_context_data()
        context['object_list'] = Organization.objects.filter(
                                    creator=self.object.user)
        return context
