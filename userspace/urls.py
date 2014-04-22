from django.conf.urls import url
from userspace import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]