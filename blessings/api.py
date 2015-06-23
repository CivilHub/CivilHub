# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from rest_framework import permissions, views, viewsets
from rest_framework.response import Response

from rest.permissions import IsOwnerOrReadOnly

from .models import Blessing, bless
from .serializers import BlessSerializer, BlessDetailSerializer


class BlessViewSet(viewsets.ModelViewSet):
    """ Basic API entry for recommendations.
    """
    model = Blessing
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BlessDetailSerializer
        else:
            return BlessSerializer

    def pre_save(self, obj):
        obj.user = self.request.user


class BlessAPIView(views.APIView):
    """ Registered users may bless or curse content here.
        Send post to trigger change for request user.
    """
    serializer_class = BlessSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        try:
            ct = int(self.request.DATA.get('ct'))
            pk = int(self.request.DATA.get('pk'))
        except (TypeError, ValueError, ):
            raise Http404
        content_type = get_object_or_404(ContentType, pk=ct)
        try:
            self.object = content_type.get_object_for_this_type(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return self.object

    def post(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.user.is_anonymous():
            raise Http404
        data = bless(self.request.user, self.object)
        message = ""
        if data['last'] is not None:
            if data['last'].user == request.user:
                message = _("You") + " "
            else:
                message = '<a href="{}">{}</a> '.format(
                    data['last'].user.profile.get_absolute_url(),
                    data['last'].user.get_full_name())
            data['last'] = BlessDetailSerializer(data['last']).data
        if data['count'] > 1:
            message += _('and %d others recommended this' % (data['count']-1))
        elif data['count'] > 0:
            message += _("recommended this")
        data['message'] = message
        return Response(data)
