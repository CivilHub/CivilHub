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

import os, subprocess, json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--module', help="Single module to compress")

SRC_DIR = os.path.join(os.getcwd(), 'js', 'build')
LESS_IN = os.path.join(os.getcwd(), 'less', 'style.less')
CSS_OUT = os.path.join(os.getcwd(), 'css', 'style.min.css')
TMP_FILE = os.path.join(os.getcwd(), 'tmp.js')

subprocess.call(['lessc', '-x', LESS_IN, CSS_OUT])

def compress_file(filename):
    f = open('js/config.json', 'r')
    ef = open(filename, 'r')
    tmpf = open(TMP_FILE, 'w')

    conf = json.loads(f.read())
    conf.update(json.loads(ef.read()))
    tmpf.write("(%s)" % json.dumps(conf))

    f.close()
    ef.close()
    tmpf.close()
    subprocess.call(['r.js', '-o', 'tmp.js'])

if __name__ == '__main__':
    args = parser.parse_args()
    for name in os.listdir(SRC_DIR):
        if args.module is None or name == args.module + '.js':
            compress_file (os.path.join(SRC_DIR, name))
    try:
        os.unlink(TMP_FILE)
    except OSError:
        pass
