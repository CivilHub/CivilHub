from django.conf.urls import patterns, url
from .views import BookmarkListView, BookmarkCreateView, BookmarkDeleteView


urlpatterns = patterns('',
    url(r'^$', BookmarkListView.as_view(), name="bookmarks-list"),
    url(r'^create/', BookmarkCreateView.as_view(), name="bookmarks-create"),
    url(r'^delete/(?P<pk>\d+)/', BookmarkDeleteView.as_view(), name="bookmarks-delete"),
)
