# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from userspace import views, api

from bookmarks.views import BookmarkListView, BookmarkDeleteView

from rest import routers
router = routers.HybridRouter()
router.add_api_view('social_auths', url(r'^social_auths/$', api.SocialApiView.as_view(), name='social_auths'))
router.register('my-bookmarks', api.UserBookmarksViewSet, 'my-bookmarks')
router.add_api_view('contents', url(r'^contents/', api.UserSummaryAPI.as_view(), name='contents'))
router.add_api_view('api-token-auth', url(r'^api-token-auth/', api.obtain_auth_token, name='api-token-auth'))
router.add_api_view('activity', url(r'activity/$', api.ActivityAPIViewSet.as_view(), name='activity'))
router.add_api_view('follow', url(r'follow/$', api.UserFollowAPIView.as_view(), name='follow'))
router.add_api_view('locations', url(r'locations/$', api.UserFollowedLocationsAPI.as_view(), name='locations'))


urlpatterns = patterns('',
    url(r'relogin/(?P<username>[-\w.]+)/', views.ReloginView.as_view(), name='relogin'),
    url(r'^$', views.ProfileUpdateView.as_view(), name='index'),
    #url(r'facebook-friends/', views.FindFriendsView.as_view(), name='facebook-friends'),
    url(r'register_credentials_check', views.register_credentials_check, name='register_credentials_check'),
    url(r'twitter-email/', views.SetTwitterEmailView.as_view(), name='twitter_email'),
    url(r'login/', views.LoginFormView.as_view(), name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'active/', views.NewUserView.as_view(), name='active'),
    url(r'activate/(?P<activation_link>\w+)/', views.activate, name='activate'),
    url(r'register/', views.RegisterFormView.as_view(), name='register'),
    url(r'chpass/', views.chpass, name='chpass'),
    url(r'passreset/', views.pass_reset, name='passreset'),
    url(r'upload_avatar/', views.upload_avatar, name='upload_avatar'),
    #url(r'save_settings/', views.save_settings, name='save_settings'),
    url(r'locations/(?P<username>[-\w.]+)/', views.UserFollowedLocations.as_view(), name='locations'),
    url(r'background/', views.UserBackgroundView.as_view(), name='background'),
    url(r'dashboard/', views.UserActivityView.as_view(), name='dashboard'),
    url(r'(?P<username>[-\w.]+)/organizations/', views.UserNGOList.as_view(), name='organizations'),
    url(r'(?P<username>[-\w.]+)/$', views.UserProfileView.as_view(), name='profile'),
)
