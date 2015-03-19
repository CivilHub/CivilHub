# -*- coding: utf-8 -*-
import os, subprocess, json

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand


if settings.DEBUG:
    BASE = os.path.join(settings.BASE_DIR, 'places_core/static/places_core')
else:
    BASE = os.path.join(settings.STATIC_ROOT, 'places_core')
SRC_DIR = os.path.join(BASE, 'js', 'build')
LESS_IN = os.path.join(BASE, 'less', 'style.less')
CSS_OUT = os.path.join(BASE, 'css', 'style.min.css')
TMP_FILE = os.path.join(BASE, 'tmp.js')


def compress_file(filename):
    f = open(os.path.join(BASE, 'js/config.json'), 'r')
    ef = open(filename, 'r')
    tmpf = open(TMP_FILE, 'w')

    conf = json.loads(f.read())
    conf.update(json.loads(ef.read()))
    tmpf.write("(%s)" % json.dumps(conf))

    f.close()
    ef.close()
    tmpf.close()
    subprocess.call(['r.js', '-o', TMP_FILE])


class Command(BaseCommand):
    """
    Program kompresujący wszystkie pliki less i js projektu.

    OPCJE
        -m <nazwa_modułu> Wybrany moduł js do skompresowania (np. -m idea-create)
        --only-css        Kompresuj tylko style CSS
    """
    option_list = BaseCommand.option_list + (
        make_option('-m', dest='module', help=u"Kompresuj wybrany moduł"),
        make_option('--css-only',
            dest='css',
            action='store_true',
            default=False,
            help=u"Kompresuj tylko style CSS"
        ),
    )

    def handle(self, *args, **options):
        if options['module'] is not None or options['css']:
            subprocess.call(['lessc', '-x', LESS_IN, CSS_OUT])
        if options['css']:
            return u"Skompresowano style CSS"
        for name in sorted(os.listdir(SRC_DIR)):
            if options['module'] is None or name == options['module'] + '.js':
                compress_file (os.path.join(SRC_DIR, name))
        try:
            os.unlink(TMP_FILE)
        except OSError:
            pass
