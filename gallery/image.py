# -*- coding: utf-8 -*-
import os, re
from PIL import Image
from django.conf import settings


def resize_image(image):
    max_w, max_h = settings.BACKGROUND_IMAGE_SIZE
    width, height = image.getdata().size
    #if max_w > width: ratio = float(max_w)/float(width)
    #else: ratio = float(width)/float(max_w)
    ratio = float(max_w)/float(width)
    return image.resize((max_w, int(height*ratio)), Image.ANTIALIAS)


def delete_image(imagepath):
    try:
        os.unlink(imagepath)
    except OSError, IOError:
        pass


def get_fieldname(instance):
    """
    Metoda przyjmuje instancję obiektu jako argument i zwraca prawidłową nazwę
    pola przechowującego obrazek tła. Działa dla modeli UserProfile oraz Location.
    """
    if str(type(instance)) == "<class 'locations.models.Location'>":
        fieldname = instance.image
    elif str(type(instance)) == "<class 'userspace.models.UserProfile'>":
        fieldname = instance.background_image

    if fieldname is None:
        raise Exception("Wrong model instance")

    return fieldname


def resize_background_image(sender, instance, created, **kwargs):
    """
    Resize background image to fit for sizes defined in settings file. Method
    takes model instance as argument and performs resizing and cropping.
    """
    fieldname = get_fieldname(instance)
    
    try:
        image = Image.open(fieldname.path)
    except IOError:
        return False
    image = resize_image(image)
    max_w, max_h = settings.BACKGROUND_IMAGE_SIZE
    width, height = image.getdata().size
    start_y = 0
    stop_y = height
    if height > max_h:
        start_y = int(float(height-max_h)/2)
        stop_y = start_y + max_h
    box = (0, start_y, max_w, stop_y)
    image = image.crop(box)
    image.save(fieldname.path, 'JPEG')


def delete_background_image(sender, instance, **kwargs):
    """
    Metoda usuwająca obraz tła dla modeli lokalizacji oraz profilu użytkownika.
    """
    fieldname = get_fieldname(instance)

    if (os.path.isfile(fieldname.path)):
        os.unlink(fieldname.path)
