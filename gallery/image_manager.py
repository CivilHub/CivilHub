# -*- coding: utf-8 -*-
from PIL import Image
import os

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
            return image.resize((width, int(image_h * ratio)), Image.ANTIALIAS)
        else:
            ratio = height / float(image_h)
            return image.resize((int(image_w * ratio), height), Image.ANTIALIAS)

    def smart_cut(self, width, height):
        """
        Przycinamy i skalujemy obraz z zachowaniem proporcji. Przydatne dla
        miniaturek o równych proporcjach. Metoda upewnia się, że jak największa
        część oryginalnego obrazu będzie widoczna.
        """
        image_w, image_h = self.image.size
        aspect_ratio = image_w / float(image_h)

        if image_h > image_w:
            ratio = width / float(image_w)
            image = image.resize((width, int(image_h * ratio)), Image.ANTIALIAS)
            box = (0, 0, width, height)
        else:
            ratio = height / float(image_h)
            new_width = int(image_w * ratio)
            image = self.image.resize((new_width, height), Image.ANTIALIAS)
            start_x = 0
            x_factor = width
            if new_width > width:
                start_x = int((float(new_width) - float(width)) / 2)
            if new_width < width:
                nratio = width / float(new_width)
                image = image.resize((width, int(float(image_h) * nratio)), Image.ANTIALIAS)
            stop_x = start_x + x_factor
            box = (start_x, 0, stop_x, height)
        return image.crop(box)

    def fixed_thumb(self, width, height):
        """ Tworzy miniaturkę zoptymalizowaną dla konkretnego rozmiaru. """
        img = self.smart_cut(width * 2, height * 2)
        img.save(self.create_filename("{}x{}@2x".format(width, height)), 'JPEG')
        img = img.resize((width, height), Image.ANTIALIAS)
        img.save(self.create_filename("{}x{}".format(width, height)), 'JPEG')

    def fix_size(self, width, height):
        return True

    def __init__(self, filename, dirname=None):
        """ FIXME: tu nie wszystko będzie teraz potrzebne. """
        self.filename = filename.split('/')[-1]
        self.image = self._open_image(filename)
        self.dir = dirname if dirname is not None else os.getcwd()