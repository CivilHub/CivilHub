#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script will convert all already existing user profile images
# to JPEG format. You should run it in /media/img/avatars directory.
#
import os
from PIL import Image

BASE_DIR = os.getcwd()

def convert_image(image):
    filename, ext = os.path.splitext(image)
    img = Image.open(image)
    img.save(os.path.join(BASE_DIR, filename + '.jpg'), 'JPEG')
    os.unlink(os.path.join(BASE_DIR, image))
    print("Converted image: {}".format(filename))

if __name__ == '__main__':
    for image in [x for x in os.listdir(BASE_DIR) if '.png' in x]:
        convert_image(image)
    print("Done, without errors")
