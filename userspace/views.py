# -*- coding: utf-8 -*-
import hashlib, datetime, random, string, os, json, re
from json import dumps
from PIL import Image
from datetime import timedelta
from django.utils import timezone
from ipware.ip import get_ip
from django.http import HttpResponse, HttpResponseBadRequest, \
                         HttpResponseForbidden, HttpResponseNotFound
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, UpdateView, TemplateView
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.apps.django_app.default.models import UserSocialAuth
from actstream.models import model_stream, user_stream
from civmail import messages as emails
from djmail.template_mail import MagicMailBuilder as mails
from models import UserProfile, RegisterDemand, LoginData
from helpers import UserActionStream, random_password
from places_core.tasks import send_poll_email
from places_core.helpers import truncatesmart, process_background_image
from blog.models import News
from ideas.models import Idea
from polls.models import Poll
from topics.models import Discussion
from .models import Bookmark
from forms import *
# REST api
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from rest_framework import views as rest_views
from rest_framework.response import Response
from rest.permissions import IsOwnerOrReadOnly
from rest.serializers import PaginatedActionSerializer
from .managers import SocialAuthManager
from .serializers import BookmarkSerializer, \
                          UserAuthSerializer, \
                          UserSerializer, \
                          SocialAuthSerializer


class SocialApiView(rest_views.APIView):
    """
    Rejestracja/logowanie użytkowników portali społecznościowych. Ten widok
    korzysta z backendu Python Social Auth w celu ułatwienia integracji.
    Domyślnie prezentowana jest lista wszystkich kont.
    
    Logowanie/rejestracja przez API wymaga podania jednego z backendów:
    `twitter`, `facebook`, `google-plus`, `linkedin`.
    
    Przykładowe dane do zapytania (server_response to odpowiedzi od providera): 
    
    <pre><code>{
        provider: 'facebook',
        uid: '8777323423',
        details: encodeURI(server_response_1),
        response: encodeURI(server_response_2)
    }</code></pre>
    
    Uwierzytelniając użytkownika, w parametrach POST podajemy response z serwera
    usługi uwierzytelniającej wraz z nazwą usługi oraz uid użytkownika. System
    sprawdza, czy konto o tych parametrach już istnieje i w razie potrzeby
    tworzy nowe. W odpowiedzi otrzymamy obiekt z id oraz tokenem uwierzytelnia-
    jącym użytkownika.
    """
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        queryset = UserSocialAuth.objects.all()
        serializer = SocialAuthSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        from social.apps.django_app.utils import load_strategy
        from urllib2 import unquote
        strategy = load_strategy()
        uid = request.DATA.get('uid')
        provider = request.DATA.get('provider')
        details = json.loads(unquote(request.DATA.get('details')))
        response = json.loads(unquote(request.DATA.get('response')))
        try:
            social = UserSocialAuth.objects.get(provider=provider,uid=uid)
            return Response({'user_id': social.user.pk,
                              'auth_token': social.user.auth_token.key})
        except UserSocialAuth.DoesNotExist:
            manager = SocialAuthManager(provider, uid, details)
            manager_data = manager.is_valid()
            return Response({'user_id': manager.user.pk,
                              'auth_token': manager.user.auth_token.key})


class UserAPIViewSet(viewsets.ModelViewSet):
    """
    Zarządzanie listą użytkowników z poziomu aplikacji mobilnej. Widok zapewnia
    wszystkie operacje CRUD na liście użytkowników.
    
    ### Tworzenie użytkownika:
    Pola wymagane: *username*, *first_name*, *last_name*, *password*, *email*
    
    **UWAGA**: Ten widok nie korzysta z polityki uprawnień Django (bo nie ma takiej
    fizycznej możliwośći). Trzeba **UWAŻNIE** przemyśleć implementację systemu w
    środowisku produkcyjnym.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    paginate_by = None
    permission_classes = (rest_permissions.AllowAny,)


class UserAuthAPIViewSet(viewsets.ViewSet):
    """
    *Deprecated*: Lepiej korzystać z interfejsu pod adresem `/api-userspace/social_auth/`
    
    Tutaj wysyłamy nazwę providera oraz uid użytkownika social auth w celu
    pobrania instancji użytkownika w systemie Django. Dane należy wysłać
    getem, jeżeli użytkownik istnieje w systemie, zostaną zwrócone jego
    zserializowane dane, w innym przypadku otrzymamy w odpowiedzi "Forbidden". 
    Przykład:
    
    ```/api-userspace/socials/?provider=google-plus?id=tester@gmail.com```
    
    **TODO**: Warto pomyśleć o zaszyfrowaniu tego interfejsu!!!
    """
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request):
        provider = request.QUERY_PARAMS.get('provider')
        uid = request.QUERY_PARAMS.get('uid')
        if provider and uid:
            user = UserSocialAuth.objects.get(provider=provider,uid=uid).user
            serializer = UserAuthSerializer(user)
            return Response(serializer.data)
        return Response("Forbidden")


class CredentialCheckAPIView(rest_views.APIView):
    """
    Widok pozwalający w prosty sposób sprawdzić, czy podany adres email lub
    nazwa użytkownika zostały już zarejestrowane w systemie. 
    
    #### Przykład zapytania o adres email:
    
    ```/api-userspace/credentials/?email=tester@test.pl```
    
    #### Przykład zapytania o nazwę użytkownika:
    
    ```/api-userspace/credentials/?uname=tester```
    
    W każdym przypadku otrzymujemy w odpowiedzi prosty obiekt z własnością 
    `valid` ustawioną na `true` lub `false`.
    """
    queryset = User.objects.all()
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        email = request.QUERY_PARAMS.get('email')
        uname = request.QUERY_PARAMS.get('uname')
        valid = False
        if email and re.match(r'[^@]+@[^@]+\.[^@]+', email):
            try:
                usr = User.objects.get(email=email)
            except User.DoesNotExist:
                valid = True
        elif uname:
            try:
                usr = User.objects.get(username=uname)
            except User.DoesNotExist:
                valid = True
        return Response({'valid': valid})


class ActivityAPIViewSet(rest_views.APIView):
    """
    Zastępstwo dla standardowego widoku `django-activity-stream`. Prezentuje
    tzw. feed użytkownika, który jest aktualnie zalogowany. Jeżeli użytkownik
    jest anonimowy, dostanie w odpowiedzi 404.
    """
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        if request.user.is_anonymous(): return HttpResponseNotFound()
        actstream = user_stream(request.user)
        page = request.QUERY_PARAMS.get('page')
        paginator = Paginator(actstream, settings.STREAM_PAGINATOR_LIMIT)
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            actions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            actions = paginator.page(paginator.num_pages)
        serializer = PaginatedActionSerializer(actions,
                                               context={'request': request})
        return Response(serializer.data)


class BookmarkAPIViewSet(viewsets.ModelViewSet):
    """
    Prosty widok umożliwiający pobieranie/tworzenie zakładek powiązanych
    z użytkownikiem. Domyślnie listowane są wszystkie zakładki, przekazanie
    w zapytaniu GET parametru `pk` wyświetli tylko zakładki powiązane z 
    konkretnym użytkownikiem o danym ID, np.:
    
    `/api-userspace/bookmarks/?pk=2`
    
    Tworząc zakładkę musimy tylko przekazać element docelowy, tzn. pk
    typu zawartości (`content_type`), oraz id konkretnego obiektu (`object_id`).
    "Twórcą" zakładki będzie zawsze aktualnie zalogowany użytkownik.
    """
    queryset = Bookmark.objects.all()
    paginate_by = None
    serializer_class = BookmarkSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        pk = self.request.QUERY_PARAMS.get('pk', None)
        if pk:
            return Bookmark.objects.filter(user=User.objects.get(pk=pk))
        else:
            return Bookmark.objects.all()

    def create(self, request):
        ct = request.DATA.get('content_type', None)
        id = request.DATA.get('object_id', None)
        content_type = ContentType.objects.get(pk=ct)
        try:
            bookmark = Bookmark.objects.get(content_type = content_type, 
                                         object_id = id,
                                         user = request.user)
            bookmark.delete()
            return Response(False)
        except Bookmark.DoesNotExist:
            bookmark = Bookmark.objects.create(
                content_type = content_type,
                object_id = id,
                user = request.user)
            bookmark.save()
            return Response(True)


class UserActivityView(TemplateView):
    """ """
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
                           .distinct('timestamp') \
                           .order_by('-timestamp')[:5]
        return [x.action_object for x in raw_set]

    def get_context_data(self, **kwargs):
        context = super(UserActivityView, self).get_context_data(**kwargs)
        actstream = user_stream(self.request.user)
        context['blog']   = self.get_latest(actstream, 'blog')
        context['ideas']  = self.get_latest(actstream, 'ideas')
        context['topics'] = self.get_latest(actstream, 'topics')
        context['polls']  = self.get_latest(actstream, 'polls')
        return context

    def get(self, request):
        if request.user.is_anonymous(): return HttpResponseNotFound()
        return super(UserActivityView, self).get(request)


class SetTwitterEmailView(FormView):
    """
    W tym widoku użytkownik, który rejestruje się przy pomocy konta na Twitterze
    ustawia swój adres email. Adres jest wymagany i musi być unikalny dla
    całego systemu.
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


class ProfileUpdateView(UpdateView):
    """ User profile settings. """
    model = UserProfile
    template_name = 'userspace/index.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            prof = UserProfile.objects.create(user=self.request.user)
            prof.save()
            return prof

    def get_context_data(self, **kwargs):
        from social.apps.django_app.default.models import UserSocialAuth
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.object.user.get_full_name()
        context['form'] = UserProfileForm(initial={
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name
        }, instance=self.object)
        context['passform'] = PasswordResetForm()
        context['avatar_form'] = AvatarUploadForm(initial={'avatar':self.object.avatar})

        try:
            us = UserSocialAuth.objects.get(user=self.object.user, provider='google-plus')
            context['google_data'] = {
                'token': us.extra_data['access_token'],
                'key': settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY,
            }
        except UserSocialAuth.DoesNotExist:
            us = None

        return context

    def get(self, request):
        if  request.user.is_anonymous():
            return HttpResponseNotFound()
        return super(ProfileUpdateView, self).get(request)


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
            prof.gender = f.cleaned_data['gender']
            prof.gplus_url = f.cleaned_data['gplus_url']
            prof.fb_url = f.cleaned_data['fb_url']
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
        'title'  : user.first_name + " " + user.last_name + " | CivilHub",
        'stream' : actions,
    }
    return render(request, 'userspace/profile.html', ctx)


def register(request):
    """
    Register new user via django system.
    """
    from rest_framework.authtoken.models import Token
    
    if request.user.is_authenticated():
        return redirect('/activity')
    
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
                # Create auth token for REST api:
                token = Token.objects.create(user=user)
                token.save()
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
                return render(request, 'staticpages/pages/home.html', ctx)
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
            except Exception as ex:
                # User is registered and link is created, but there was errors
                # during sanding email, so just show static page with link.
                print str(ex)
                return render(request, 'userspace/register-errors.html', {
                    'title': _("Registration"),
                    'link' : link,
                })
            # Show confirmation
            return redirect('user:message_sent')
    
        else:
            ctx = {
                'form': RegisterForm(initial={
                    'username': request.POST.get('username'),
                    'email':    request.POST.get('email')
                }),
                'title': _("Registration"),
                'errors': f.errors,
            }
            return render(request, 'staticpages/pages/home.html', ctx)

    # Display registration form.
    ctx = {
        'form' : RegisterForm,
        'title': _("Registration"),
        'plus_scope': ' '.join(settings.SOCIAL_AUTH_GOOGLE_PLUS_SCOPE),
        'plus_id': settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY,
    }
    return render(request, 'staticpages/pages/home.html', ctx)


def confirm_registration(request):
    """
    Show confirmation about successfull registration.
    """
    return render(request, 'userspace/register-success.html', {
        'title': _("Message send"),
    })


def activate(request, activation_link=None):
    """ Activate new user account and delete related user demand object. """
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
    from social.backends.google import GooglePlusAuth
    if request.user.is_authenticated():
        return redirect('user:index')
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        f = LoginForm(request.POST)
        if f.is_valid():
            try:
                user = User.objects.get(email=f.cleaned_data['email'])
            except User.DoesNotExist as ex:
                ctx = {'errors': _("Login credentials invalid")}
                return render(request, 'userspace/login.html', ctx)
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
                    elif len(datas) == 1:
                        # Jeżeli użytkownik loguje się pierwszy raz, pokazujemy mu listę
                        return redirect('locations:index')
                    return redirect('/activity/')
                else:
                    ctx = {'errors': _("Your account has not been activated")}
                    return render(request, 'userspace/login.html', ctx)
        ctx = {'errors': _("Fields can not be empty")}
        return render(request, 'userspace/login.html', ctx)
    f = LoginForm()
    ctx = {
        'title': _('Login'),
        'form': f,
        'plus_scope': ' '.join(settings.SOCIAL_AUTH_GOOGLE_PLUS_SCOPE),
        'plus_id': settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY,
    }
    return render(request, 'userspace/login.html', ctx)


def logout(request):
    """
    Logout currently logged in user
    """
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


def upload_avatar(request):
    """
    Upload/change user avatar
    """
    from .helpers import crop_avatar, delete_thumbnails
    if request.method == 'POST':
        f = AvatarUploadForm(request.POST, request.FILES)
        if f.is_valid():
            user = UserProfile.objects.get(user=request.user.id)
            if not u'anonymous' in user.avatar.name:
                try:
                    os.unlink(user.avatar.path)
                    delete_thumbnails(user.avatar.name.split('/')[-1:][0])
                except Exception:
                    pass
            user.avatar = crop_avatar(request.FILES['avatar'])
            size = 30, 30
            path = os.path.join(settings.MEDIA_ROOT, 'img/avatars')
            file, ext = os.path.splitext(user.avatar.name.split('/')[-1:][0])
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
        profile.background_image = request.FILES['background']
        profile.save()
        return redirect(request.META['HTTP_REFERER'])


class TestAPIView(rest_views.APIView):
    """
    Tutaj testujemy requesty i zapisujemy je do pliku.
    """
    permission_classes = (rest_permissions.AllowAny,)

    def post(self, request):
        pass
