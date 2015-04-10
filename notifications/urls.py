from django.conf.urls import patterns, url

from rest.routers import HybridRouter

import api
import views

router = HybridRouter()
router.register('list', api.NotificationViewSet, 'list')
router.add_api_view('mark', url(r'^mark/', api.NotificationMarkView.as_view(), name='mark'))
router.add_api_view('count', url(r'^count/', api.NewNotifications.as_view(), name='count'))

urlpatterns = patterns('',
    url('^notifications/(?P<pk>\d+)/', views.NotificationView.as_view(), name="notify-detail"),
    url('^notifications/', views.NotificationList.as_view(), name="notify-list"),
)
