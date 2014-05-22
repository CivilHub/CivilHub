# -*- coding: utf-8 -*-
import os, json, sys
from PIL import Image
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from easy_thumbnails.files import get_thumbnailer
from locations.models import Location


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
    size = 128, 128
    filepath = os.path.join(settings.MEDIA_ROOT, gallery)
    thumb_path = filepath + '/thumbs/'
    thumbname = os.path.join(thumb_path, filename)

    try:
        thumb = Image.open(filepath + '/' + filename)
        thumb.thumbnail(size, Image.ANTIALIAS)
        thumb.save(thumbname, 'JPEG')
        return True
    except IOError:
        return False


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

    def post(self, request):
        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        if not create_gallery(username):
            raise IOError
        for filename, f in request.FILES.iteritems():
            filename = request.FILES[filename].name
            file, ex = os.path.splitext(filename)
            filename = slugify(file) + ex
            destination = open(filepath + '/' + filename, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            create_gallery_thumbnail(username, filename)
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

    def post(self, request, slug):
        username = slug
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        if not create_gallery(username):
            raise IOError
        for filename, f in request.FILES.iteritems():
            filename = request.FILES[filename].name
            file, ex = os.path.splitext(filename)
            filename = slugify(file) + ex
            destination = open(filepath + '/' + filename, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            create_gallery_thumbnail(username, filename)
        if request.is_ajax():
            return HttpResponse(json.dumps({
                'success': True,
                'message': _("File uploaded")
            }))
        return redirect(reverse('locations:gallery', kwargs={'slug':slug}))
