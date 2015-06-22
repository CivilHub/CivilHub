from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.VisitorsMainView.as_view(), name="index"),
    url(r'^details/(?P<pk>\d+)/', views.GeoDetailsView.as_view(), name="details"),
)
