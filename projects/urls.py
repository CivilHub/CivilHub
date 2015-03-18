from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
	url(r'^discussions/(?P<pk>\d+)/delete/', views.ProjectForumDeleteView.as_view(), name="discussion_delete"),
	url(r'^(?P<slug>[\w-]+)/background/', views.ProjectBackgroundView.as_view(), name="background"),
	url(r'^(?P<project_slug>[\w-]+)/discussions/create/', views.ProjectForumCreateView.as_view(), name="discussion_create"),
	url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<pk>\d+)/', views.ProjectForumAnswerUpdateView.as_view(), name="entry_update"),
	url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<discussion_slug>[\w-]+)/update/', views.ProjectForumUpdateView.as_view(), name="discussion_update"),
	url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<discussion_slug>[\w-]+)/entry/', views.ProjectForumAnswerCreateView.as_view(), name="create_entry"),
	url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<discussion_slug>[\w-]+)/', views.ProjectForumDetailView.as_view(), name="discussion"),
	url(r'^(?P<project_slug>[\w-]+)/discussions/', views.ProjectForumListView.as_view(), name="discussions"),
	url(r'^change_order/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<direction>[\w-]+)/', views.set_element_order, name='change_order'),
	url(r'^toggle_task/(?P<pk>\d+)/', views.toggle_task_state, name="toggle_task"),
)
