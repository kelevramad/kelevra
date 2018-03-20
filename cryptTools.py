#!/usr/bin/python
# coding: utf-8

import os
import sys
import md5
import time
import zlib
import base64
import random
import argparse
import animation
import threading
import itertools

from Crypto import Random
from Crypto.Cipher import AES


__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0"
__description__ = "Crypt Tools"

__banner__ = ["""
  /$$$$$$                                  /$$           /$$$$$$$$                  /$$          
 /$$__  $$                                | $$          |__  $$__/                 | $$          
| $$  \__/  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$           | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$
| $$       /$$__  $$| $$  | $$ /$$__  $$|_  $$_/           | $$ /$$__  $$ /$$__  $$| $$ /$$_____/
| $$      | $$  \__/| $$  | $$| $$  \ $$  | $$             | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$ 
| $$    $$| $$      | $$  | $$| $$  | $$  | $$ /$$         | $$| $$  | $$| $$  | $$| $$ \____  $$
|  $$$$$$/| $$      |  $$$$$$$| $$$$$$$/  |  $$$$/         | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/
 \______/ |__/       \____  $$| $$____/    \___/           |__/ \______/  \______/ |__/|_______/ 
                     /$$  | $$| $$                                                               
                    |  $$$$$$/| $$                                                               
                     \______/ |__/                                                               
""","""
   ÛÛÛÛÛÛÛÛÛ                                  ÛÛÛÛÛ       ÛÛÛÛÛÛÛÛÛÛÛ                   ÛÛÛÛ         
  ÛÛÛ°°°°°ÛÛÛ                                °°ÛÛÛ       °Û°°°ÛÛÛ°°°Û                  °°ÛÛÛ         
 ÛÛÛ     °°°  ÛÛÛÛÛÛÛÛ  ÛÛÛÛÛ ÛÛÛÛ ÛÛÛÛÛÛÛÛ  ÛÛÛÛÛÛÛ     °   °ÛÛÛ  °   ÛÛÛÛÛÛ   ÛÛÛÛÛÛ  °ÛÛÛ   ÛÛÛÛÛ 
°ÛÛÛ         °°ÛÛÛ°°ÛÛÛ°°ÛÛÛ °ÛÛÛ °°ÛÛÛ°°ÛÛÛ°°°ÛÛÛ°          °ÛÛÛ     ÛÛÛ°°ÛÛÛ ÛÛÛ°°ÛÛÛ °ÛÛÛ  ÛÛÛ°°  
°ÛÛÛ          °ÛÛÛ °°°  °ÛÛÛ °ÛÛÛ  °ÛÛÛ °ÛÛÛ  °ÛÛÛ           °ÛÛÛ    °ÛÛÛ °ÛÛÛ°ÛÛÛ °ÛÛÛ °ÛÛÛ °°ÛÛÛÛÛ 
°°ÛÛÛ     ÛÛÛ °ÛÛÛ      °ÛÛÛ °ÛÛÛ  °ÛÛÛ °ÛÛÛ  °ÛÛÛ ÛÛÛ       °ÛÛÛ    °ÛÛÛ °ÛÛÛ°ÛÛÛ °ÛÛÛ °ÛÛÛ  °°°°ÛÛÛ
 °°ÛÛÛÛÛÛÛÛÛ  ÛÛÛÛÛ     °°ÛÛÛÛÛÛÛ  °ÛÛÛÛÛÛÛ   °°ÛÛÛÛÛ        ÛÛÛÛÛ   °°ÛÛÛÛÛÛ °°ÛÛÛÛÛÛ  ÛÛÛÛÛ ÛÛÛÛÛÛ 
  °°°°°°°°°  °°°°°       °°°°°ÛÛÛ  °ÛÛÛ°°°     °°°°°        °°°°°     °°°°°°   °°°°°°  °°°°° °°°°°°  
                         ÛÛÛ °ÛÛÛ  °ÛÛÛ                                                              
                        °°ÛÛÛÛÛÛ   ÛÛÛÛÛ                                                             
                         °°°°°°   °°°°°                                                              
""","""
                                                                                                       
  ,ad8888ba,                                               888888888888                    88          
 d8"'    `"8b                                     ,d            88                         88          
d8'                                               88            88                         88          
88            8b,dPPYba, 8b       d8 8b,dPPYba, MM88MMM         88  ,adPPYba,   ,adPPYba,  88 ,adPPYba,
88            88P'   "Y8 `8b     d8' 88P'    "8a  88            88 a8"     "8a a8"     "8a 88 I8[    ""
Y8,           88          `8b   d8'  88       d8  88            88 8b       d8 8b       d8 88  `"Y8ba, 
 Y8a.    .a8P 88           `8b,d8'   88b,   ,a8"  88,           88 "8a,   ,a8" "8a,   ,a8" 88 aa    ]8I
  `"Y8888Y"'  88             Y88'    88`YbbdP"'   "Y888         88  `"YbbdP"'   `"YbbdP"'  88 `"YbbdP"'
                             d8'     88                                                                
                            d8'      88                                                                
""","""
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║          ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║          ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗██║  ██║   ██║   ██║        ██║          ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""]

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

BLOCK_SIZE = 16

__version = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__)

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	parser.add_argument('-m', '--mode', dest='mode', help='Option crypt or decrypt [default: crypt]', default='crypt', choices=['crypt','decrypt'])
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-t', '--text', dest='text', help='Plain-text for crypt/decrypt')
	group.add_argument('-i', '--input', dest='input', help='Input file for crypt/decrypt.', type=argparse.FileType('r'), nargs='*')
	parser.add_argument('-o', '--output', dest='output', help='Output file for crypt/decrypt.', type=argparse.FileType('w'))
	parser.add_argument('-p', '--password', dest='password', help='Password for crypt.', required=True)
	parser.add_argument('-c', '--compress', dest='compress', help='Compress file before crypt/decompress after decrypt.', action='store_true')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def trans(key):
     return md5.new(key).digest()

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


@animation.wait('bar')
def encryption(message, password):
	try:
		IV = Random.new().read(BLOCK_SIZE)
		aes = AES.new(trans(password), AES.MODE_CFB, IV)
		encode = base64.b64encode(IV + aes.encrypt(message))
		return encode
	except:
		print '%s[-]%s Error encryption message' %(CRED, CEND)
		if args.debug: print '%s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info())
		return ''

@animation.wait('bar')
def decryption(encrypted, password):
	try:
		encrypted = base64.b64decode(encrypted)
		IV = encrypted[:BLOCK_SIZE]
		aes = AES.new(trans(password), AES.MODE_CFB, IV)
		decode = aes.decrypt(encrypted[BLOCK_SIZE:])
		return decode
	except:
		print '%s[-]%s Error decryption message' %(CRED, CEND)
		if args.debug: print '%s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info())
		return ''

@animation.wait('bar')
def load_file(file_input):
	return open(file_input, 'rb').read()

@animation.wait('bar')
def compress(content):
	return zlib.compress(content, 9)

@animation.wait('bar')
def decompress(content):
	return zlib.decompress(content)

@animation.wait('bar')
def write_file(file_output, content):
	file_write = open(file_output, 'w')
	file_write.write(content)
	file_write.close()
	return

def encrypt_file(file_input, file_output, password):
	sys.stdout.write('%s[+]%s Loading file/size: %s/%s' %(CGREEN, CEND, file_input, humansize(os.path.getsize(file_input))))
	print "\r"
	file_load = load_file(file_input)
	
	if args.compress:
		sys.stdout.write('%s[+]%s Compress content file: %s' %(CGREEN, CEND, file_input))
		print "\r"
		file_load = compress(file_load)
	
	sys.stdout.write('%s[+]%s Encryption content - OK' %(CGREEN, CEND))
	print "\r"
	file_encrypt = encryption(file_load, password)
	
	sys.stdout.write('%s[+]%s Write encryption file: %s' %(CGREEN, CEND, file_output))
	print "\r"
	write_file(file_output, file_encrypt)
	return

def decrypt_file(file_input, file_output, password):
	sys.stdout.write('%s[+]%s Loading file/size: %s/%s' %(CGREEN, CEND, file_input, humansize(os.path.getsize(file_input))))
	print "\r"
	file_load = load_file(file_input)

	sys.stdout.write('%s[+]%s Decryption content - OK' %(CGREEN, CEND))
	print "\r"
	file_decrypt = decryption(file_load, password)

	if args.compress:
		try:
			sys.stdout.write('%s[+]%s Decompress content file: %s' %(CGREEN, CEND, file_input))
			print "\r"
			file_decrypt = decompress(file_decrypt)
		except:
			print '%s[-]%s Error decompress content file: %s' %(CRED, CEND, file_input)
			if args.debug: print '%s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info())
			exit(0)
	
	sys.stdout.write('%s[+]%s Write plain-text file: %s' %(CGREEN, CEND, file_output))
	print "\r"
	write_file(file_output, file_decrypt)
	return

def main():
	os.system('clear')

	#print random banner
	print __banner__[random.randint(0,len(__banner__)-1)]

	global args

	args = get_args()

	if args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND)
	
	if args.text:
		if args.mode == 'crypt':
			encode = encryption(args.text, args.password)		
			print '%s[+]%s Encryption Start' %(CBLUE, CEND)
			print '%s[+]%s Message Plain-Text: %s' %(CGREEN, CEND, args.text)
			print '%s[+]%s Password: %s' %(CGREEN, CEND, args.password)
			print '%s[+]%s Password Encrypted: %s' %(CGREEN, CEND, trans(args.password))
			print '%s[+]%s Message Encrypted: %s' %(CGREEN, CEND, encode)

		elif args.mode == 'decrypt':
			decode = decryption(args.text, args.password)
			print '%s[+]%s Decryption Start' %(CBLUE, CEND)
			print '%s[+]%s Message Encrypted: %s' %(CGREEN, CEND, args.text)
			print '%s[+]%s Password: %s' %(CGREEN, CEND, args.password)
			print '%s[+]%s Password Encrypted: %s' %(CGREEN, CEND, trans(args.password))
			print '%s[+]%s Message Plain-Text: %s' %(CGREEN, CEND, decode)

	if args.input:
		for f in args.input:
			if args.mode == 'crypt':
				if len(args.input) > 1 or args.output is None: file_output = os.path.splitext(f.name)[0] + '.enc'
				else: file_output = args.output.name

				print '%s[+]%s Encryption Start' %(CBLUE, CEND)
				print '%s[+]%s Password: %s' %(CGREEN, CEND, args.password)
				print '%s[+]%s Password Encrypted: %s' %(CGREEN, CEND, trans(args.password))
				encrypt_file(f.name, file_output, args.password)		
			elif args.mode == 'decrypt':
				if len(args.input) > 1 or args.output is None: file_output = os.path.splitext(f.name)[0] + '.dec'
				else: file_output = args.output.name

				print '%s[+]%s Encryption Start' %(CBLUE, CEND)
				print '%s[+]%s Password: %s' %(CGREEN, CEND, args.password)
				print '%s[+]%s Password Encrypted: %s' %(CGREEN, CEND, trans(args.password))

				decrypt_file(f.name, file_output, args.password)
		
if __name__ == '__main__':
	main()
