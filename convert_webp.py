#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from PIL import Image

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Convert Image Webp to JPG"

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

__version = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__) 

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	parser.add_argument('-f', '--file', dest='file', help='file(s) for convert image(s).', type=argparse.FileType('r'), nargs='*')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def convert_image(image_path, saved_location):
	image_obj = Image.open(image_path).convert("RGB")
	image_obj.save(saved_location,"jpeg")
	print "%s[+]%s File => Converted: %s => %s" %(CGREEN, CEND, image_path, saved_location)

def main():
	os.system('clear')

	global args

	args = get_args()

	if args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND)

	if args.file:
		for f in args.file:
			str_path, str_filename = os.path.split(f.name)
			str_name = os.path.splitext(str_filename)[0]
			convert_image(str_path + '/' + str_filename, str_path + '/' + str_name + '.jpg')

if __name__ == '__main__':
	main()

