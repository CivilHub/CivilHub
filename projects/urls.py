from django.conf.urls import patterns, include, url

from views import base, forum, documents, galleries

urlpatterns = patterns('',
    url(r'^discussions/(?P<pk>\d+)/delete/', forum.ProjectForumDeleteView.as_view(), name="discussion_delete"),
    url(r'^(?P<project_slug>[\w-]+)/organizations/add/', base.AddProjectToNGO.as_view(), name="organization_add"),
    url(r'^(?P<slug>[\w-]+)/picture/(?P<picture_pk>\d+)/update/', galleries.ProjectPictureUpdate.as_view(), name="picture-update"),
    url(r'^(?P<slug>[\w-]+)/picture/(?P<picture_pk>\d+)/', galleries.ProjectPictureView.as_view(), name="picture-detail"),
    url(r'^(?P<slug>[\w-]+)/galleries/(?P<gallery_pk>\d+)delete/', galleries.ProjectGalleryDelete.as_view(), name="gallery-delete"),
    url(r'^(?P<slug>[\w-]+)/galleries/(?P<gallery_pk>\d+)/upload/', galleries.ProjectPictureUpload.as_view(), name="gallery-upload"),
    url(r'^(?P<slug>[\w-]+)/galleries/(?P<gallery_pk>\d+)/', galleries.ProjectGalleryPreview.as_view(), name="gallery-preview"),
    url(r'^(?P<slug>[\w-]+)/galleries/create/', galleries.ProjectGalleryCreate.as_view(), name="gallery-create"),
    url(r'^(?P<slug>[\w-]+)/galleries/', galleries.ProjectGalleryList.as_view(), name="gallery-list"),
    url(r'^(?P<slug>[\w-]+)/background/', base.ProjectBackgroundView.as_view(), name="background"),
    url(r'^(?P<slug>[\w-]+)/documents/(?P<document_slug>[\w-]+)/', documents.ProjectDocumentPreview.as_view(), name="document"),
    url(r'^(?P<slug>[\w-]+)/documents/', documents.ProjectDocumentsList.as_view(), name="documents"),
    url(r'^(?P<project_slug>[\w-]+)/discussions/create/', forum.ProjectForumCreateView.as_view(), name="discussion_create"),
    url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<pk>\d+)/', forum.ProjectForumAnswerUpdateView.as_view(), name="entry_update"),
    url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<discussion_slug>[\w-]+)/update/', forum.ProjectForumUpdateView.as_view(), name="discussion_update"),
    url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<discussion_slug>[\w-]+)/entry/', forum.ProjectForumAnswerCreateView.as_view(), name="create_entry"),
    url(r'^(?P<project_slug>[\w-]+)/discussions/(?P<discussion_slug>[\w-]+)/', forum.ProjectForumDetailView.as_view(), name="discussion"),
    url(r'^(?P<project_slug>[\w-]+)/discussions/', forum.ProjectForumListView.as_view(), name="discussions"),
    url(r'^change_order/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<direction>[\w-]+)/', base.set_element_order, name='change_order'),
    url(r'^toggle_task/(?P<pk>\d+)/', base.toggle_task_state, name="toggle_task"),
)
