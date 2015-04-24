# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import Http404
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
from actstream.actions import follow, unfollow

from .helpers import profile_activation, random_username, create_username
from .managers import SocialAuthManager
from .serializers import UserAuthSerializer, UserSerializer, SocialAuthSerializer, \
            BookmarkSerializer


def user_dict(user):
    """
    A helper useful in the 2 functions below. It presents a summary of
    information about the user in a delectable for the mobile application form.
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
    """ Login mobile app user with system email and password. """
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
    Registration/logging in of social media portals. This view uses Python Social
    Auth backend in order to facilitate integration. By default a list of all
    accounts is presented.

    Registration/loggin in through the API requires to specify one of the backends
    `twitter`, `facebook`, `google-plus`, `linkedin`.

    An example of such data for the query (server_response are the answers of the provider):

    <pre><code>{
        provider: 'facebook',
        uid: '8777323423',
        details: encodeURI(server_response_1),
        response: encodeURI(server_response_2)
    }</code></pre>

    By authorizing the user, in the POST parameter we give the server response
    of the authorizing service along with te name of the service and the uid of
    the user. The system check whether the accound with those parameters already
    exists and if necessary, creates a new one. In return we receive an object
    with and id and an authorization token of the user.
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
    """ A list of locations that the user is following. """
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        if request.user.is_anonymous():
            return Response([])
        locations = request.user.profile.followed_locations()
        serializer = SimpleLocationSerializer(locations, many=True)
        return Response(serializer.data)


class UserSummaryAPI(rest_views.APIView):
    """
    Content summary for user. Similar to summary for location, the difference
    is that we present content created by currently logged in user.
    """
    paginate_by = 48
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        if request.user.is_anonymous():
            raise Http404

        page = request.QUERY_PARAMS.get('page', 1)
        content = request.QUERY_PARAMS.get('content', 'all')
        time = request.QUERY_PARAMS.get('time', 'any')
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
    """ Allows the users to manipulate bookmarks. """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = BookmarkSerializer
    paginate_by = None

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class UserFollowAPIView(rest_views.APIView):
    """
    API view that manages the follow a user button. Only POST queries. It is
    necessary to give the ID of the user that we want to follow in the 'pk'
    request. It returns a true or false value depending on whether we start/stop
    to follow another unser .
    An example of such an answer:
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
    Managing a user list from the mobile application level. This view provides
    all CRUD operations on the user list.

    ### User creation:
    Required fields: *username*, *first_name*, *last_name*, *password*, *email*

    **WARNING**: This view does not use Django authorization policy (because
    it is impossible). It needs to be **CAREFULLY** thought over on how to
    implement this system in the production environment.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    paginate_by = None
    permission_classes = (rest_permissions.AllowAny,)


class UserAuthAPIViewSet(viewsets.ViewSet):
    """
    *Deprecated*: It is better to the the interface from the following address
    `/api-userspace/social_auth/`

    Here we send the provider's name and the uid user social auth in order
    to download the instance of the user in Django system. The data need to
    be send via get, if the user exists in the system, his/her serialized
    data will be returned, in the other case we will receive the answer "Forbidden"
    An example:

    ```/api-userspace/socials/?provider=google-plus?id=tester@gmail.com```

    **TODO**: It is worth to think about encripting this interface!!!
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
    A view that allows to easily check whether the given email address or
    the user name is already registered in the system.

    #### A sample query for an email address:

    ```/api-userspace/credentials/?email=tester@test.pl```

    ####  sample query for a user name:

    ```/api-userspace/credentials/?uname=tester```

    In both cases we receive in return a simple object with the property of
    'valid' set to 'true' or 'false'.
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
    Replacement for standard activity stream view. Displays actions for
    currently logged in user. If user is anonymous, it returns 404.
    """
    permission_classes = (rest_permissions.AllowAny,)

    def get(self, request):
        if request.user.is_anonymous():
            raise Http404
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
