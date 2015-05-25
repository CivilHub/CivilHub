# -*- coding: utf-8 -*-
from PIL import Image
import os


def resize_image(image, max_width):
    """ Scales the image to the given width, preserving proportions. """
    img_width, img_height = image.getdata().size
    if img_width >= max_width and img_width >= img_height:
        # Obrazek do przeskalowania przez `thumbnail`
        img_copy = image.copy()
        img_copy.thumbnail((max_width, max_width), Image.ANTIALIAS)
        return img_copy
    ratio = float(max_width) / float(img_width)
    return image.resize((max_width, int(float(img_height) * ratio)), Image.ANTIALIAS)


def perform_smart_cut(image, size):
    """ Crops the image to the exact sizes, preserves as much as it can. """
    if size[0] >= size[1]:
        image = resize_image(image, size[0])
        new_width, new_height = image.getdata().size
        start_x = 0
        start_y = (new_height - size[1]) / 2
        stop_x = start_x + size[0]
        stop_y = start_y + size[1]

    box = (start_x, start_y, stop_x, stop_y)
    return image.crop(box)


def crop_thumbnail(image, size):
    """ Cuts out a minature from the cropped background image """
    max_w, max_h = size
    width, height = image.getdata().size
    new_width = int(width * float(max_h)/float(height))
    startx = int((new_width - max_w) / 2)
    image = image.resize((new_width, max_h), Image.ANTIALIAS)
    box = (startx, 0, startx + max_w, max_h)
    return image.crop(box)


class ImageManager(object):
    """
    A manager that facilitates the manipulation of images uploaded onto the server.
    Allows to create minatures and to crop "intelligently" images to the given
    sizes. It also standarizes names and file extensions. ALl created images
    are converted into JPEG formet.
    """
    @classmethod
    def _open_image(cls, filename):
        """ Returns PIL image if it is possible. """
        try:
            return Image.open(filename)
        except (IOError, OSError):
            raise Exception(u"Cannot open image file '%s'" % filename)

    def create_filename(self, suffix, format='jpg'):
        """ A Helper that will create a proper name for the file"""
        file, ext = os.path.splitext(self.filename)
        return os.path.join(self.dir, "{}_{}.{}".format(file, suffix, format))

    def resize(self, width, height):
        """ We scale the image and preserve the proportions"""
        image_w, image_h = self.image.size
        aspect_ratio = image_w / float(image_h)

        if image_h > image_w:
            ratio = width / float(image_w)
            return self.image.resize((width, int(image_h * ratio)), Image.ANTIALIAS)
        else:
            ratio = height / float(image_h)
            return self.image.resize((int(image_w * ratio), height), Image.ANTIALIAS)

    def smart_cut(self, width, height):
        """
        We crop and scale the image and preserve the proportions. Useful for
        minatures with equal proportions. The method makes sure that as much
        as possible of the original image will be visible.
        """
        return perform_smart_cut(self.image, (width, height))

    def fixed_thumb(self, width, height):
        """ Creates a minature optimized for a given size. """
        img = self.smart_cut(width * 2, height * 2)
        img.save(self.create_filename("{}x{}@2x".format(width, height)), 'JPEG')
        img = img.resize((width, height), Image.ANTIALIAS)
        img.save(self.create_filename("{}x{}".format(width, height)), 'JPEG')

        # TODO: rozmiary miniatur powinny być zdefiniowane w ustawieniach
        img = crop_thumbnail(img, (270, 190))
        img.save(self.create_filename("{}x{}".format(270, 190)), 'JPEG')

    def __init__(self, filename, dirname=None):
        """ FIXME: tu nie wszystko będzie teraz potrzebne. """
        self.filename = filename.split('/')[-1]
        self.image = self._open_image(filename)
        self.dir = dirname if dirname is not None else os.getcwd()


def fix_images():
    """ Creates image minatures and cropped background images for original files on the server."""
    import re
    from django.conf import settings

    max_width, max_height = settings.BACKGROUND_IMAGE_SIZE
    dirname = os.path.join(settings.BASE_DIR, 'media/img/locations')
    for filename in os.listdir(dirname):
        if not re.match(r'\w+_\d+', filename):
            im = ImageManager(os.path.join(dirname, filename), dirname)
            im.fixed_thumb(max_width, max_height)
