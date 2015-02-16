#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, subprocess, json

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
	for root, dirs, files in os.walk(SRC_DIR):
		for name in files:
			compress_file (os.path.join(root, name))
	os.unlink(TMP_FILE)