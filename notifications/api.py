# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer, NotificationSimpleSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This is the place where we can get notifications
    for currently logged in user.
    """
    model = Notification
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 10

    def get_queryset(self):
        return super(NotificationViewSet, self).get_queryset()\
            .filter(user=self.request.user)

    def retrieve(self, request, pk=None):
        """
        Be sure to mark this object as read.
        """
        obj = self.get_object()
        obj.read()
        return super(NotificationViewSet, self).retrieve(request, pk)


class NotificationMarkView(APIView):
    """
    Mark users notifications as read. You can pass pk to mark selected notify
    or mark them all at once as post parameter. Only POST requests.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        pk = request.POST.get('pk')
        if pk is not None:
            obj = get_object_or_404(Notification, pk=pk)
            obj.read()
            return Response({
                'success': True,
                'checked_at': obj.checked_at,
            })
        qs = Notification.objects.unread_for_user(self.request.user)
        for notify in qs:
            notify.read()
        serializer = NotificationSerializer(qs, many=True)
        return Response({
            'success': True,
            'count': len(qs),
            'notifications': serializer.data,
        })


class NewNotifications(APIView):
    """ Count new notifications for currently logged in user. """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({
            'count': Notification.objects.count_unread_for_user(self.request.user)
        })
