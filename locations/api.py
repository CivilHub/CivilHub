# -*- coding: utf-8 -*-
from ipware.ip import get_ip

from django.conf import settings
from django.http import Http404
from django.utils import translation
from django.shortcuts import get_object_or_404
from django.core import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geoip import GeoIP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from actstream.actions import follow, unfollow
from actstream.models import following
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
                         MapLocationSerializer, \
                         AutocompleteLocationSeraializer
from rest.serializers import MyActionsSerializer, PaginatedActionSerializer

redis_cache = cache.get_cache('default')


class LocationSearchAPI(APIView):
    """
    Provides simple autocomplete functionality.
    """
    permission_classes = (rest_permissions.AllowAny, )
    serializer_class = AutocompleteLocationSeraializer

    def get(self, request, **kwargs):
        q = request.QUERY_PARAMS.get('term', '')
        if len(q) < 4:
            raise Http404
        qs = Location.objects.filter(name__icontains=q.lower())
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class CapitalAPI(APIView):
    """
    A view that searches for a capital of a country most suitable for the location
    of the current user. You don't have to pass in any parameters.
    """
    permission_classes = (rest_permissions.AllowAny, )

    def get(self, request):
        code = GeoIP().country(get_ip(self.request))\
                      .get('country_code', settings.DEFAULT_COUNTRY_CODE)
        country = None
        try:
            country = Country.objects.get(code=code)
        except Country.DoesNotExist:
            country = get_object_or_404(Country,
                                        code=settings.DEFAULT_COUNTRY_CODE)
        capital = country.get_capital()
        if capital is not None:
            serializer = LocationListSerializer(capital)
            return Response(serializer.data)


class LocationSummaryAPI(APIView):
    """
    A view that allows to download a list of all elements in a given location
    (idea, discussion, poll, news). In the query we give the pk of the location
    we are interested in, e.g:

        `/api-locations/contents/?pk=756135`

    Additional parameters:<br>
        `page`     - number of page after download<br>
        `content`  - Only one type of content (idea, news, poll, discussion)
                    The default value is 'all'<br>
        `time`     - Time scope (year, week, month, day). By default: `any`<br>
        `haystack` - The phrase to be searched for in the titles<br>
        `category` - ID of the category that we want to look in (if applicable)<br>
        `per_page` - Number of elements to show on one page (max 100)<br>
    """
    paginate_by = 48
    permission_classes = (rest_permissions.AllowAny, )

    def get(self, request):

        # Location Id from which we gather entries
        try:
            location_pk = int(request.QUERY_PARAMS.get('pk'))
        except (ValueError, TypeError):
            location_pk = None

        # Number of page that is going to be displayed
        try:
            page = int(request.QUERY_PARAMS.get('page'))
        except (ValueError, TypeError):
            page = 1

        # Number of elements on the site
        try:
            per_page = int(request.QUERY_PARAMS.get('per_page'))
        except (ValueError, TypeError):
            per_page = self.paginate_by

        # Type of content (or all)
        content = request.QUERY_PARAMS.get('content', 'all')

        # Time duration for search
        time = get_time_difference(request.QUERY_PARAMS.get('time', 'any'))

        # Search by entries' titles
        haystack = request.QUERY_PARAMS.get('haystack')

        # Search through category ID (if applicable)
        try:
            category = int(request.QUERY_PARAMS.get('category'))
        except (ValueError, TypeError):
            category = None

        location = get_object_or_404(Location, pk=location_pk)
        content_objects = location.content_objects()

        if content != 'all':
            content_objects = [x for x in content_objects
                               if x['type'] == content]
        if time is not None:
            content_objects = [x for x in content_objects\
                                    if x['date_created'] >= time.isoformat()]
        if haystack:
            content_objects = [x for x in content_objects \
                                    if haystack.lower() in x['title'].lower()]
        if category is not None:
            content_objects = [x for x in content_objects
                               if x['category']['pk'] == category]

        # Sort results option (Opcje sortowania wyników (is applicable to concrete objects)
        sortby = self.request.QUERY_PARAMS.get('sortby')
        if sortby == 'title':
            content_objects = sort_by_locale(content_objects,
                                             lambda x: x['title'],
                                             translation.get_language())
        elif sortby == 'oldest':
            content_objects.sort(key=lambda x: x['date_created'])
        elif sortby == 'newest':
            content_objects.sort(key=lambda x: x['date_created'],
                                 reversed=True)
        elif sortby == 'user':
            content_objects.sort(
                key=lambda x: x['creator']['name'].split(' ')[1])

        paginator = Paginator(content_objects, per_page)
        try:
            items = paginator.page(page)
        except EmptyPage:
            items = paginator.page(1)
        serializer = ContentPaginatedSerializer(items,
                                                context={'request': request})

        return Response(serializer.data)


class LocationFollowAPI(APIView):
    """
    Follow/unfollow location. GET request to find out that current user already
    follow location passed with `pk` query parameter. Perform POST request to
    toggle follow/unfollow state.
    """
    permission_classes = (rest_permissions.IsAuthenticated, )
    location = None

    def _get_location(self):
        if self.location is not None:
            return self.location
        try:
            location_id = int(self.request.QUERY_PARAMS.get('pk'))
        except (TypeError, ValueError):
            raise Http404
        self.location = get_object_or_404(Location, pk=location_id)
        return self.location

    def get(self, request, **kwargs):
        self.location = self._get_location()
        return Response(
            {'following': self.location in following(request.user), })

    def post(self, request, **kwargs):
        user = request.user
        self.location = self._get_location()
        if self.location in following(user):
            unfollow(user, self.location)
            self.location.users.remove(user)
            msg = _(u"You stopped following")
        else:
            follow(user, self.location, actor_only=False)
            self.location.users.add(user)
            msg = _(u"You are following")
        return Response(
            {'following': self.location in following(user),
             'message': msg, })


class LocationAPIViewSet(viewsets.ModelViewSet):
    """
    Rest view for mobile app. Provides a way to manage and add new locations.
    It is possible to search for a certain country on the basis of the country's
    code (ONLY a location bound with the country). To do this, we add a parameter
    'code', e.g.

    ```/api-locations/locations/?code=pl```

    In the result we will receive a single location object (here, Poland)
    """
    model = Location
    serializer_class = SimpleLocationSerializer
    paginate_by = settings.LIST_PAGINATION_LIMIT
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly, IsOwnerOrReadOnly, )

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
    Here we "connect" the country kode with the GeoIP with our location's model.
    The model stores information about the starting location and the zoom of
    the map etc. By default a list of all countries in the database is presented.
    It allows to search by country code (e.g. ?code=pl)
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    paginate_by = None
    permission_classes = (
        rest_permissions.DjangoModelPermissionsOrAnonReadOnly, )

    def get_queryset(self):
        code = self.request.QUERY_PARAMS.get('code') or None
        if code:
            return Country.objects.filter(code=code.upper())
        return Country.objects.all()


class LocationActionsRestViewSet(viewsets.ViewSet):
    """
    Returns a list of action connected with the places. Providing the 'pk'
    of the given location is required. We can additionally filter the list by
    the object's conent ('action_object'), by adding the parameter 'ct' in
    the query(id type of the contnet). The results are presented in the exact same
    form as for users actstreams.

    #### Przykład:
    ```/api-locations/actions/?pk=2&ct=28```

    Read-only view. If we won't give a 'pk' of any location, we will receive an
    empty list.
    """
    serializer_class = MyActionsSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, )

    def get_queryset(self, pk=None, ct=None):
        from actstream.models import Action, model_stream
        if not pk: return []
        content_type = ContentType.objects.get_for_model(Location).pk
        stream = model_stream(Location).filter(
            target_content_type_id=content_type)
        try:
            location = Location.objects.get(pk=pk)
            stream = stream.filter(target_object_id=location.pk)
            ctid = ContentType.objects.get_for_model(Idea).pk
            vote_actions = [a.pk for a in Action.objects.all() if \
                            hasattr(a.action_object, 'location') and \
                            a.action_object.location == location]
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

        serializer = PaginatedActionSerializer(actions,
                                               context={'request': request})
        return Response(serializer.data)


class LocationMapViewSet(viewsets.ModelViewSet):
    """
    An entry point for the application that downloads the names of the locations.
    Written mainly with the autocomplete widget in the main map view in mind.
    Searching for a location we give part of its name, e.g.:

    ```/api-locations/markers/?term=awa```
    """
    queryset = Location.objects.exclude(latitude__isnull=True).exclude(
        longitude__isnull=True)
    serializer_class = MapLocationSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly, )
    http_method_names = [u'get']

    def get_queryset(self):
        name = self.request.QUERY_PARAMS.get('term')
        if name is not None:
            return self.queryset.filter(name__icontains=name)
        return self.queryset


class SublocationAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get sublocations in location with provided ID, for example:

    ```/api-locations/sublocations/pk=1```
    """
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer
    permission_classes = (rest_permissions.AllowAny, )
    paginate_by = None

    def get_queryset(self):
        try:
            pk = int(self.request.QUERY_PARAMS.get('pk'))
        except (ValueError, UnicodeError):
            raise Http404
        location = get_object_or_404(Location, pk=pk)
        key = "{}_{}_sub".format(location.slug, translation.get_language())
        queryset = redis_cache.get(key)
        if queryset is None:
            queryset = location.location_set.all()
            redis_cache.set(key, queryset)
        return sort_by_locale(queryset, lambda x: x.name)
