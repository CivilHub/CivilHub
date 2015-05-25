# -*- coding: utf-8 -*-
import os
import re
import StringIO

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from .image_manager import ImageManager


def rename_background_file(filepath, pref="s_"):
    """
    The function takes an absolute system path to the background image (mainly
    with location and users in mind) and adds/changes the name for the cropped
    file (prefix). The prefix can be set in any way, but only "s_" will work
    later on in the templates.

    TODO: global cropped image prefix.
    """
    path, file = os.path.split(filepath)
    return os.path.join(path, pref + file)


def handle_tmp_image(image):
    """
    A function that allows to "change" the images before they get uploaded and send
    to Django enginge. Used while uploading background images and avatars to create
    temporary files that can be used in ImageField model of Django.
    """
    img_io = StringIO.StringIO()
    image.save(img_io, format='JPEG')
    return InMemoryUploadedFile(img_io, None, 'foo.jpg', 'image/jpeg',
                                    img_io.len, None)


def resize_image(image, size=None):
    """
    The function take the PIL image as an argument and returns the same object
    but with changed dimensions. The change of dimensions takes place to the
    maximum width.
    """
    max_w, max_h = settings.BACKGROUND_IMAGE_SIZE if size is None else size
    width, height = image.getdata().size
    ratio = float(max_w) / float(width)
    return image.resize((max_w, int(height*ratio)), Image.ANTIALIAS)


def delete_image(imagepath):
    """
    A simple function that "silences" errors while deleting files that don't exist.
    """
    try:
        os.unlink(imagepath)
    except OSError, IOError:
        pass


def get_fieldname(instance):
    """
    A Method that takes an instance of an object as an argument and returns the
    correct name of the filed that stores the background image. Works for UserProfile
    model and Location.
    """
    field_names = ('background_image', 'image')
    fieldname = None

    for fn in field_names:
        fieldname = instance.__dict__.get(fn)
        if fieldname is not None:
            break

    if fieldname is None:
        raise Exception("Wrong model instance")

    return fieldname


def crop_background(image, pathname, max_size=(270,150)):
    """
    Crop background images and display them in thumbs. Both arguments are
    required. Image is PIL image instance (resized and cropped to fit background
    dimmensions) and pathname means upload path (excluding MEDIA_ROOT, e.g same
    as in model's field declaration).
    """
    max_w, max_h  = max_size
    width, height = image.getdata().size
    new_width     = int(width * float(max_h)/float(height))
    startx        = int((new_width - max_w) / 2)

    image = image.resize((new_width, max_h), Image.ANTIALIAS)
    box = (startx, 0, startx + max_w, max_h)
    image = image.crop(box)
    path = os.path.join(settings.MEDIA_ROOT, rename_background_file(pathname))
    image.save(path, 'JPEG')


def resize_background_image(sender, instance, created, **kwargs):
    """
    Resize background image to fit for sizes defined in settings file. Method
    takes model instance as argument and performs resizing and cropping.
    """
    fieldname = instance.image

    if u'nowhere.jpg' in fieldname.path or u'background.jpg' in fieldname.path or u'default.jpg' in fieldname.path:
        return False

    max_width, max_height = settings.BACKGROUND_IMAGE_SIZE
    im = ImageManager(fieldname.path, "/".join(fieldname.path.split('/')[:-1]))
    im.fixed_thumb(max_width, max_height)


def delete_background_image(sender, instance, **kwargs):
    """
    A Method that deletes the background image for location and user profile models
    """
    fieldname = get_fieldname(instance)

    if u'nowhere.jpg' in fieldname or u'background.jpg' in fieldname:
        return False

    if (os.path.isfile(fieldname)):
        os.unlink(fieldname)

    path, fname = os.path.splitext(fieldname)
    fname = "s_" + str(fname)
    fpath = os.path.join(path, fname)

    if os.path.isfile(fpath):
        os.unlink(fpath)


def crop_gallery_thumb(sender, instance, **kwargs):
    """
    We crop the image to show it on the main site of the gallery.
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
    The signal that deletes the cropped image for gallery element.
    """
    filename = 'cropped_' + instance.picture_name
    if hasattr(instance, 'location'):
        filepath = os.path.join(settings.MEDIA_ROOT, instance.location.slug, filename)
    else:
        filepath = os.path.join(settings.MEDIA_ROOT, instance.user.username, filename)
    delete_image(filepath)


def thumb_name(filename, size):
    """ Given file name or full path and size tuple returns thumbnail name. """
    file, ext = os.path.splitext(filename)
    return "%s_%dx%d%s" % (file, size[0], size[1], ext)


def crop_thumb(filename, size):
    """
    The function takes the path to the image file as an argument and creates
    a minature with the given (typed) dimensions. The image will be shrunk and
    cropped "intelligently".
    """
    image = Image.open(filename)
    max_w, max_h = size
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
        if new_width >= max_w:
            start_x = int((float(new_width)-float(max_w))/2)
        else:
            nratio = float(max_w)/float(new_width)
            cw, ch = image.getdata().size
            image = image.resize((max_w, int(float(ch)*nratio)), Image.ANTIALIAS)
        stop_x = start_x + x_factor
        box = (start_x, 0, stop_x, max_h)
    image = image.crop(box)
    image.save(thumb_name(filename, size), 'JPEG')


def get_image_size(imagepath):
    """
    A small helper. We give the path to the image and the function returns
    a tuplet with its height and width in pixels. We return the sizes of
    the images already matched (changed).
    """
    try:
        image = Image.open(os.path.splitext(imagepath)[0] + '_fx.jpg')
        return image.getdata().size
    except IOError:
        # Element najwyraźniej ma ustawiony obrazek domyślny
        return 0


def adjust_uploaded_image(sender, instance, **kwargs):
    """
    A unified method that manages images for our model ImagableItemMixin.
    Readies images of standarized sizes and the same for retina.
    The size of the image is set in settings.DEFAULT_IMG_SIZE. We preserve
    the original.
    """
    # Ignoruj wpisy z domyślnymi obrazami
    if instance.image.name == settings.DEFAULT_IMG_PATH:
        return True
    # Zapisz kopię oryginału jako JPEG
    base_image = Image.open(instance.image.path)
    filename = os.path.splitext(instance.image.path)[0]
    base_image.save("{}.jpg".format(filename), 'JPEG')
    # Rozmiar obrazów i miniatur pobieramy z ustawień globalnych
    width, height = settings.DEFAULT_IMG_SIZE
    t_width, t_height = settings.DEFAULT_THUMB_SIZE
    # Normalne obrazki w pełnych wymiarach
    image = resize_image(base_image, (width * 2, height * 2))
    image.save("{}_fx@2x.jpg".format(filename), 'JPEG')
    image = resize_image(base_image, (width, height))
    image.save("{}_fx.jpg".format(filename), 'JPEG')
    # Miniatury do pokazania w widokach list i aktywności
    image = resize_image(base_image, (t_width * 2, t_height * 2))
    image.save("{}_thumbnail@2x.jpg".format(filename), 'JPEG')
    image = resize_image(base_image, (t_width, t_height))
    image.save("{}_thumbnail.jpg".format(filename), 'JPEG')


# Functions and methods for ContentObjectGallery and ContentObjectPicture
# ------------------------------------------------------------------------------


def fix_path(filepath, size='BIG'):
    """
    Returns path to fixed images (i.e. images with proper suffix) based on
    full path to image provided as argument.
    """
    path_parts = filepath.split('/')
    name = path_parts.pop()
    size_prefix = "%dx%d_" % settings.CO_THUMB_SIZES.get(size.upper())
    path_parts.append(size_prefix + name)
    return "/".join(path_parts)


def crop(image, max_size):
    """ Takes PIL image and tuple with width and height and performs "smart cut".
    """
    max_w, max_h = max_size
    width, height = image.getdata().size

    # Find ratio
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

    return image.crop(box)


def generate_thumbs(filepath):
    """ Creates thumbs for all selected sizes for ContentObjectPicture.
    """
    image = Image.open(filepath)

    # First convert all uploaded originals to JPG format
    image = image.convert('RGB')
    image.save(filepath, 'JPEG')

    for label, size in settings.CO_THUMB_SIZES.iteritems():
        thumb = crop(image.copy(), size)
        thumb.save(fix_path(filepath, label), 'JPEG')
