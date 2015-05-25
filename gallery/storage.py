# -*- coding: utf-8 -*-
import os
import shutil

from uuid import uuid4

from django.conf import settings

CONTENT_IMAGE_DIRNAME = os.path.join(settings.MEDIA_ROOT, 'galleries')


def check(gallery):
    """ Check if gallery directory exists or create new one if not.
    """
    if not gallery.dirname:
        gallery.dirname = uuid4().hex
    full_path = os.path.join(CONTENT_IMAGE_DIRNAME, gallery.dirname)
    if not os.path.exists(full_path):
        os.makedirs(full_path)


def rmdir(gallery):
    """ Delete gallery image directory.
    """
    full_path = os.path.join(CONTENT_IMAGE_DIRNAME, gallery.dirname)
    if os.path.exists(full_path):
        shutil.rmtree(full_path)


def upload_path(instance, filename):
    """ Provides unique filename.
    """
    return 'galleries/{}/{}.jpg'.format(instance.gallery.dirname, uuid4().hex)


def massrm(picture):
    """ Delete original and all fixed files for picture.
    """
    clean_filename, ext = os.path.splitext(picture.image.path.split('/')[-1])
    full_path = os.path.join(CONTENT_IMAGE_DIRNAME, picture.gallery.dirname)
    for root, dirnames, files in os.walk(full_path):
        for name in files:
            if clean_filename in name:
                os.unlink(os.path.join(root, name))
