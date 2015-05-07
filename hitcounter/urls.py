from django.conf.urls import patterns, url

from rest_framework import routers

from rest.routers import HybridRouter

import api
import views

router = HybridRouter()
router.add_api_view('hot-box', url(r'^hot-box/', api.HotBoxAPIView.as_view(), name='hot-box'))

urlpatterns = patterns('',
    url(r'^trigger-hit/(?P<ct>\d+)/(?P<pk>\d+)/', views.visit_view, name='visit-counter'),
)
