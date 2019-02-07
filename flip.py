#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from PIL import Image

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Flip Image"

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
	parser.add_argument('-f', '--file', dest='file', help='file(s) for flip image(s).', type=argparse.FileType('r'), nargs='*')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def flip_image(image_path, saved_location):
	"""
	Flip or mirror the image
	@param image_path: The path to the image to edit
	@param saved_location: Path to save the cropped image
	"""
	image_obj = Image.open(image_path)
	rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
	rotated_image.save(saved_location)
	print "%s[+]%s File => Flipped: %s => %s" %(CGREEN, CEND, image_path, saved_location)
	#rotated_image.show()

def main():
	os.system('clear')

	global args

	args = get_args()

	if args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND)


	if args.file:
		for f in args.file:
			str_path, str_filename = os.path.split(f.name)
			flip_image(str_path + '/' + str_filename, str_path + '/F_' + str_filename)

if __name__ == '__main__':
	main()

