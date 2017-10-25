#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, codecs, time, datetime,re,argparse,textwrap, subprocess
from datetime import date, timedelta
from time import mktime
from os.path import expanduser
from shutil import copyfile
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

def convert_to_apng(src_path, dest_path):
	FNULL = open(os.devnull, 'w')

	filter_files = lambda f: os.path.splitext(f)[1][1:].strip().lower()=='png'
	dir_abs_path = lambda d: os.path.join(src_path,d)
	dirs = lambda d: os.listdir(d)

	target_dirs = filter(lambda f: os.path.isdir(f) and not f.startswith('.'), dirs(src_path))
	targets = [(d, dir_abs_path(d), d.split('_'), dirs(dir_abs_path(d))) for d in target_dirs]
	targets = filter(lambda args: len(args[2])==2 and len(args[3]), targets)

	for dirname, dirpath, scheme, files in targets:
		packname = scheme[0]
		frame_interval = str(int(float(scheme[1])*1000))
		subprocess.call(['apngasm','-o',os.path.join(dest_path, (packname+'.png')),os.path.join(dirname, '*.png'),'-d',frame_interval,'-F'],stdout=FNULL, stderr=subprocess.STDOUT)

	print dest_path

def main():
	parser = argparse.ArgumentParser(description='Generate all png frames to APNGs.')
	#parser.add_argument('target', help='Target path',required=False)
	#parser.add_argument('-f','--force', type=bool, help='Something forceful.)', default=None, required=False, nargs='*')
	args = parser.parse_args()

	#print args.target
	#__force__= args.force is not None

	#path
	__src_path__ = os.getcwd()
	__src_dirname_scheme__ = os.path.basename(__src_path__).split('_src')
	__dest_dirname__ = __src_dirname_scheme__[0]

	if len(__src_dirname_scheme__)!=2:
		print 'Default source directory name must be "%s_src" instead of "%s"' % (__dest_dirname__,__dest_dirname__)
		sys.exit(1)

	__dest_path__ = os.path.join(os.path.join(__src_path__,'..'), __dest_dirname__)
	convert_to_apng(__src_path__, __dest_path__)

if __name__ == '__main__':
	main()
