# -*- coding: utf-8 -*-
import os, json, sys
from PIL import Image
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from easy_thumbnails.files import get_thumbnailer
from locations.models import Location


class UserGalleryView(View):
    """
    List and manage items uploaded by user.
    """
    def get(self, request):
        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        filehref = settings.MEDIA_URL + username + '/'
        files = []
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            os.makedirs(filepath + '/thumbs')
        for file in os.listdir(filepath):
            if not os.path.isdir(os.path.join(filepath, file)):
                files.append(str(file))
        return HttpResponse(json.dumps({
            'href': filehref,
            'files': sorted(files),
        }))

    def post(self, request):
        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        for filename, f in request.FILES.iteritems():
            filename = request.FILES[filename].name
            file, ex = os.path.splitext(filename)
            filename = slugify(file) + '.' + ex
            destination = open(filepath + '/' + filename, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            size = 128, 128
            thumb = Image.open(filepath + '/' + filename)
            file, ext = os.path.splitext(filename)
            thumbname = filepath + '/thumbs/' + filename
            thumb.thumbnail(size, Image.ANTIALIAS)
            thumb.save(thumbname, 'JPEG')
        return HttpResponse(json.dumps({
            'success': True,
            'message': _("File uploaded")
        }))

    def delete(self, request, filename):
        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        os.remove(os.path.join(filepath, filename))
        return HttpResponse(json.dumps({
            'success': True,
            'message': _("File deleted"),
            'level': 'success'
        }))


class PlaceGalleryView(View):
    """
    List and manage items uploaded by user.
    """
    def get(self, request, slug):
        username = slug
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        filehref = settings.MEDIA_URL + username + '/'
        files = []
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            os.makedirs(filepath + '/thumbs')
        # Ajax request
        if request.is_ajax():
            for file in os.listdir(filepath):
                if not os.path.isdir(os.path.join(filepath, file)):
                    files.append(file)
            return HttpResponse(json.dumps({
                'href': filehref,
                'files': sorted(files),
            }))
        # Static HTML gallery
        for file in os.listdir(filepath):
            if not os.path.isdir(os.path.join(filepath, file)):
                files.append(filehref + str(file))
        ctx = {
            'title': _("Media Gallery"),
            'location': get_object_or_404(Location, slug=slug),
            'files': sorted(files),
        }
        return render(request, 'gallery/media-form.html', ctx)

    def post(self, request, slug):
        username = slug
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            os.makedirs(filepath + '/thumbs')
        for filename, f in request.FILES.iteritems():
            filename = request.FILES[filename].name
            file, ex = os.path.splitext(filename)
            filename = slugify(file) + '.' + ex
            destination = open(filepath + '/' + filename, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            size = 128, 128
            thumb = Image.open(filepath + '/' + filename)
            file, ext = os.path.splitext(filename)
            thumbname = filepath + '/thumbs/' + filename
            thumb.thumbnail(size, Image.ANTIALIAS)
            thumb.save(thumbname, 'JPEG')
        if request.is_ajax():
            return HttpResponse(json.dumps({
                'success': True,
                'message': _("File uploaded")
            }))
        return redirect(reverse('locations:gallery', kwargs={'slug':slug}))

    def delete(self, request, filename):
        username = request.user.username
        filepath = os.path.join(settings.MEDIA_ROOT, username)
        os.remove(os.path.join(filepath, filename))
        return HttpResponse(json.dumps({
            'success': True,
            'message': _("File deleted"),
            'level': 'success'
        }))


def test_view(request):
    """
    Testowanie różnych nowych elementów.
    """
    ctx = {
        'title': _("Upload and manage media"),
        'media_folder': os.path.join(settings.MEDIA_ROOT, request.user.username),
    }
    return render(request, 'gallery/media-test.html', ctx)
