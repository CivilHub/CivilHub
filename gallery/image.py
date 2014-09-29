# -*- coding: utf-8 -*-
import os, re, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.conf import settings


def handle_tmp_image(image):
    """
    Funkcja, która pozwala 'obrabiać' zdjęcia zanim zostaną uploadowane i przekazane
    do silnika Django. Wykorzystywana przy uploadzie zdjęć tla i avatarów do
    tworzenia tymczasowych plików, które mogą być wykorzystane w ImageField
    modelu Django.
    """
    img_io = StringIO.StringIO()
    image.save(img_io, format='JPEG')
    return InMemoryUploadedFile(img_io, None, 'foo.jpg', 'image/jpeg',
                                    img_io.len, None)


def resize_image(image):
    """
    Funkcja przyjmuje obraz PIL jako argument i zwraca taki sam obiekt, ale ze
    zmienionymi rozmiarami.
    TODO: warto pomyśleć o dodaniu rozmiaru jako kolejnego argumentu.
    """
    max_w, max_h = settings.BACKGROUND_IMAGE_SIZE
    width, height = image.getdata().size
    ratio = float(max_w)/float(width)
    return image.resize((max_w, int(height*ratio)), Image.ANTIALIAS)


def delete_image(imagepath):
    """
    Prosta funkcja "wyciszająca" błędy podczas usuwania nieistniejących plików.
    """
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

    if u'nowhere.jpg' in fieldname.path or u'background.jpg' in fieldname.path:
        return False

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
    
    if u'nowhere.jpg' in fieldname.path or u'background.jpg' in fieldname.path:
        return False

    if (os.path.isfile(fieldname.path)):
        os.unlink(fieldname.path)


def crop_gallery_thumb(sender, instance, **kwargs):
    """
    Przycinamy obraz, żeby pokazać go na głównej stronie galerii.
    """
    filename = 'cropped_' + instance.picture_name
    if hasattr(instance, 'location'):
        path = os.path.join(settings.MEDIA_ROOT, instance.location.slug)
    else:
        path = os.path.join(settings.MEDIA_ROOT, instance.user.username)
    image = Image.open(instance.get_filename())
    max_w, max_h = settings.GALLERY_THUMB_SIZE
    width, height = image.getdata().size
    if height > width:
        ratio = float(max_w)/float(width)
        image = image.resize((max_w, int(height*ratio)), Image.ANTIALIAS)
        box = (0, 0, max_w, max_h)
    else:
        ratio = float(max_h)/float(height)
        new_width = int(width*ratio)
        image = image.resize((new_width, max_h), Image.ANTIALIAS)
        start_x = 0
        x_factor = max_w
        if new_width > max_w:
            start_x = int((float(new_width)-float(max_w))/2)
        if new_width < max_w:
            nratio = float(max_w)/float(new_width)
            cw, ch = image.getdata().size
            image = image.resize((max_w, int(float(ch)*nratio)), Image.ANTIALIAS)
        stop_x = start_x + x_factor
        box = (start_x, 0, stop_x, max_h)
    image = image.crop(box)
    image.save(os.path.join(path, filename), 'JPEG')


def delete_cropped_thumb(sender, instance, **kwargs):
    """
    Sygnał usuwający przycięty obrazek dla elementu galerii.
    """
    filename = 'cropped_' + instance.picture_name
    if hasattr(instance, 'location'):
        filepath = os.path.join(settings.MEDIA_ROOT, instance.location.slug, filename)
    else:
        filepath = os.path.join(settings.MEDIA_ROOT, instance.user.username, filename)
    delete_image(filepath)
