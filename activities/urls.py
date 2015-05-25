from django.conf.urls import url

from rest.routers import HybridRouter

import views

router = HybridRouter()

router.register('actstream', views.ActivityViewSet, 'actstream')
router.add_api_view('follow', url(r'^follow/', views.FollowObjectView.as_view(), name='follow'))
