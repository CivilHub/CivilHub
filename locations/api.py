# -*- coding: utf-8 -*-
from ipware.ip import get_ip

from django.conf import settings
from django.utils import translation
from django.shortcuts import get_object_or_404
from django.core import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geoip import GeoIP
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions as rest_permissions
from rest_framework.response import Response

from ideas.models import Idea
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from places_core.helpers import sort_by_locale, get_time_difference
from locations.serializers import MapLocationSerializer

from .models import Country, Location
from .serializers import SimpleLocationSerializer, \
                         LocationListSerializer, \
                         CountrySerializer, \
                         ContentPaginatedSerializer, \
                         MapLocationSerializer
from rest.serializers import MyActionsSerializer, PaginatedActionSerializer


redis_cache = cache.get_cache('default')


class CapitalAPI(APIView):
    """
    Widok wyszukujący stolicę kraju najbardziej odpowiedniego dla lokalizacji
    aktualnego użytkownika. Nie trzeba tutaj przekazywać żadnych parametrów.
    """
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        code = GeoIP().country(get_ip(self.request))\
                      .get('country_code', settings.DEFAULT_COUNTRY_CODE)
        country = None
        try:
            country = Country.objects.get(code=code)
        except Country.DoesNotExist:
            country = get_object_or_404(Country, code=settings.DEFAULT_COUNTRY_CODE)
        capital = country.get_capital()
        if capital is not None:
            serializer = LocationListSerializer(capital)
            return Response(serializer.data)


class LocationSummaryAPI(APIView):
    """ 
    Widok pozwalający pobierać listę wszystkich elementów w danej lokalizacji 
    (idee, dyskusje, ankiety oraz blog). W zapytaniu podajemy pk interesującego
    nas miejsca, np:

    `/api-locations/contents/?pk=756135`

    Dodatkowe parametry:<br>
        `page`     - Numer strony do pobrania<br>
        `content`  - Tylko jeden typ zawartości (idea, news, poll, discussion)
                    Domyślna wartość to `all`<br>
        `time`     - Zakres czasowy (year, week, month, day). Domyślnie `any`<br>
        `haystack` - Fraza do wyszukania w tytułach<br>
        `category` - ID kategorii do przeszukania (jeżeli dotyczy)<br>
        `per_page` - Ilość elementów do pokazania na jednej stronie (max 100)<br>
    """
    paginate_by = 48
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):

        # Id lokacji, z której pobieramy wpisy
        try:
            location_pk = int(request.QUERY_PARAMS.get('pk'))
        except (ValueError, TypeError):
            location_pk = None

        # Numer strony do wyświetlenia
        try:
            page = int(request.QUERY_PARAMS.get('page'))
        except (ValueError, TypeError):
            page = 1

        # Ilość elementów na stronę
        try:
            per_page = int(request.QUERY_PARAMS.get('per_page'))
        except (ValueError, TypeError):
            per_page = self.paginate_by

        # Rodzaj typu zawartości (albo wszystkie)
        content = request.QUERY_PARAMS.get('content', 'all')

        # Przedział czasowy do przeszukania
        time = get_time_difference(request.QUERY_PARAMS.get('time', 'any'))

        # Wyszukiwanie po tytułach wpisów
        haystack = request.QUERY_PARAMS.get('haystack')

        # Wyszukiwanie poprzez ID kategorii (jeżeli dotyczy)
        try:
            category = int(request.QUERY_PARAMS.get('category'))
        except (ValueError, TypeError):
            category = None

        location = get_object_or_404(Location, pk=location_pk)
        content_objects = location.content_objects()

        if content != 'all':
            content_objects = [x for x in content_objects if x['type']==content]
        if time is not None:
            content_objects = [x for x in content_objects\
                                    if x['date_created'] >= time.isoformat()]
        if haystack:
            content_objects = [x for x in content_objects \
                                    if haystack.lower() in x['title'].lower()]
        if category is not None:
            content_objects = [x for x in content_objects if x['category']['pk']==category]

        # Opcje sortowania wyników (dotyczy konkretnych obiektów)
        sortby = self.request.QUERY_PARAMS.get('sortby')
        if sortby == 'title':
            content_objects = sort_by_locale(content_objects,
                            lambda x: x['title'], translation.get_language())
        elif sortby == 'oldest':
            content_objects.sort(key=lambda x: x['date_created'])
        elif sortby == 'newest':
            content_objects.sort(key=lambda x: x['date_created'], reversed=True)
        elif sortby == 'user':
            content_objects.sort(key=lambda x: x['creator']['name'].split(' ')[1])

        paginator = Paginator(content_objects, per_page)
        try:
            items = paginator.page(page)
        except EmptyPage:
            items = paginator.page(1)
        serializer = ContentPaginatedSerializer(items, context={'request': request})

        return Response(serializer.data)


class LocationFollowAPIView(APIView):
    """
    Wyjście REST na funkcję obserwowania lokalizacji. Generalnie wysyłamy tutaj
    POST z jednym parametrem - `pk` lokalizacji. Jeżeli użytkownik już obserwuje
    tę lokalizację, zostanie usunięty z listy obserwatorów i vice-versa.
    Za każdym razem w odpowiedzi otrzymujemy obiekt z wartością follow ustawioną
    na `true` lub `false` w zależności od faktycznego stanu po zmianie,tzn. jeżeli
    użytkownik zaczął obserwować lokalizację, otrzymamy coś takiego:
    
    ```{
        follow: true
    }```
    """
    permission_classes = (rest_permissions.IsAuthenticated,)

    def post(self, request):
        pk = request.DATA.get('pk', None)
        user = request.user
        context = {}
        if pk:
            location = get_object_or_404(Location, pk=pk)
            if not location.users.filter(pk=user.pk).exists():
                location.users.add(user)
                location.save()
                follow(user, location, actor_only = False)
                context['follow'] = True
            else:
                location.users.remove(user)
                location.save()
                unfollow(user, location)
                context['follow'] = False
        return Response(context)


class LocationAPIViewSet(viewsets.ModelViewSet):
    """
    REST view for mobile app. Provides a way to manage and add new locations.
    Możliwe jest wyszukanie konkretnego kraju na podstawie codu kraju (TYLKO
    lokacji powiązanej z krajem). W tym celu dodajemy parametr `code`, np:
    
    ```/api-locations/locations/?code=pl```
    
    W wyniku otrzymamy wówczas pojedynczy obiekt lokacji (w tym przypadku Polska)
    """
    model = Location
    serializer_class = SimpleLocationSerializer
    paginate_by = settings.LIST_PAGINATION_LIMIT
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)

    def list(self, request):
        code = request.QUERY_PARAMS.get('code', None)
        if code:
            location = get_object_or_404(Location, country__code=code.upper())
            serializer = self.serializer_class(location)
            serializer.data['followed'] = request.user in location.users.all()
            return Response(serializer.data)
        return super(LocationAPIViewSet, self).list(request)

    def retrieve(self, request, pk=None):
        if request.user.is_anonymous():
            return super(LocationAPIViewSet, self).retrieve(request, pk)
        location = get_object_or_404(Location, pk=pk)
        serializer = self.serializer_class(location)
        serializer.data['followed'] = request.user in location.users.all()
        return Response(serializer.data)


class CountryAPIViewSet(viewsets.ModelViewSet):
    """
    Tutaj kojarzymy kod państwa z GeoIP z naszym modelem lokalizacji. Model
    przechowuje informacje o startowej lokalizacji i powiększeniu mapy etc.
    Domyślnie prezentowana jest lista wszystkich państw w bazie. Umożliwia
    wyszukiwanie na podstawie country code (np. ?code=pl).
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    paginate_by = None
    permission_classes = (rest_permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        code = self.request.QUERY_PARAMS.get('code') or None
        if code:
            return Country.objects.filter(code=code.upper())
        return Country.objects.all()


class LocationActionsRestViewSet(viewsets.ViewSet):
    """
    Zwraca listę akcji powiązanych z miejscami. Wymagane jest podanie `pk`
    docelowej lokalizacji. Dodatkowo możemy przefiltrować listę pod względem
    typów zawartości obiektu (`action_object`), dodając parametr `ct` w 
    zapytaniu (id typu zawartości). Wyniki prezentowane są dokładnie w takiej
    samej formie jak dla actstreamów użytkowników.
    
    #### Przykład:
    ```/api-locations/actions/?pk=2&ct=28```
    
    Widok tylko do odczytu. Jeżeli nie podamy `pk` żadnej lokalizacji, otrzymamy
    w odpowiedzi pustą listę.
    """
    serializer_class = MyActionsSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    
    def get_queryset(self, pk=None, ct=None):
        from actstream.models import Action, model_stream
        if not pk: return []
        content_type = ContentType.objects.get_for_model(Location).pk
        stream = model_stream(Location).filter(target_content_type_id=content_type)
        try:
            location = Location.objects.get(pk=pk)
            stream = stream.filter(target_object_id=location.pk)
            ctid = ContentType.objects.get_for_model(Idea).pk
            vote_actions = [a.pk for a in Action.objects.all() if \
                            hasattr(a.action_object, 'location') and \
                            a.action_object.location==location]
            stream = stream | Action.objects.filter(pk__in=vote_actions)
        except Location.DoesNotExist:
            return []
        if ct:
            stream = stream.filter(action_object_content_type_id=ct)
        return stream
        
    def list(self, request):
        pk = request.QUERY_PARAMS.get('pk', None)
        ct = request.QUERY_PARAMS.get('ct', None)
        queryset = self.get_queryset(pk, ct)
        
        page = request.QUERY_PARAMS.get('page')
        paginator = Paginator(queryset, 48)
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:
            actions = paginator.page(1)
        except EmptyPage:
            actions = paginator.page(paginator.num_pages)

        serializer = PaginatedActionSerializer(actions, context={'request': request})
        return Response(serializer.data)


class LocationMapViewSet(viewsets.ModelViewSet):
    """
    Entry point dla aplikacji pobierającej nazwy lokalizacji. Napisany głównie
    z myślą o widgecie autocomplete w głównym widoku mapy. Wyszukując lokalizację
    podajemy fragment jej nazwy, np:
    
    ```/api-locations/markers/?term=awa```
    """
    queryset = Location.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    serializer_class = MapLocationSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = [u'get']

    def get_queryset(self):
        name = self.request.QUERY_PARAMS.get('term')
        if name is not None:
            return self.queryset.filter(name__icontains=name)
        return self.queryset


class SublocationAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Prosty widok umożliwiający pobranie listy lokalizacji z podstawowymi informacjami.
    Domyślnie prezentowana jest lista wszystkich lokalizacji. Do parametrów GET
    możemy dodać `pk` lokalizacji, której bezpośrednie "dzieci" chcemy pobrać, np.:
    
    ```/api-locations/sublocations/pk=1```
    """
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer
    permission_classes = (rest_permissions.AllowAny,)
    paginate_by = None

    def get_queryset(self):
        pk = self.request.QUERY_PARAMS.get('pk', None)
        if pk:
            try:
                location = Location.objects.get(pk=pk)
                key = "{}_{}_{}".format(location.slug,
                    translation.get_language(), 'sub')
                cached_qs = redis_cache.get(key, None)
                if cached_qs is None or not settings.USE_CACHE:
                    queryset = location.location_set.all()
                    redis_cache.set(key, queryset)
                else:
                    queryset = cached_qs
            except Location.DoesNotExist:
                queryset = Location.objects.all()
            return sort_by_locale(queryset, lambda x: x.__unicode__(),
                                    translation.get_language())
        return sort_by_locale(Location.objects.all(), lambda x: x.name,
                                translation.get_language())