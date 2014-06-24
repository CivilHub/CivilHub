# -*- coding: utf-8 -*-
import os, json, sys, hashlib, random
from PIL import Image
from datetime import datetime
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from easy_thumbnails.files import get_thumbnailer
from userspace.models import UserProfile
from locations.models import Location
from .models import LocationGalleryItem, UserGalleryItem


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


class ImageView(View):
    """
    Edit photos.
    """
    def get(self, request, filename):
        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        filehref = settings.MEDIA_URL + username + '/'
        if not os.path.exists(os.path.join(filepath, filename)):
            raise Http404
        ctx = {
            'title': _("Edit image"),
            'imgpath': filehref,
            'image': filename,
        }
        return render(request, 'gallery/media-editor.html', ctx)

    def post(self, request, filename):
        """
        Save changes in image.
        """
        x = request.POST.get('x')
        y = request.POST.get('y')
        x2 = request.POST.get('x2')
        y2 = request.POST.get('y2')
        filename = request.POST.get('filename')
        filepath = os.path.join(settings.MEDIA_ROOT, request.user.username)
        file = os.path.join(filepath, filename)
        box = (int(x), int(y), int(x2), int(y2))

        img = Image.open(file)
        img.crop(box).save(file)
        create_gallery_thumbnail(request.user.username, filename)

        return redirect(reverse('gallery:index'))


class GalleryView(View):
    """
    Generic gallery view class.
    """
    def get(self, request, slug=None):
        username = slug if slug else request.user.username
        template = 'gallery/media-form.html' if slug else 'userspace/gallery.html'
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        filehref = settings.MEDIA_URL + username + '/'
        files = []
        if not create_gallery(username):
            raise IOError
        for file in os.listdir(filepath):
            if not os.path.isdir(os.path.join(filepath, file)):
                files.append(str(file))
        if request.is_ajax():
            return HttpResponse(json.dumps({
                'href': filehref,
                'files': sorted(files),
            }))
        else:
            ctx = {
                'href': filehref,
                'title': _("Media gallery"),
                'files': sorted(files),
            }
            if slug:
                ctx['location'] = Location.objects.get(slug=slug)
            return render(request, template, ctx)

    def post(self, request, slug=None):
        username = slug if slug else request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        if not create_gallery(username):
            raise IOError
        for filename, f in request.FILES.iteritems():
            image = Image.open(f)
            filename = gallery_item_name()
            width, height = image.size
            if width > settings.IMAGE_MAX_SIZE[0] or height > settings.IMAGE_MAX_SIZE[1]:
                image.thumbnail(settings.IMAGE_MAX_SIZE)
            image.save(os.path.join(filepath, filename), "JPEG")
            create_gallery_thumbnail(username, filename)
            return filename

    def delete(self, request, filename, slug=None):
        username = slug if slug else request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        thumbpath = filepath + '/thumbs/'
        try:
            os.remove(os.path.join(filepath, filename))
            os.remove(os.path.join(thumbpath, filename))
        except OSError:
            pass
        return HttpResponse(json.dumps({
            'success': True,
            'message': _("File deleted"),
            'level': 'success'
        }))


class UserGalleryView(GalleryView):
    """
    List and manage items uploaded by user.
    """
    def get(self, request):
        context = {
            'title': _("Media gallery"),
            'files': [],
        }
        for picture in UserGalleryItem.objects.filter(user=request.user):
            context['files'].append({
                'pk': picture.pk,
                'thumb': picture.get_thumbnail((128,128)),
                'href': picture.url(),
            })
        return render(request, 'gallery/user-gallery.html', context)

    def post(self, request):
        filename = super(UserGalleryView, self).post(request)
        try:
            UserGalleryItem.objects.get(picture_name=filename)
        except UserGalleryItem.DoesNotExist:
            item = UserGalleryItem(
                user = request.user,
                picture_name = filename,
            )
            item.save()
        if request.is_ajax():
            return HttpResponse(json.dumps({
                'success': True,
                'message': _("File uploaded")
            }))
        else:
            return redirect(reverse('gallery:index'))


class PlaceGalleryView(GalleryView):
    """
    List and manage items uploaded by user.
    """
    def get(self, request, slug):
        location = Location.objects.get(slug=slug)
        context = {
            'title': _("Media gallery"),
            'files': [],
            'location': location,
        }
        for picture in location.pictures.all():
            context['files'].append({
                'pk': picture.pk,
                'thumb': picture.get_thumbnail((128,128)),
                'desc': picture.description,
                'href': picture.url(),
                'name': picture.name,
            })
        return render(request, 'gallery/media-form.html', context)

    def post(self, request, slug):
        filename = super(PlaceGalleryView, self).post(request, slug)
        try:
            LocationGalleryItem.objects.get(picture_name=filename)
        except LocationGalleryItem.DoesNotExist:
            prof = UserProfile.objects.get(user=request.user)
            prof.rank_pts += 1
            prof.save()
            item = LocationGalleryItem(
                user = prof.user,
                location = Location.objects.get(slug=slug),
                picture_name = filename,
                name = request.POST.get('name') or '',
                description = request.POST.get('description') or ''
            )
            item.save()
        if request.is_ajax():
            return HttpResponse(json.dumps({
                'success': True,
                'message': _("File uploaded")
            }))
        return redirect(reverse('locations:gallery', kwargs={'slug':slug}))
