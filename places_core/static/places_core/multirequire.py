#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multirequire.py
# ===============
#
# Program kompresujący wszystkie pliki less i js projektu, ze szczególnym
# uwzględnieniem tych drugich. Po uruchomieniu bez argumentów program kompresuje
# wszystko za jednym zamachem. Możemy też podać parametr '--module' albo '-m'
# odpowiadający nazwie modułu bez rozszerzenia (np. userspace-profile), żeby
# skompresować tylko ten jeden plik. Na przykład polecenie:
#
#   ./multirequire -m idea-create
#
# skompresuje tylko skrypty dla podstrony tworzenia/edycji idei.

import os, subprocess, json, sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--module', help="Single module to compress")
parser.add_argument('--css', action="store_true", help="Compress only css filest")

SRC_DIR = os.path.join(os.getcwd(), 'js', 'src')
LESS_IN = os.path.join(os.getcwd(), 'less', 'style.less')
CSS_OUT = os.path.join(os.getcwd(), 'css', 'style.min.css')
TMP_FILE = os.path.join(os.getcwd(), 'tmp.js')


def compress_module(module):
    f = open(os.path.join(os.getcwd(), 'js/config.json'), 'r')
    tmpf = open(TMP_FILE, 'w')
    conf = json.loads(f.read())
    conf.update({
        'name': 'js/src/' + module,
        'out': 'js/dist/' + module + '.js',
    })
    tmpf.write("(%s)" % json.dumps(conf))
    f.close()
    tmpf.close()
    subprocess.call(['r.js', '-o', TMP_FILE])


if __name__ == '__main__':
    args = parser.parse_args()
    subprocess.call(['lessc', '-x', LESS_IN, CSS_OUT])
    if args.css:
        sys.exit()
    for name in sorted(os.listdir(SRC_DIR)):
        module = os.path.splitext(name)[0]
        if args.module is None or module == args.module:
            compress_module(module)
    try:
        os.unlink(TMP_FILE)
    except OSError:
        pass
