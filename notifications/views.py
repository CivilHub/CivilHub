# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView

from places_core.mixins import LoginRequiredMixin

from .models import Notification


class NotificationList(LoginRequiredMixin, ListView):
    """
    List all notifications for currently logged in user.
    """
    model = Notification
    paginate_by = 25

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationView(LoginRequiredMixin, DetailView):
    """
    Show single notification and mark it as read.
    """
    model = Notification

    def get_object(self):
        """ Make sure that only owner can mark notification as read. """
        self.object = super(NotificationView, self).get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied
        self.object.read()
        return self.object
