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

def main():
	parser = argparse.ArgumentParser(description='Generate all png frames to APNGs.')
	#parser.add_argument('target', help='Target path',required=False)
	#parser.add_argument('-f','--force', type=bool, help='Something forceful.)', default=None, required=False, nargs='*')
	args = parser.parse_args()

	#print args.target
	#__force__= args.force is not None

	#path
	__src_dirpath__ = os.getcwd()
	__src_dirnam_scheme__ = os.path.basename(__src_dirpath__).split('_src')
	__dest_dirname__ = __src_dirnam_scheme__[0]

	if len(__src_dirnam_scheme__)!=2:
		print 'Source Directory name must be "%s_src" instead of "%s"' % (__dest_dirname__,__dest_dirname__)
		sys.exit(1)

	__dest_path__ = os.path.join(os.path.join(__src_dirpath__,'..'), __dest_dirname__)

	# print "Start to build APNGs to ",__dest_path__
	FNULL = open(os.devnull, 'w')

	filter_files = lambda f: os.path.splitext(f)[1][1:].strip().lower()=='png'
	dir_abs_path = lambda d: os.path.join(__src_dirpath__,d)
	dirs = lambda d: os.listdir(d)

	target_dirs = filter(lambda f: os.path.isdir(f) and not f.startswith('.'), dirs(__src_dirpath__))
	targets = [(d, dir_abs_path(d), d.split('_'), dirs(dir_abs_path(d))) for d in target_dirs]
	targets = filter(lambda args: len(args[2])==2 and len(args[3]), targets)

	for dirname, dirpath, scheme, files in targets:
		packname = scheme[0]
		frame_interval = str(int(float(scheme[1])*1000))
		subprocess.call(['apngasm','-o',os.path.join(__dest_path__,(packname+'.png')),os.path.join(dirname, '*.png'),'-d',frame_interval,'-F'],stdout=FNULL, stderr=subprocess.STDOUT)

	print __dest_path__

if __name__ == '__main__':
	main()
