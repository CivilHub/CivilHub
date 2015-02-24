# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from userspace import views

from bookmarks.views import BookmarkListView, BookmarkDeleteView

from rest import routers
router = routers.HybridRouter()
#router.add_api_view('social_auths', url(r'^social_auths/$', views.SocialApiView.as_view(), name='social_auths'))
#router.add_api_view('credentials', url(r'^credentials/$', views.CredentialCheckAPIView.as_view(), name='credentials'))
#router.register('users', views.UserAPIViewSet, 'users')
router.register('my-bookmarks', views.UserBookmarksViewSet, 'my-bookmarks')
#router.register('socials', views.UserAuthAPIViewSet, 'socials')
router.add_api_view('contents', url(r'^contents/', views.UserSummaryAPI.as_view(), name='contents'))
router.add_api_view('api-token-auth', url(r'^api-token-auth/', views.obtain_auth_token, name='api-token-auth'))
router.add_api_view('activity', url(r'activity/$', views.ActivityAPIViewSet.as_view(), name='activity'))
router.add_api_view('follow', url(r'follow/$', views.UserFollowAPIView.as_view(), name='follow'))
router.add_api_view('locations', url(r'locations/$', views.UserFollowedLocationsAPI.as_view(), name='locations'))


urlpatterns = patterns('',
    url(r'^$', views.ProfileUpdateView.as_view(), name='index'),
    url(r'register_credentials_check', views.register_credentials_check, name='register_credentials_check'),
    url(r'confirm-register/', views.confirm_registration, name='message_sent'),
    url(r'twitter-email/', views.SetTwitterEmailView.as_view(), name='twitter_email'),
    url(r'test/', views.test_view, name='test'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'active/(?P<lang>\w+)/', views.active, name='active'),
    url(r'activate/(?P<activation_link>\w+)/', views.activate, name='activate'),
    url(r'register/', views.register, name='register'),
    #url(r'passet/', views.passet, name='passet'),
    url(r'chpass/', views.chpass, name='chpass'),
    url(r'passreset/', views.pass_reset, name='passreset'),
    url(r'upload_avatar/', views.upload_avatar, name='upload_avatar'),
    url(r'save_settings/', views.save_settings, name='save_settings'),
    url(r'locations/(?P<pk>\d+)/', views.UserFollowedLocations.as_view(), name='locations'),
    #url(r'background/', views.change_background, name='background'),
    url(r'background/', views.UserBackgroundView.as_view(), name='background'),
    url(r'dashboard/', views.UserActivityView.as_view(), name='dashboard'),
    url(r'(?P<username>[-\w.]+)/$', views.profile, name='profile'),
)
