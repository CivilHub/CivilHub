# -*- coding: utf-8 -*-
from .image import generate_thumbs
from .storage import rmdir, massrm


def cleanup_gallery(sender, instance, **kwargs):
    """ Make sure that all files will be deleted along with gallery itself.
    """
    rmdir(instance)


def cleanup_image(sender, instance, **kwargs):
    """ Remove all images when model is deleted.
    """
    massrm(instance)


def adjust_images(sender, instance, **kwargs):
    """ Crop image.
    """
    generate_thumbs(instance.image.path)
