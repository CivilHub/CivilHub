#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, subprocess

SRC_DIR = os.path.join(os.getcwd(), 'js', 'build')
LESS_IN = os.path.join(os.getcwd(), 'less', 'style.less')
CSS_OUT = os.path.join(os.getcwd(), 'css', 'style.min.css')

subprocess.call(['lessc', '-x', LESS_IN, CSS_OUT])

for root, dirs, files in os.walk(SRC_DIR):
    for name in files:
        filepath = os.path.join(root, name)
        subprocess.call(['r.js', '-o', filepath])
