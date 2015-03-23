# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from actstream.models import model_stream, user_stream, following

from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from rest_framework import views as rest_views
from rest_framework.response import Response

from rest.permissions import IsOwnerOrReadOnly
from rest.serializers import PaginatedActionSerializer
from locations.serializers import ContentPaginatedSerializer, SimpleLocationSerializer
from bookmarks.models import Bookmark

from .helpers import profile_activation, random_username, create_username
from .managers import SocialAuthManager
from .serializers import UserAuthSerializer, UserSerializer, SocialAuthSerializer, \
            BookmarkSerializer


def user_dict(user):
    """
    Helper przydatny w dwóch poniższych funkcjach. Przedstawia podsumowanie
    informacji o użytkowniku w formacie apetycznym dla mobilnej aplikacji.
    """
    if not isinstance(user, User):
        raise Error(u"user must be django.contrib.auth.user instance")
    return {
        'success'   : True,
        'id'        : user.pk,
        'token'     : user.auth_token.key,
        'username'  : user.username,
        'email'     : user.email,
        'first_name': user.first_name,
        'last_name' : user.last_name,
        'avatar'    : user.profile.avatar.url,
    }


@csrf_exempt
def obtain_auth_token(request):
    """
    Widok dla aplikacji mobilnej pozwalający nam zalogować
    użytkownika przy pomocy email i hasła.
    """
    context = {'success': False,}
    if request.method != 'POST':
        context.update({'error': _("Only POST requests allowed"),})
    else:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            system_user = User.objects.get(email=email)
            user = auth.authenticate(username=system_user.username, password=password)
            if user is not None:
                context.update(user_dict(system_user))
        except User.DoesNotExist:
            user = None
    return HttpResponse(json.dumps(context), content_type='application/json')


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

    def post(self, request):

        from social.apps.django_app.utils import load_strategy
        from urllib2 import unquote

        strategy = load_strategy()
        uid      = request.POST.get('uid')
        provider = request.POST.get('provider')
        details  = json.loads(unquote(request.DATA.get('details')))
        response = json.loads(unquote(request.DATA.get('response')))

        try:
            social = UserSocialAuth.objects.get(provider=provider,uid=uid)
            return Response(user_dict(social.user))
        except UserSocialAuth.DoesNotExist:
            manager = SocialAuthManager(provider, uid, details)
            if manager.user.pk:
                profile = profile_activation(manager.user)
            manager_data = manager.is_valid()
            return Response(user_dict(manager.user))


class UserFollowedLocationsAPI(rest_views.APIView):
    """ Lista lokalizacji, które obserwuje użytkownik. """
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        if request.user.is_anonymous():
            return Response([])
        locations = request.user.profile.followed_locations()
        serializer = SimpleLocationSerializer(locations, many=True)
        return Response(serializer.data)


class UserSummaryAPI(rest_views.APIView):
    """
    Widok podsumowania dla użytkownika. Działa podobnie, jak moduł wyświetlający
    ostatnie wpisy w podsumowaniu lokalizacji, z tym, że zbiera wpisy ze wszystkich
    lokacji obserwowanych przez użytkownika.
    """
    paginate_by = 48
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):

        # Id lokacji, z której pobieramy wpisy
        location_pk = request.QUERY_PARAMS.get('pk', 0)
        # Numer strony do wyświetlenia
        page = request.QUERY_PARAMS.get('page', 1)
        # Rodzaj typu zawartości (albo wszystkie)
        content = request.QUERY_PARAMS.get('content', 'all')
        # Zakres dat do wyszukiwania
        time = request.QUERY_PARAMS.get('time', 'any')
        # Wyszukiwanie po tytułach wpisów
        haystack = request.QUERY_PARAMS.get('haystack', None)
        
        content_objects = []
        for location in request.user.profile.followed_locations():
            content_objects += location.content_objects()
        content_objects = sorted(content_objects, reverse=True,
                                    key=lambda x: x['date_created'])

        if content != 'all':
            content_objects = [x for x in content_objects if x['type']==content]
        if time != 'any':
            content_objects = [x for x in content_objects\
                if x['date_created'] >= get_time_difference(time).isoformat()]
        if haystack:
            content_objects = [x for x in content_objects \
                if haystack.lower() in x['title'].lower()]

        paginator = Paginator(content_objects, self.paginate_by)
        items = paginator.page(page)
        serializer_context = {'request': request}
        serializer = ContentPaginatedSerializer(items, context=serializer_context)

        return Response(serializer.data)


class UserBookmarksViewSet(viewsets.ModelViewSet):
    """ Pozwala użytkownikom manipulować zakładkami. """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = BookmarkSerializer
    paginate_by = None

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class UserFollowAPIView(rest_views.APIView):
    """
    Widok API obsługujący przycisk podążania za użytkownikiem. Tylko zapytania
    typu POST. Wymagane jest podanie ID użytkownika, którego chcemy obserwować
    w parametrze `pk` żądania. Zwracana wartość to true albo false w zależności
    od tego, czy zaczynamy, czy przestajemy obserwować drugiego użytkownika.
    Przykład odpowiedzi:
        ```{'fallow': true }```
    
    """
    permission_classes = (rest_permissions.IsAuthenticated,)

    def post(self, request):
        target_user = None
        pk = request.DATA.get('pk', None)
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            pass

        if target_user is None:
            raise Http404()

        if target_user in following(request.user):
            unfollow(request.user, target_user)
        else:
            follow(request.user, target_user, actor_only=True)

        return Response({'follow': target_user in following(request.user)})


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
        if len(following(request.user)) > 0:
            actstream = user_stream(request.user)
        else:
            actstream = []
        page = request.QUERY_PARAMS.get('page')
        paginator = Paginator(actstream, settings.STREAM_PAGINATOR_LIMIT)
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:
            actions = paginator.page(1)
        except EmptyPage:
            actions = paginator.page(paginator.num_pages)
        serializer = PaginatedActionSerializer(actions,
                                               context={'request': request})
        return Response(serializer.data)
