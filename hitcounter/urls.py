from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^trigger-hit/(?P<ct>\d+)/(?P<pk>\d+)/', views.visit_view, name='visit-counter'),
)
