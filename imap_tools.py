#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import email
import imaplib
import argparse
import subprocess
from datetime import datetime
from validate_email import validate_email

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
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
----------------------------------   --------------------------------------------
"""

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

IMAP_CONFIG = {
	'@gmail' : 'imap.gmail.com',
	'@yahoo' : 'imap.mail.yahoo.com',
	'@live' : 'imap-mail.outlook.com',
	'@hotmail' : 'imap-mail.outlook.com',
	'@office365' : 'outlook.office365.com',
	'@marriott' : 'mail.marriott.com',
	'@bt' : 'imap.btinternet.com',
	'@hyatt' : 'mail.hyatt.com',
	'@tvglobo': 'ms01.tvglobo.com.br'
}

DOWNLOAD_FOLDER = "/tmp/email"

VERSION = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__) 

def get_args():

	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', '--email', dest='email', help='Teste email:password or email|password for test imap')
	group.add_argument('-i', '--input', dest='input', help='Input file with email:password for test imap.', type=argparse.FileType('r'))
	group.add_argument('-t', '--test', dest='test', help='Test email valid.')
	group.add_argument('-f', '--file', dest='file', help='Input file with email for test email.', type=argparse.FileType('r'))
	parser.add_argument('-s', '--search', dest='search', help='Search in email ex: \'FROM "test@mail.com"\'')
	parser.add_argument('-d', '--download', dest='download', help='Download attachment when using in search ex: \'HEADER Content-Type "multipart"\'', action='store_true')
	parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
	parser.add_argument('-b', '--beep', dest='beep', help='Beep alert when raw is live.', action='store_true')
	parser.add_argument('--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=VERSION)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def imap_test(num, raw, lines):

	if _args.debug: print '%s[!]%s Num/Lines: %s/%s - Raw: %s' %(CYELLOW, CEND, num, lines, raw)
	if _args.output: file_write.write('[!] Num: %s - Raw: %s\n' %(num, raw))

	arr_raw = re.split(r'[:;|]', raw)

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
		if _args.debug: print '    => %s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info()[1])
		if _args.output: file_write.write('    => [-] Unexpected error: %s | %s | %s' %(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))


def save_attachment(msg, filename, download_folder="/tmp/email"):

	global int_down, int_n_down, int_n_att

	try:
		body = msg[0][1]
		m = email.message_from_string(body)
		if m.get_content_maintype() != 	'multipart':
			return

		for i, part in enumerate(m.walk()):
			if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None and part.get_filename() is not None:
				original_filename, file_extension = os.path.splitext(part.get_filename())
				
				filename_full = filename + "_" + str(i) +  file_extension

				if file_extension.lower() == ".pdf" or file_extension.lower() == ".jpg" or file_extension.lower() == ".jpeg":
					#print '    => %s[*]%s Downloading: %s => %s' %(CBLUE, CEND, part.get_filename(), filename_full)
					if _args.output: file_write.write('    => [*] Downloading: %s => %s\n' %(part.get_filename(), filename_full))
					open(download_folder + '/' + filename_full, 'wb').write(part.get_payload(decode=True))
					int_down += 1
				else:
					#if _args.debug: print '    => %s[-]%s File not downloading: %s' %(CRED, CEND, part.get_filename())
					if _args.output: file_write.write('    => [-] File not downloading: %s\n' %(part.get_filename()))
					int_n_down += 1
			else:
				#if _args.debug: print '    => %s[-]%s Not attachment: %s' %(CRED, CEND, part.get_filename())
				if _args.output: file_write.write('    => [-] Not attachment: %s\n' %(part.get_filename()))
				int_n_att += 1
		sys.stdout.write('    => %s[*]%s Downloading: %s | Not Downloading: %s | Not attachment: %s\r' %(CBLUE, CEND, str(int_down), str(int_n_down), str(int_n_att)))
		sys.stdout.flush()

	except:
		#exc_type, exc_obj, exc_tb = sys.exc_info()
		#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		#print(exc_type, fname, exc_tb.tb_lineno)
		if _args.debug: print '    => %s[-]%s Error downloading message: %s' %(CRED, CEND, sys.exc_info()[1])
		if _args.output: file_write.write('    => [-] Error downloading message: %s | %s | %s\n' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
	
	return

def imap_tools(num, raw, lines):

	if _args.debug: print '%s[!]%s Num/Lines: %s/%s - Raw: %s' %(CYELLOW, CEND, num, lines, raw)
	if _args.output: file_write.write('[!] Num/Lines: %s/%s - Raw: %s\n' %(num, lines, raw))

	arr_raw = re.split(r'[:;|]', raw)

	if len(arr_raw) == 1:
		if _args.debug: print '%s[-]%s Fail split' %(CRED, CEND)
		if _args.output: file_write.write('[-] Fail split\n')
		return

	try:
		imap = re.search("@[\w]+", arr_raw[0])
		imap = imap.group()
	except:
		if _args.debug: print '%s[!]%s IMAP config not found: %s' %(CYELLOW, CEND, arr_raw[0])
		if _args.output: file_write.write('[!] IMAP config not found: %s\n' %arr_raw[0])
	
	try:
		config = IMAP_CONFIG[imap]
	except:	
		if _args.debug: print '%s[!]%s IMAP config not found: %s' %(CYELLOW, CEND, raw)
		if _args.output: file_write.write('[!] IMAP config not found: %s\n' %raw)
		try:
			imap = re.search("@[\w.]+", arr_raw[0])
			config = 'imap.' + imap.group().replace("@","")
		except:
			if _args.debug: print '%s[-]%s Invalid raw: %s' %(CRED, CEND, raw)
			if _args.output: file_write.write('[-] Invalid raw: %s\n' %raw)
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
				mail.select(readonly=True)
				result, data = 	mail.uid('search', None, '('+_args.search+')')

				if not data[0]:
					print "%s[-]%s %s - Search not found" %(CRED, CEND, raw)
					if _args.output: file_write.write('[-] %s - Search not found\n' %raw)
				else:
					print "%s[+]%s %s - Search found" %(CGREEN, CEND, raw)
					if _args.output: file_write.write('[+] %s - Search found\n' %raw)
					if _args.beep:
						text = '"search found"'
						subprocess.call('echo '+text+'|festival --tts', shell=True)

					if _args.download:
						for message in data:
							items = message.split()
							for item in items:
								try: 
									ret, message_body = mail.uid('fetch', item, '(BODY.PEEK[])')
									#hash = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f')[:-3]
									hash = datetime.utcnow().strftime('%Y%m%d%H%M%S')
									save_attachment(message_body, arr_raw[0] + "_" + str(hash))
								except:
									#exc_type, exc_obj, exc_tb = sys.exc_info()
									#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
									#print '    => %s[-]%s Except: %s | %s | %s' %(CRED, CEND, exc_type, fname, exc_tb.tb_lineno)
									if _args.debug: print '    => %s[-]%s Error read: %s' %(CRED, CEND, sys.exc_info()[1])
									if _args.output: file_write.write('    => [-] Error read: %s | %s | %s\n' %(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
					sys.stdout.write('\n')
					sys.stdout.flush()
			except:
				print '%s[-]%s %s - Search fail - %s' %(CRED, CEND, raw, sys.exc_info()[1])
				if _args.output: file_write.write('[-] %s - Search fail - %s\n' %(raw, sys.exc_info()[1]))

				if _args.debug: print '    => %s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info()[1])
				if _args.output: file_write.write('    => [-] Unexpected error: %s | %s | %s' %(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
	except:
		print '%s[-]%s %s - Dead - %s' %(CRED, CEND, raw, sys.exc_info()[1])
		if _args.output: file_write.write('[-] %s - Dead - %s | %s | %s\n' %(raw, sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
		
		if _args.debug: print '    => %s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info()[1])
		if _args.output: file_write.write('    => [-] Unexpected error: %s | %s | %s' %(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
		return

def main():
	os.system('clear')

	print __banner__
	
	global _args, file_write
	global int_down, int_n_down, int_n_att
	
	_args = get_args()
	email_list = []
	
	if _args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND) 

	if _args.output:	
		file_write = open(_args.output.name, 'w')
		print "%s[*]%s File output: %s" %(CBLUE, CEND, _args.output.name) 
		file_write.write('[*] File output: %s\n' %_args.output.name)

	if _args.download:
		print "%s[*]%s Download attachment" %(CBLUE, CEND)
		if _args.output: file_write.write('[*] Download attachment\n')
		if not os.path.exists(DOWNLOAD_FOLDER):
			print "%s[!]%s Create/Set temp folder: %s" %(CYELLOW, CEND, DOWNLOAD_FOLDER)
			if _args.output: file_write.write('[!] Create/Set temp folder: %s\n' %DOWNLOAD_FOLDER)
			os.mkdir(DOWNLOAD_FOLDER)
		else:
			print "%s[*]%s Set temp folder: %s" %(CBLUE, CEND, DOWNLOAD_FOLDER)
			if _args.output: file_write.write('[*] Set temp folder: %s\n' %DOWNLOAD_FOLDER)

	if _args.email:
		imap_tools(1, _args.email, 1)
	elif _args.test:
		imap_test(1, _args.test, 1)
	elif _args.file:
		lines = sum(1 for line in open(_args.file.name))
		print "%s[*]%s File input: %s" %(CBLUE, CEND, _args.file.name)
		print "%s[*]%s Lines: %s"  %(CBLUE, CEND, str(lines))
		if _args.search: print "%s[*]%s Search: %s"  %(CBLUE, CEND, _args.search)

		if _args.output: 
			file_write.write('[*] File input: %s\n' %_args.file.name)
			file_write.write('[*] Lines: %s\n' %str(lines))
			if _args.search: file_write.write('[*] Search: %s\n' %_args.search)
		
		try:
			for num, line in enumerate(_args.file, 1):
				imap_test(num, line.strip(), lines)
		except KeyboardInterrupt:
			print "%s[!]%s Keyboard Interrupt..." %(CYELLOW, CEND)
			if _args.output:	
				file_write.close()
			sys.exit(1)		
	else:
		lines = sum(1 for line in open(_args.input.name))
		print "%s[*]%s File input: %s" %(CBLUE, CEND, _args.input.name)
		print "%s[*]%s Lines: %s"  %(CBLUE, CEND, str(lines))
		if _args.search: print "%s[*]%s Search: %s"  %(CBLUE, CEND, _args.search)

		if _args.output: 
			file_write.write('[*] File input: %s\n' %_args.input.name)
			file_write.write('[*] Lines: %s\n' %str(lines))
			if _args.search: file_write.write('[*] Search: %s\n' %_args.search)
		
		try:
			for num, line in enumerate(_args.input, 1):
				int_down = 0
				int_n_down = 0
				int_n_att = 0

				imap_tools(num, line.strip(), lines)
		except KeyboardInterrupt:
			print "%s[!]%s Keyboard Interrupt..." %(CYELLOW, CEND)
			if _args.output:	
				file_write.close()
			sys.exit()		

	if _args.output:	
		file_write.close()

if __name__ == '__main__':
	main()

