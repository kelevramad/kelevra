#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import re
import sys
import json
import random
import smtplib
import argparse

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.1"
__description__ = "Send E-mails"

__banner__ = """\033[94m@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[0m \033[92m╔════════════════════════════════╗\033[0m
\033[94m@@              .*/#((/*.              @@\033[0m \033[92m║ ******** Fuck Society ******** ║\033[0m
\033[94m@@        %@@@@@@@@@@@@@@@@@@@@*       @@\033[0m \033[92m╠════════════════════════════════╣\033[0m
\033[94m@@    (@@@@@@@@@@@@@@@@@@@@@@@@@@@#    @@\033[0m \033[92m║ A bug is never just a mistake. ║\033[0m
\033[94m@@  &@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&  @@\033[0m \033[92m║ It represents something bigger.║\033[0m
\033[94m@@/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/@@\033[0m \033[92m║ An error of thinking that makes║\033[0m
\033[94m@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[0m \033[92m║ you who you are.               ║\033[0m
\033[94m@@ #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&.@@\033[0m \033[92m║                                ║\033[0m
\033[94m@@   @@/       *@@@@@@@@@*       /@@   @@\033[0m \033[92m║ Hello, friend. Hello, friend?  ║\033[0m
\033[94m@@   & &@@@@@     .@@@.     @@@@@% &   @@\033[0m\033[92m ║ That's lame. Maybe I should    ║\033[0m
\033[94m@@(  @@@@@@@@@@(   @@@   /@@@@@@@@@@  /@@\033[0m \033[92m║ give you a name. But that's a  ║\033[0m
\033[94m@@&@@@ @@@&    &@@@@@@@@@&    &@@@ @@@&@@\033[0m \033[92m║ slippery slope. You're only in ║\033[0m
\033[94m@@@@@@ @@        @@(@@#@        @@ @@@@@@\033[0m \033[92m║ my head. We have to remember   ║\033[0m
\033[94m@@@@@@@(.@@@@@*,@@&%@@.@@.*@@@@&.#@@@@@@@\033[0m \033[92m║ that.                          ║\033[0m
\033[94m@@@@@@@#@@@@@@@@@ &@@@@*/@@@@@@@@#@@@@@@@\033[0m \033[92m║                                ║\033[0m
\033[94m@@@@@  @@@@@@@@@.@@@@@@@&*@@@@@@@@  @@@@@\033[0m \033[92m║ Sometimes I dream of saving the║\033[0m
\033[94m@@@/   @@@@@@@%   @@@@&   #@@@@@@@   /@@@\033[0m \033[92m║ world. Saving everyone from the║\033[0m
\033[94m@@@                           ..      @@@\033[0m \033[92m║ invisible hand, the one that   ║\033[0m
\033[94m@@@.                                 &@@@\033[0m \033[92m║ brands us with an employee     ║\033[0m
\033[94m@@ *#                               @/ @@\033[0m \033[92m║ badge, the one the forces us to║\033[0m 
\033[94m@@   @@@@@@@%.  ,&&%#%&&,   #@@@@@@@   @@\033[0m \033[92m║ work for them, the one that    ║\033[0m
\033[94m@@   *@@@@@@@@,            @@@@@@@@(   @@\033[0m \033[92m║ controls us every day without  ║\033[0m
\033[94m@@    @@@@@@@@@@@(.   ,%@@@@@@@@@@@    @@\033[0m \033[92m║ us knowing it. But I can't stop║\033[0m 
\033[94m@@    &@@@@@@@@@@@@@@@@@@@@@@@@@@@&    @@\033[0m \033[92m║ it. I'm not that special. I'm  ║\033[0m
\033[94m@@     @@@@@@@@@@@@@@@@@@@@@@@@@@@     @@\033[0m \033[92m║ just anonymous. I'm just alone.║\033[0m
\033[94m@@      *@@@@@@@@@@@@@@@@@@@@@@@%      @@\033[0m \033[92m║                                ║\033[0m
\033[94m@@        #@@@@@@@@@@@@@@@@@@@(        @@\033[0m \033[92m╠════════════════════════════════╣\033[0m
\033[94m@@          ,@@@@@@@@@@@@@@@,          @@\033[0m \033[92m║ Our Democracy has been hacked▒ ║\033[0m
\033[94m@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[0m \033[92m╚════════════════════════════════╝\033[0m"""

__footer__ = ["""    +--=[ Don't cry because it's over, smile because it happened. ]=--+""","""          +--=[ Be yourself; everyone else is already taken. ]=--+""","""                 +--=[ So many books, so little time. ]=--+"""]

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLACK = '\033[90m'
CEND = '\033[0m'

_ARGS = None

__version = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__)

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	parser.add_argument('-c', '--smtp_config', dest='smtp_config', help='Path to text file that lists SMTP Config.', type=argparse.FileType('r'), required=True)
	parser.add_argument('-t', '--addr_to', dest='addr_to', help='Path to text file that lists email addresses.', type=argparse.FileType('r'), required=True)
	parser.add_argument('-s', '--subject', dest='subject', help='Text for Subject.', required=True)
	parser.add_argument('-b', '--body', dest='body', help='File html body.', type=argparse.FileType('r'), required=True)
	parser.add_argument('-a', '--attachment', dest='attachment', help='File attachment.', type=argparse.FileType('r'), required=False)
	parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'), required=False)
	parser.add_argument('-e', '--enable', dest='enable', help='Enable starttls and ehlo.', action='store_true', required=False)
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true', required=False)
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)
	
	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def smtpConfig(filename):
	try:
		with open(filename, 'r') as f:
			readfile = f.read().splitlines()
	except:
		print "%s[-]%s Unexpected error: %s | %s | %s" %(CRED, CEND, sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
		if _ARGS.output: file_write.write('[-] Unexpected error: %s | %s | %s\n' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
		sys.exit(1)

	if not readfile:
		print "%s[-]%s File SMTP Config is empty!" %(CRED, CEND)
		if _ARGS.output: file_write.write('[-] File SMTP Config is empty!\n')
		sys.exit(1)

	return readfile
	
def addrTo(filename):
	try:
		with open(filename, 'r') as f:
			readfile = f.read().splitlines()
	except:
		print "%s[-]%s Unexpected error: %s | %s | %s" %(CRED, CEND, sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
		if _ARGS.output: file_write.write('[-] Unexpected error: %s | %s | %s\n' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
		sys.exit(1)

	if not readfile:
		print "%s[-]%s File Addr To is empty!" %(CRED, CEND)
		if _ARGS.output: file_write.write('[-] File Addr To is empty!\n')
		sys.exit(1)

	return readfile

def sendMail(smtp_config, addr_to):
	idxConfig = 0
	i = 0
	
	while i < len(addr_to):
		if addr_to[i] is None or addr_to[i] == '':
			i += 1
			if _ARGS.debug: print "%s[!]%s Addr To - Linha %s em branco." %(CYELLOW, CEND, i)
			if _ARGS.output: file_write.write('[!] Addr To - Linha %s em branco\n' %i)
			continue

		if idxConfig < 0 or idxConfig >= len(smtp_config):
			idxConfig = 0

		try:
			if smtp_config[idxConfig] is None or smtp_config[idxConfig] == '':
				if _ARGS.debug: print "%s[!]%s SMTP Config - Linha %s em branco." %(CYELLOW, CEND, i)
				if _ARGS.output: file_write.write('[!] SMTP - Config Linha %s em branco\n' %i)
				del smtp_config[idxConfig]
				continue

			#arrConfig = smtp_config[idxConfig].split('|')
			arrConfig = re.split(r'[:;|]', smtp_config[idxConfig])

			smtp_server = arrConfig[0]
			smtp_port = arrConfig[1]
			smtp_user = arrConfig[2]	
			smtp_pass = arrConfig[3]	
		except:
			if _ARGS.debug: print "%s[#]%s EXIT SMTP CONFIG EMPTY!" %(CMAGENTA, CEND)
			if _ARGS.output: file_write.write('[#] EXIT SMTP CONFIG EMPTY!\n')
			sys.exit(1)
					
		if _ARGS.debug:
			print "%s[!]%s Num/Lines: %s/%s" %(CYELLOW, CEND, i+1, len(addr_to))
			print "%s[!]%s SMTP Config: %s - From: %s - To: %s" %(CYELLOW, CEND, smtp_config[idxConfig], smtp_user, addr_to[i])
			print "%s[#]%s Vars==> idxConfig: %s | smtp_config: %s" %(CMAGENTA, CEND, idxConfig, len(smtp_config))
			if _ARGS.output:
				file_write.write('[!] Num/Lines: %s/%s\n' %(i+1, len(addr_to)))
				file_write.write('[!] SMTP Config: %s - From: %s - To: %s\n' %(smtp_config[idxConfig], smtp_user, addr_to[i]))
				file_write.write('[#] Vars==> idxConfig: %s | smtp_config: %s\n' %(idxConfig, len(smtp_config)))

		msg = MIMEMultipart()
		msg['From'] = smtp_user
		msg['To'] = addr_to[i]
		msg['Subject'] = _ARGS.subject

		#read html body
		with open(_ARGS.body.name, 'r') as f:
			body = f.read()
		
		if not body:
			print "%s[-]%s File body html empty!" %(CRED, CEND)
			if _ARGS.output: file_write.write('[-] File body html empty!\n')
			sys.exit(1)

		msg.attach(MIMEText(body, 'html'))
		
		if _ARGS.attachment:
			attachment = open(_ARGS.attachment.name, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" %_ARGS.attachment.name)
			msg.attach(part)

		try:
			server = smtplib.SMTP(smtp_server, smtp_port)
			if _ARGS.enable:
				server.ehlo()
				server.starttls()
			server.login(smtp_user, smtp_pass)
			text = msg.as_string()
			server.sendmail(smtp_user, addr_to[i], text)
			server.quit()

			print "%s[+]%s Send Success - From: %s - To: %s" %(CGREEN, CEND, smtp_user, addr_to[i])
			if _ARGS.output: file_write.write('[+] Send Success - From: %s - To: %s\n' %(smtp_user, addr_to[i]))
			i += 1
			if len(smtp_config) > 1: idxConfig += 1
		except smtplib.SMTPRecipientsRefused:
			if _ARGS.debug:
				print "%s[-]%s Send Fail SMTP Recipient Refused - From: %s - To: %s - SMTP=%s / Port=%s / User=%s / Pass=%s" %(CRED, CEND, smtp_user, addr_to[i], smtp_server, smtp_port, smtp_user, smtp_pass)
				print "%s[-]%s Error SMTP Recipients Refused: %s | %s | %s" %(CRED, CEND, sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
			if _ARGS.output:
				file_write.write('[-] Send Fail SMTP Recipient Refused - From: %s - To: %s - SMTP=%s / Port=%s / User=%s / Pass=%s\n' %(smtp_user, addr_to[i], smtp_server, smtp_port, smtp_user, smtp_pass))
				file_write.write('[-] Error SMTP Recipients Refused: %s | %s | %s\n' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))

			i += 1
		except:
			if _ARGS.output:
				file_write.write('[-] Delete SMTP Config: %s\n' %smtp_config[idxConfig])
				file_write.write('[-] Send Fail - From: %s - To: %s - SMTP=%s / Port=%s / User=%s / Pass=%s\n' %(smtp_user, addr_to[i], smtp_server, smtp_port, smtp_user, smtp_pass))
				file_write.write('[-] Unexpected error: %s | %s | %s\n' %(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))

			if len(smtp_config) > 0:			
				if _ARGS.debug: print "%s[-]%s Delete SMTP Config: %s" %(CRED, CEND, smtp_config[idxConfig])
				del smtp_config[idxConfig]
			if _ARGS.debug:
				print "%s[-]%s Send Fail - From: %s - To: %s - SMTP=%s / Port=%s / User=%s / Pass=%s" %(CRED, CEND, smtp_user, addr_to[i], smtp_server, smtp_port, smtp_user, smtp_pass)
				print "%s[-]%s Unexpected error: %s | %s | %s" %(CRED, CEND, sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
		
		if idxConfig == 0 and len(smtp_config) == 0:
			if _ARGS.debug: print "%s[#]%s EXIT SMTP CONFIG EMPTY!" %(CMAGENTA, CEND)
			if _ARGS.output: file_write.write('[#] EXIT SMTP CONFIG EMPTY!\n')
			sys.exit(1)
		
def main():
	os.system('clear')

	#print random banner
	print __banner__
	print CRED + __footer__[random.randint(0,len(__footer__)-1)] + CEND

	global _ARGS, file_write
	_ARGS = get_args()

	if _ARGS.debug:
		print "%s[!]%s Mode Debug: On" %(CYELLOW, CEND)

	if _ARGS.output:
		file_write = open(_ARGS.output.name, 'w')
		print "%s[*]%s File Output: %s" %(CBLUE, CEND, _ARGS.output.name) 
		file_write.write('[*] File Output: %s\n' %_ARGS.output.name)

	smtp_config  = smtpConfig(_ARGS.smtp_config.name)
	addr_to = addrTo(_ARGS.addr_to.name)

	print "%s[*]%s File SMTP Config / Total: %s / %s" %(CBLUE, CEND, _ARGS.smtp_config.name, len(smtp_config))
	print "%s[*]%s File Add To / Total: %s / %s"  %(CBLUE, CEND, _ARGS.addr_to.name, len(addr_to))
	print "%s[*]%s Subject: %s"  %(CBLUE, CEND, _ARGS.subject)
	print "%s[*]%s File HTML Body: %s"  %(CBLUE, CEND, _ARGS.body.name)
	if _ARGS.attachment:
		print "%s[*]%s File Attachment: %s"  %(CBLUE, CEND, _ARGS.attachment.name)
	if _ARGS.enable:
		print "%s[*]%s Enable ehlo and starttls." %(CBLUE, CEND)
	else:
		print "%s[*]%s Disable ehlo and starttls." %(CBLUE, CEND)

	if _ARGS.output:
		file_write.write('[*] File SMTP Config / Total: %s / %s\n' %(_ARGS.smtp_config.name, len(smtp_config)))
		file_write.write('[*] File Add To / Total: %s / %s\n' %(_ARGS.addr_to.name, len(addr_to)))
		file_write.write('[*] Subject: %s\n' %_ARGS.subject)
		file_write.write('[*] File HTML Body: %s\n' %_ARGS.body.name)
		if _ARGS.attachment:
			file_write.write('[*] File Attachment: %s\n' %_ARGS.attachment.name)
		if _ARGS.enable:
			file_write.write('[*] Enable starttls and ehlo.\n')
		else:
			file_write.write('[*] Disable starttls and ehlo.\n')

	sendMail(smtp_config, addr_to)

	if _ARGS.debug:
		print "%s[#]%s SEND ALL EMAILS!" %(CMAGENTA, CEND)

	if _ARGS.output:
		file_write.write('[#] SEND ALL EMAILS!\n')
		file_write.close()

if __name__ == "__main__":
	main()
