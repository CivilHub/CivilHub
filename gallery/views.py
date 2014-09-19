# -*- coding: utf-8 -*-
import os, json, sys, hashlib, random
from PIL import Image
from datetime import datetime
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.views.generic import View, DetailView, ListView, FormView, UpdateView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from easy_thumbnails.files import get_thumbnailer
from actstream import action
from userspace.models import UserProfile
from locations.models import Location
from locations.links import LINKS_MAP as links
from comments.models import CustomComment
from places_core.permissions import is_moderator
from places_core.helpers import TagFilter
from .models import LocationGalleryItem, UserGalleryItem
from .forms import UserItemForm, SimpleItemForm, LocationItemForm
from .serializers import UserMediaSerializer

from rest.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response

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
    Wyjście dla galerii użytkownika. W tym wypadku serializer stosowany jest
    tylko jako read only. Widok sam dba o utworzenie elementu w bazie danych
    i przygotowanie wszystkich miniaturek. Zalogowany użytkownik może tutaj
    przejrzeć swoją galerię. Anonimowi użytkownicy nie mają praw do tego widoku
    i dostaną w odpowiedzi 403.
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
    """ Lista zdjęć w galerii użytkownika. """
    queryset = UserGalleryItem.objects.all()
    template_name = 'gallery/user-gallery.html'
    context_object_name = 'files'
    paginate_by = settings.USER_GALLERY_LIMIT

    def get_context_data(self, **kwargs):
        context = super(UserGalleryView, self).get_context_data(**kwargs)
        context['title'] = _("Gallery")
        return context

    def get_queryset(self):
        return UserGalleryItem.objects.filter(user=self.request.user)


class UserGalleryCreateView(FormView):
    """ Upload nowego zdjęcia do galerii przez formularz statyczny. """
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
    """ Edycja zdjęcia, które znajduje się już w galerii. """
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
    Edit photos. W tym momencie ten widok nie jest wykorzystywany.
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
    """ Główna strona galerii dla lokalizacji. """
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
    Dodawanie nowych zdjęć do galerii miejsca.
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
        return redirect(reverse('locations:gallery', kwargs={'slug':location.slug}))


def location_gallery_delete(request, slug=None, pk=None):
    """
    Widok umożliwiający usuwanie obrazów z galerii. Parametr `pk` jest wymagany
    i jego brak zaskutkuje błędem. Parametr `slug` jest tylko po to, żeby
    wpasować widok w urlconf z aplikacji `locations`.
    Prawo do usuwania obrazów mają tylko superadmini oraz moderatorzy lokalizacji.
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
