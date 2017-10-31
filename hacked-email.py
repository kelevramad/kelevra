#!/usr/bin/python

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0"
__description__ = "Hacked E-mail"

__banner__ = """
ooooo   ooooo                     oooo                        .o8     oooooooooooo                              o8o  oooo 
`888'   `888'                     `888                       "888     `888'     `8                              `"'  `888 
 888     888   .oooo.    .ooooo.   888  oooo   .ooooo.   .oooo888      888         ooo. .oo.  .oo.    .oooo.   oooo   888 
 888ooooo888  `P  )88b  d88' `"Y8  888 .8P'   d88' `88b d88' `888      888oooo8    `888P"Y88bP"Y88b  `P  )88b  `888   888 
 888     888   .oP"888  888        888888.    888ooo888 888   888      888    "     888   888   888   .oP"888   888   888 
 888     888  d8(  888  888   .o8  888 `88b.  888    .o 888   888      888       o  888   888   888  d8(  888   888   888 
o888o   o888o `Y888""8o `Y8bod8P' o888o o888o `Y8bod8P' `Y8bod88P"    o888ooooood8 o888o o888o o888o `Y888""8o o888o o888o
------------- --------- --------- ----------- --------- ----------    ------------ ----------------- --------- ----- -----

Highlighted leaks where your email has been compromised

We use the term Data Leak for when a site has been accessed through a vulnerability in its system and information obtained is shared publicly.
See the matches we have found and take the suitable measures, such as changing your passwords or asking the site where the information was published to remove the content.
"""

from termcolor import colored

import urllib
import urllib2
import json
import argparse
import sys
import requests
import os

__version = "[+] %s - Version: %s" %(__description__, __version__)

API_URL = "https://hacked-emails.com/api?q=%s"
HEADERS = {
	'Host': 'hacked-emails.com',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0'}

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', '--email', help='Email or username search site', required=False)
	group.add_argument('-i', '--input', type=argparse.FileType('r'), help='Path to text file that lists email addresses.', required=False)
	parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Path to output text file.', required=False)
	parser.add_argument('-p', '--option', help='Show options: ', required=False)
	parser.add_argument('-H', '--hide', help='Hide not found search email', action='store_true', required=False)
	parser.add_argument('-d', '--debug', help='Show error and debug.', action='store_true', required=False)
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)
	args = parser.parse_args()

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def pwnedMail(email, args):
	"Search email pwned - hacked-emails.com"

	if email is None or email == "":
		return

	if args.debug:
		print(colored("[!] Debug - url: %s" %API_URL %email, "yellow"))

	#if args.output:

	req = urllib2.Request(API_URL %email, headers=HEADERS)

	try:
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		if args.debug:
			print(colored("[!] Debug - error: %s" %str(e), "yellow"))
			print(colored("[!] Debug - resp: %s" %str(e.read()), "yellow"))
		if not args.hide:
			print(colored("[-] We found no entries for %s" %email, "red"))
		if args.output: file_write.write('[-] We found no entries for %s\n' %email)
		return
	
	content = json.loads(resp.read())
	
	if not args.hide and len(content["data"]) == 0:
		print(colored("[-] We found no entries for %s" %email, "red"))
		if args.output: file_write.write('[-] We found no entries for %s\n' %email)
		return

	print(colored("[+]", "green") + " We have found %s entries for %s" %(len(content["data"]), email))
	if args.output: file_write.write('[+] We have found %s entries for %s\n' %(len(content["data"]), email))

	for value in content["data"]: 
		print (colored("  [+] ", "blue") + "Title: " + value["title"] + " \ Data Leaked: " + value["date_leaked"])
		if args.output: file_write.write("  [+] Title: %s \ Data Leaked: %s\n" %(value["title"], value["date_leaked"]))

	return

def main():
	os.system('clear')

	print __banner__

	global file_write

	args = get_args()

	if args.output:
		file_write = open(args.output.name, 'w')
		print(colored("[*]", "blue") + " File output: %s" %args.output.name)
		if args.output: file_write.write('[*] File output: %s\n' %args.output.name)
	
	if args.hide:
		print(colored("[!] Hide not found search email\n\r", "yellow"))
		
	if args.email is not None:
		pwnedMail(args.email, args)
		exit(0)
	elif args.input is not None:
		lines = sum(1 for line in open(args.input.name))
		print(colored("[*]", "blue") + " Filename: " + args.input.name)
		if args.output: file_write.write('[*] Filename: %s\n' %args.input.name)

		#exit(0)

		for line in args.input:
			pwnedMail(line.strip(), args)
		exit(0)

if __name__ == "__main__":
	main()
