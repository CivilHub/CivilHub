# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from gallery.actions import created_gallery, uploaded_picture
from gallery.forms import PictureUpdateForm
from gallery.models import ContentObjectGallery, ContentObjectPicture
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator

from ..forms import ProjectGalleryForm, ProjectPictureForm
from ..models import SocialProject
from ..permissions import check_access


def get_gallery(project, gallery_id):
    """ Handy shortcut to get gallery object and validate id input.
    """
    try:
        gallery_id = int(gallery_id)
    except (TypeError, ValueError):
        raise Http404
    try:
        return ContentObjectGallery.objects.for_object(project).get(pk=gallery_id)
    except ContentObjectGallery.DoesNotExist:
        raise Http404


class ProjectGalleryMixin(SingleObjectMixin):
    """ Provides common context variables for gallery subpages.
    """
    model = SocialProject

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        user = self.request.user
        context = super(ProjectGalleryMixin, self).get_context_data(**kwargs)
        context.update({
            'location': self.object.location,
            'is_moderator': is_moderator(user, self.object.location),
            'project_access': check_access(self.object, user),
            'gallery_access': user in self.object.participants.all(),
        })
        return context


class GalleryAccessMixin(LoginRequiredMixin, ProjectGalleryMixin):
    """ Extends above for update and create views.
    """

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user in self.object.participants.all():
            raise PermissionDenied
        return super(GalleryAccessMixin, self).dispatch(*args, **kwargs)


class ProjectGalleryList(ProjectGalleryMixin, View):
    """ List all gallery albums for this project.
    """
    template_name = 'projects/gallery_list.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super(ProjectGalleryList, self).get_context_data()
        context['object_list'] = ContentObjectGallery.objects.for_object(
            self.object)
        return render(request, self.template_name, context)


class ProjectGalleryPreview(ProjectGalleryMixin, View):
    """ List all pictures in single gallery for this project.
    """
    template_name = 'projects/gallery_detail.html'
    paginate_by = 25

    def get(self, request, **kwargs):
        self.object = self.get_object()
        gallery = get_gallery(self.object, self.kwargs.get('gallery_pk'))
        page = request.GET.get('page', 1)
        paginator = Paginator(gallery.pictures.all(), self.paginate_by)
        try:
            pictures = paginator.page(page)
        except PageNotAnInteger:
            pictures = paginator.page(1)
        except EmptyPage:
            pictures = paginator.page(paginator.num_pages)
        context = super(ProjectGalleryPreview, self).get_context_data(**kwargs)
        context.update({
            'gallery': gallery,
            'page_obj': pictures,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
        })
        return render(request, self.template_name, context)


class ProjectGalleryCreate(GalleryAccessMixin, View):
    """ Create new gallery for selected project.
    """
    template_name = 'projects/gallery_form.html'
    form_class = ProjectGalleryForm

    def get(self, request, **kwargs):
        context = super(ProjectGalleryCreate, self).get_context_data(**kwargs)
        context['form'] = self.form_class(initial={
            'content_type': ContentType.objects.get_for_model(SocialProject),
            'object_id': self.object.pk,
        })
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            gallery = form.save()
            created_gallery(request.user, gallery)
        return redirect(reverse('projects:gallery-list',
                                kwargs={'slug': self.object.slug, }))


class ProjectGalleryDelete(GalleryAccessMixin, View):
    """ Access to project is more important than gallery permissions.
    """
    def post(self, request, **kwargs):
        self.object = self.get_object()
        gallery = get_gallery(self.object, self.kwargs.get('gallery_pk'))
        if not check_access(self.object, request.user):
            raise PermissionDenied
        gallery.delete()
        messages.add_message(request, messages.SUCCESS,
            _(u"Gallery has been deleted"))
        return redirect(reverse('projects:gallery-list',
            kwargs={'slug': self.object.slug, }))


class ProjectPictureUpload(GalleryAccessMixin, View):
    """ Upload new picture to selected gallery.
    """
    template_name = 'projects/picture_form.html'
    form_class = ProjectPictureForm
    gallery = None

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        self.gallery = get_gallery(self.object, kwargs.get('gallery_pk'))
        return super(ProjectPictureUpload, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectPictureUpload, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)
        obj = form.save(commit=False)
        obj.gallery = self.gallery
        obj.uploaded_by = self.request.user
        obj.save()
        uploaded_picture(obj)
        return redirect(reverse('projects:gallery-preview', kwargs={
            'slug': self.object.slug,
            'gallery_pk': self.gallery.pk,
        }))


class ProjectPictureUpdate(GalleryAccessMixin, View):
    """ Update name and description of uploaded picture.
    """
    template_name = 'projects/picture_form.html'
    form_class = PictureUpdateForm
    instance = None

    def get_instance(self):
        if self.instance is not None:
            return instance
        try:
            pk = int(self.kwargs.get('picture_pk'))
        except (TypeError, ValueError):
            raise Http404
        self.instance = get_object_or_404(ContentObjectPicture, pk=pk)
        return self.instance

    def get(self, request, **kwargs):
        context = super(ProjectPictureUpdate, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_instance())
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, instance=self.get_instance())
        if not form.is_valid():
            context = super(ProjectPictureUpdate, self).get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)
        obj = form.save()
        return redirect(self.instance.get_absolute_url())


class ProjectPictureView(ProjectGalleryMixin, View):
    """ Single picture detail view.
    """
    template_name = 'projects/picture_detail.html'

    def get(self, request, **kwargs):
        try:
            picture_id = int(self.kwargs.get('picture_pk'))
        except (TypeError, ValueError):
            raise Http404
        context = super(ProjectPictureView, self).get_context_data(**kwargs)
        context['picture'] = get_object_or_404(ContentObjectPicture, pk=picture_id)
        return render(request, self.template_name, context)
