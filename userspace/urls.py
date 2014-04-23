from django.conf.urls import url
from userspace import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'register/', views.register, name='register'),
]