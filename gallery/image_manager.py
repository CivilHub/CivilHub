# -*- coding: utf-8 -*-
from PIL import Image
import os


def resize_image(image, max_width):
    """ Skaluje obraz do podanej szerokości z zachowaniem proporcji. """
    img_width, img_height = image.getdata().size
    if img_width >= max_width and img_width >= img_height:
        # Obrazek do przeskalowania przez `thumbnail`
        img_copy = image.copy()
        img_copy.thumbnail((max_width, max_width), Image.ANTIALIAS)
        return img_copy
    ratio = float(max_width) / float(img_width)
    return image.resize((max_width, int(float(img_height) * ratio)), Image.ANTIALIAS)


def perform_smart_cut(image, size):
    """ Przycina obraz do dokładnych rozmiarów, zachowując jak największą część. """
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
    """ Wycina miniaturkę z przyciętego już obrazu tła. """
    max_w, max_h = size
    width, height = image.getdata().size
    new_width = int(width * float(max_h)/float(height))
    startx = int((new_width - max_w) / 2)
    image = image.resize((new_width, max_h), Image.ANTIALIAS)
    box = (startx, 0, startx + max_w, max_h)
    return image.crop(box)


class ImageManager(object):
    """
    Manager ułatwiający manipulowanie obrazami uploadowanymi na serwer. Pozwala
    tworzyć miniatury oraz przycinać "inteligentnie" obrazy do określonych
    rozmiarów. Tworzy też standardowe nazwy i rozszerzenia plików. Wszystkie
    utworzone obrazy konwertowane są do formatu JPEG.
    """
    @classmethod
    def _open_image(cls, filename):
        """ Zwraca obraz PIL jeżeli jest to możliwe. """
        try:
            return Image.open(filename)
        except (IOError, OSError):
            raise Exception(u"Cannot open image file '%s'" % filename)

    def create_filename(self, suffix, format='jpg'):
        """ Helper, który tworzy odpowiednią nazwę dla pliku. """
        file, ext = os.path.splitext(self.filename)
        return os.path.join(self.dir, "{}_{}.{}".format(file, suffix, format))

    def resize(self, width, height):
        """ Skalujemy obraz z zachowaniem proporcji. """
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
        Przycinamy i skalujemy obraz z zachowaniem proporcji. Przydatne dla
        miniaturek o równych proporcjach. Metoda upewnia się, że jak największa
        część oryginalnego obrazu będzie widoczna.
        """
        return perform_smart_cut(self.image, (width, height))

    def fixed_thumb(self, width, height):
        """ Tworzy miniaturkę zoptymalizowaną dla konkretnego rozmiaru. """
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
    """ Tworzy miniatury zdjęć i przycięte tła dla oryginałów na serwerze. """
    import re
    from django.conf import settings

    max_width, max_height = settings.BACKGROUND_IMAGE_SIZE
    dirname = os.path.join(settings.BASE_DIR, 'media/img/locations')
    for filename in os.listdir(dirname):
        if not re.match(r'\w+_\d+', filename):
            im = ImageManager(os.path.join(dirname, filename), dirname)
            im.fixed_thumb(max_width, max_height)
