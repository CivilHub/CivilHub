from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^pad/create/', views.CreatePadView.as_view(), name="pad-create"),
    url(r'^pad/update/(?P<pk>\d+)/', views.UpdatePadView.as_view(), name="pad-update"),
    url(r'^pad/edit/(?P<pk>\d+)/', views.EtherPadEditView.as_view(), name="pad-collaborate"),
    url(r'^pad/delete/(?P<pk>\d+)/', views.DeletePadView.as_view(), name="pad-remove"),
    url(r'^pad/download/(?P<pk>\d+)/', views.ServePadView.as_view(), name="pad-download"),
    url(r'^pads/(?P<group_id>\d+)/', views.PadListView.as_view(), name="pad-group-index"),
    url(r'^pad/(?P<slug>[\w-]+)/', views.PadExternalView.as_view(), name="pad-detail"),
    url(r'^pads/', views.PadListView.as_view(), name="pad-index"),
)
