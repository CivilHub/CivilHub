from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
	url(r'^change_order/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<direction>[\w-]+)/', views.set_element_order, name='change_order'),
	url(r'^toggle_task/(?P<pk>\d+)/', views.toggle_task_state, name="toggle_task"),
)
