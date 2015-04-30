# -*- coding: utf-8 -*-
import hashlib
import json
import os
import random
import sys

from PIL import Image
from datetime import datetime
from slugify import slugify

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic import View, DetailView, DeleteView, ListView,\
                                 FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView

from actstream import action
from rest_framework import viewsets
from rest_framework.response import Response

from comments.models import CustomComment
from locations.links import LINKS_MAP as links
from locations.models import Location
from places_core.helpers import TagFilter
from places_core.permissions import is_moderator
from rest.permissions import IsOwnerOrReadOnly
from userspace.models import UserProfile

from .forms import ContentGalleryForm, UserItemForm, \
                   SimpleItemForm, LocationItemForm, \
                   PictureUploadForm
from .models import ContentObjectGallery, ContentObjectPicture, \
                    LocationGalleryItem, UserGalleryItem
from .serializers import UserMediaSerializer


# Helper functions
# ------------------------------------------------------------------------------

def create_gallery(gallery_name):
    """
    Check if gallery folder exists and create new one if not.
    """
    filepath = os.path.join(settings.MEDIA_ROOT, gallery_name)
    thumb_path = os.path.join(filepath, 'thumbs')
    if not os.path.exists(filepath):
        try:
            os.makedirs(os.path.join(filepath, 'thumbs'))
            return True
        except IOError:
            return False
    return True


def create_gallery_thumbnail(gallery, filename):
    """
    Create thumbnail for given image in selected gallery.
    @param gallery  (string) Username or place slug
    @param filename (string) Image filename
    """
    filepath = os.path.join(settings.MEDIA_ROOT, gallery)
    thumb_path = filepath + '/thumbs/'

    for w, h in settings.THUMB_SIZES:
        size = w, h
        thumbfile = str(w) + 'x' + str(h) + '_' + filename
        thumbname = os.path.join(thumb_path + thumbfile)
        try:
            thumb = Image.open(filepath + '/' + filename)
            thumb.thumbnail(size, Image.ANTIALIAS)
            thumb.save(thumbname, 'JPEG')
        except IOError:
            return False
    return True


def gallery_item_name():
    """
    Creates name based on md5 sum of current date and time to avoid naming
    conflicts in files.
    """
    rand = random.randint(0, 10000)
    basename = hashlib.md5()
    basename.update(str(datetime.now().time) + str(rand))
    return basename.hexdigest() + '.jpg'


# API views
# ------------------------------------------------------------------------------

class UserGalleryAPIViewSet(viewsets.ModelViewSet):
    """
    Exit for the user gallery. In this case, the serializer is used only as
    a read only. The view takes care of creating the element in the data base
    and prepares all minatures. A logged in user can view his/her gallery here.
    Anonymous users don't have the permissions to this view and will get a 403
    in return.
    """
    queryset = UserGalleryItem.objects.all()
    serializer_class = UserMediaSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def list(self, request):
        if request.user.is_authenticated():
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True,
                                                context={'request':request})
            return Response(serializer.data)
        else:
            return HttpResponseForbidden()

    def create(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if not create_gallery(request.user.username):
            return Response({
                'success': False,
                'message': _("Cannot create gallery"),
                'level': 'danger',
            })

        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        image = Image.open(request.FILES.get('file'))
        filename = gallery_item_name()
        width, height = image.size
        if width > settings.IMAGE_MAX_SIZE[0] or height > settings.IMAGE_MAX_SIZE[1]:
            image.thumbnail(settings.IMAGE_MAX_SIZE)
        image.save(os.path.join(filepath, filename), "JPEG")
        create_gallery_thumbnail(username, filename)

        item = UserGalleryItem(
            user = request.user,
            picture_name = filename,
        )
        item.save()

        serializer = self.serializer_class(item, context={'request':request})

        return Response({
            'success': True,
            'message': _("File uploaded"),
            'level': 'success',
            'item': serializer.data,
        })

    def delete(self, request, pk=None):
        if not pk:
            return Response({
                'success': False,
                'level': 'danger',
                'message': _("No item ID provided")
            })

        item = get_object_or_404(UserGallerItem, pk=pk)

        try:
            item.delete()
        except Exception as ex:
            return Response({
                'success': False,
                'level': 'danger',
                'message': str(ex),
            })

        return Response({
                'success': True,
                'level': 'success',
                'message': _("Item deleted")
            })


# Static views - user gallery
# ------------------------------------------------------------------------------

class UserGalleryView(ListView):
    """ A list of images in the gallery of the user. """
    queryset = UserGalleryItem.objects.all()
    template_name = 'gallery/user-gallery.html'
    context_object_name = 'files'
    paginate_by = settings.USER_GALLERY_LIMIT

    def get_context_data(self, **kwargs):
        context = super(UserGalleryView, self).get_context_data(**kwargs)
        context['title'] = _("Gallery")
        return context

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = self.request.user

        return UserGalleryItem.objects.filter(user=user)


class UserGalleryCreateView(FormView):
    """ An upload of a new image to the gallery through the statistical form. """
    form_class = UserItemForm
    template_name = 'gallery/user-gallery-form.html'

    def get_context_data(self, **kwargs):
        context = super(UserGalleryCreateView, self).get_context_data(**kwargs)
        context['title'] = _("Add pictures")
        return context

    def form_valid(self, form, **kwargs):
        create_gallery(self.request.user.username)
        username = self.request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        image = Image.open(form.cleaned_data['image'])
        filename = gallery_item_name()
        width, height = image.size
        if width > settings.IMAGE_MAX_SIZE[0] or height > settings.IMAGE_MAX_SIZE[1]:
            image.thumbnail(settings.IMAGE_MAX_SIZE)
        image.save(os.path.join(filepath, filename), "JPEG")
        create_gallery_thumbnail(username, filename)

        item = UserGalleryItem(
            user = self.request.user,
            picture_name = filename,
            name = form.cleaned_data['name'],
            description = form.cleaned_data['description']
        )
        item.save()
        return redirect(reverse('gallery:index'))


class UserGalleryUpdateView(UpdateView):
    """ An edit of an image that is already in the gallery. """
    model = UserGalleryItem
    form_class = SimpleItemForm
    template_name = 'gallery/user-gallery-form.html'
    success_url = '/gallery/'

    def get_context_data(self, **kwargs):
        context = super(UserGalleryUpdateView, self).get_context_data(**kwargs)
        context['title'] = _("Edit picture data")
        return context

    def get(self, request, pk=None, slug=None):
        self.object = self.get_object()
        if request.user != self.object.user:
            return HttpResponseForbidden()
        return super(UserGalleryUpdateView, self).get(request)


class ImageView(View):
    """
    Edit photos. As of now, this view is not in use.
    """
    def get(self, request, pk):
        username = request.user.username
        item = get_object_or_404(UserGalleryItem, pk=pk)
        ctx = {
            'title': _("Edit image"),
            'href' : item.url(),
            'image': item,
        }
        return render(request, 'gallery/media-editor.html', ctx)

    def post(self, request, pk):
        """
        Save changes in image.
        """
        x = request.POST.get('x')
        y = request.POST.get('y')
        x2 = request.POST.get('x2')
        y2 = request.POST.get('y2')
        item = get_object_or_404(UserGalleryItem, pk=pk)
        filename = item.picture_name
        filepath = item.get_filepath()
        file = os.path.join(filepath, filename)
        box = (int(x), int(y), int(x2), int(y2))

        img = Image.open(file)
        img.crop(box).save(file)
        create_gallery_thumbnail(request.user.username, filename)

        return redirect(reverse('gallery:index'))


# Static views - location gallery
# ------------------------------------------------------------------------------

class LocationGalleryView(ListView):
    """ The main site of the location gallery. """
    queryset = LocationGalleryItem.objects.all()
    template_name = 'gallery/location-gallery.html'
    context_object_name = 'files'
    paginate_by = settings.PLACE_GALLERY_LIMIT

    def get_current_location(self):
        location = get_object_or_404(Location, slug=self.kwargs['slug'])
        return location

    def get_context_data(self, **kwargs):
        context = super(LocationGalleryView, self).get_context_data(**kwargs)
        context['title'] = _("Gallery")
        context['location'] = self.get_current_location()
        context['links'] = links['gallery']
        context['is_moderator'] = is_moderator(self.request.user, context['location'])
        return context

    def get_queryset(self):
        location = self.get_current_location()
        return LocationGalleryItem.objects.filter(location=location)


class LocationGalleryCreateView(FormView):
    """
    Allows to add new images to the gallery of a location.
    """
    form_class = LocationItemForm
    template_name = 'gallery/location-gallery-form.html'

    def get_initial(self):
        location = get_object_or_404(Location, slug=self.kwargs.get('slug'))
        return {
            'location': location,
        }

    def get_context_data(self, **kwargs):
        context = super(LocationGalleryCreateView, self).get_context_data(**kwargs)
        context['title'] = _("Add pictures")
        context['location'] = Location.objects.get(slug=self.kwargs['slug'])
        context['links'] = links['gallery']
        return context

    def form_valid(self, form, **kwargs):
        location = form.cleaned_data['location']
        username = location.slug
        create_gallery(username)
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        image = Image.open(form.cleaned_data['image'])
        filename = gallery_item_name()
        width, height = image.size
        if width > settings.IMAGE_MAX_SIZE[0] or height > settings.IMAGE_MAX_SIZE[1]:
            image.thumbnail(settings.IMAGE_MAX_SIZE)
        image.save(os.path.join(filepath, filename), "JPEG")
        create_gallery_thumbnail(username, filename)

        item = LocationGalleryItem(
            user = self.request.user,
            picture_name = filename,
            name = form.cleaned_data['name'],
            description = form.cleaned_data['description'],
            location = location
        )
        item.save()
        action.send(
            self.request.user,
            action_object = item,
            target = item.location,
            verb = _('uploaded')
        )
        self.request.user.profile.rank_pts += 2
        self.request.user.profile.save()
        return redirect(reverse('locations:gallery', kwargs={'slug':location.slug}))


class LocationGalleryUpdateView(UpdateView):
    """ Edition of an image that is already in the gallery. """
    model = LocationGalleryItem
    form_class = SimpleItemForm
    template_name = 'gallery/location-gallery-form.html'

    def get_context_data(self, **kwargs):
        context = super(LocationGalleryUpdateView, self).get_context_data(**kwargs)
        context['title'] = _("Edit picture data")
        context['location'] = self.object.location
        return context

    def get(self, request, pk=None, slug=None):
        self.object = self.get_object()
        if not request.user.is_superuser and request.user != self.object.user:
            return HttpResponseForbidden()
        return super(LocationGalleryUpdateView, self).get(request)


def location_gallery_delete(request, slug=None, pk=None):
    """
    A view that allows to delete images from the gallery. The 'pk' parameter is
    compulsory and when it is empty, an error will occur. The 'slug' parameter
    is here only to match the view in urlconf with the 'locations' application.
    """
    item = get_object_or_404(LocationGalleryItem, pk=pk)
    if request.user.is_superuser or is_moderator(request.user, item.location):
        item.delete()
        return redirect(
            reverse('locations:gallery',
            kwargs={'slug':item.location.slug})
        )
    else:
        return HttpResponseForbidden()


class PlacePictureView(DetailView):
    """
    Show single picture page with comments etc.
    """
    model = LocationGalleryItem
    template_name = 'gallery/picture-view.html'
    content_object_name = 'picture'

    def get_object(self):
        object = super(PlacePictureView, self).get_object()
        content_type = ContentType.objects.get_for_model(LocationGalleryItem)
        object.content_type = content_type.pk
        comment_set = CustomComment.objects.filter(
            content_type=content_type.pk
        )
        comment_set = comment_set.filter(object_pk=object.pk)
        object.comments = len(comment_set)
        return object

    def get_context_data(self, **kwargs):
        context = super(PlacePictureView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        context['title'] = self.object.name
        context['location'] = self.object.location
        context['picture'] = self.get_object()
        context['links'] = links['gallery']
        return context


class GalleryCreateView(CreateView):
    """
    Create new gallery - universal view. We expect user to be redirected
    with proper `ct` and `pk` parameters matching model for which gallery will
    be published. In other case stand-alone gallery will be created.
    """
    model = ContentObjectGallery
    form_class = ContentGalleryForm

    def get_initial(self):
        initial = super(GalleryCreateView, self).get_initial()
        try:
            pk = int(self.kwargs.get('pk'))
            ct = int(self.kwargs.get('ct'))
        except (TypeError, ValueError):
            # We assume that `published_in` sould be null
            return initial
        initial.update({'content_type': ct, 'object_id': pk, })
        return initial


class GalleryDeleteView(DeleteView):
    """ Delete gallery.
    """
    model = ContentObjectGallery


class GalleryDetailView(DetailView):
    """ Show single gallery, most often used for stand-alone galleries.
    """
    model = ContentObjectGallery


class PictureDeleteView(DeleteView):
    """ Delete single picture from gallery.
    """
    model = ContentObjectPicture

    def get_success_url(self):
        return self.object.gallery.get_absolute_url()


class PictureDetailView(DetailView):
    """ Show detailed info about selected gallery item.
    """
    model = ContentObjectPicture


class PictureUploadView(SingleObjectMixin, View):
    """ Universal view that allows us to upload picture to any gallery.
    """
    model = ContentObjectGallery
    template_name = 'gallery/picture_form.html'
    form_class = PictureUploadForm

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous():
            raise Http404
        self.object = self.get_object()
        return super(PictureUploadView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        return {'gallery': self.get_object(), }

    def get(self, request, **kwargs):
        context = super(PictureUploadView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(initial=self.get_initial())
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            return redirect(obj.get_absolute_url())
        if request.is_ajax():
            context = json.dumps(form.errors)
            return HttpResponse(context, content_type="application/json")
        context = super(PictureUploadView, self).get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
