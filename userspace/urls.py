# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from userspace import views

from rest import routers
router = routers.HybridRouter()
#router.add_api_view('social_auths', url(r'^social_auths/$', views.SocialApiView.as_view(), name='social_auths'))
#router.add_api_view('credentials', url(r'^credentials/$', views.CredentialCheckAPIView.as_view(), name='credentials'))
#router.register('users', views.UserAPIViewSet, 'users')
router.register('bookmarks', views.BookmarkAPIViewSet, 'bookmarks')
#router.register('socials', views.UserAuthAPIViewSet, 'socials')


urlpatterns = patterns('',
    url(r'^$', views.ProfileUpdateView.as_view(), name='index'),
    url(r'confirm-register/', views.confirm_registration, name='message_sent'),
    url(r'twitter-email/', views.SetTwitterEmailView.as_view(), name='twitter_email'),
    url(r'test/', views.test_view, name='test'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'active/(?P<lang>\w+)/', views.active, name='active'),
    url(r'activate/(?P<activation_link>\w+)/', views.activate, name='activate'),
    url(r'register/', views.register, name='register'),
    url(r'passet/', views.passet, name='passet'),
    url(r'chpass/', views.chpass, name='chpass'),
    url(r'passreset/', views.pass_reset, name='passreset'),
    url(r'upload_avatar/', views.upload_avatar, name='upload_avatar'),
    url(r'save_settings/', views.save_settings, name='save_settings'),
    url(r'my_bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    url(r'locations/(?P<pk>\d+)/', views.UserFollowedLocations.as_view(), name='locations'),
    url(r'background/', views.change_background, name='background'),
    url(r'(?P<username>\w+)/$', views.profile, name='profile'),
)
