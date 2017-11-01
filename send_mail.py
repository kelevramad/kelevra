#!/usr/bin/python
# -*- encoding: utf-8 -*-

import argparse
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import os
import sys
import json

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0"
__description__ = "Send e-mails"


CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

_ARGS = None


def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	parser.add_argument('-c', '--smtp_config', dest='smtp_config', help='Path to text file that lists stmp config.', type=argparse.FileType('r'), required=True)
	parser.add_argument('-t', '--addr_to', dest='addr_to', help='Path to text file that lists email addresses.', type=argparse.FileType('r'), required=True)
	parser.add_argument('-s', '--subject', dest='subject', help='Subject.', required=True)
	parser.add_argument('-b', '--body', dest='body', help='File html body.', type=argparse.FileType('r'), required=True)
	parser.add_argument('-a', '--attachment', dest='attachment', help='File attachment.', type=argparse.FileType('r'), required=False)
        parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true', required=False)
	parser.add_argument('-H', '--hide', dest='hide', help='Hide fail connect to smtp server', action='store_true', required=False)
        parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='store_true', required=False)
	
	if len(sys.argv) < 4:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def smtpConfig(filename):
	try:
		with open(filename, 'r') as f:
			readfile = f.read().splitlines()
	except:
		print "%s[-]%s Error: %s" %(CRED, CEND, sys.exc_info())
		sys.exit(1)

	if not readfile:
		print "%s[-]%s File smtp config is empty!" %(CRED, CEND)
		sys.exit(1)

	return readfile
	
def addrTo(filename):
	try:
		with open(filename, 'r') as f:
			readfile = f.read().splitlines()
	except:
		print "%s[-]%s Error: %s" %(CRED, CEND, sys.exc_info())
		sys.exit(1)

	if not readfile:
		print "%s[-]%s File addr to is empty!" %(CRED, CEND)
		sys.exit(1)

	return readfile

def sendMail(smtp_config, addr_to):
	idxConfig = 0
	i = 0
	
	while i < len(addr_to):
		if addr_to[i] is None or addr_to[i] == '':
			i += 1
			if _ARGS.debug:
				print "%s[!]%s Linha em branco." %(CYELLOW, CEND)
			continue

		arrConfig = smtp_config[idxConfig].split('|')

		smtp_server = arrConfig[0]
		smtp_port = arrConfig[1]
		smtp_user = arrConfig[2]	
		smtp_pass = arrConfig[3]	

		msg = MIMEMultipart()
		msg['From'] = smtp_user
		msg['To'] = addr_to[i]
		msg['Subject'] = _ARGS.subject

		#read html body
		with open(_ARGS.body.name, 'r') as f:
			body = f.read()
		
		if not body:
			print "%s[-]%s File body html empty!" %(CRED, CEND)
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
			server.ehlo()
			server.starttls()
			server.login(smtp_user, smtp_pass)
			text = msg.as_string()
			server.sendmail(smtp_user, addr_to[i], text)
			server.quit()

			print "%s[+]%s Send Success - From: %s - To: %s " %(CGREEN, CEND, smtp_user, addr_to[i])
			i += 1
			idxConfig += 1
		except:
			del smtp_config[idxConfig]
			
			if not _ARGS.hide:
				print "%s[-]%s Send Fail - From: %s - To: %s - smtp=%s / Port=%s / User=%s / Pass=%s" %(CRED, CEND, smtp_user, addr_to[i], smtp_server, smtp_port, smtp_user, smtp_pass)

			if _ARGS.debug:
				print "%s[-]%s Error: %s" %(CYELLOW, CEND, sys.exc_info())

		
		if idxConfig >= len(smtp_config):
			idxConfig = 0

def main():
	global _ARGS
	_ARGS = get_args()

	if _ARGS.version:
		print "%s[+]%s %s - Version: %s" %(CGREEN, CEND, __description__, __version__) 
		sys.exit(0)

	if _ARGS.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND) 

	smtp_config  = smtpConfig(_ARGS.smtp_config.name)
	addr_to = addrTo(_ARGS.addr_to.name)

	sendMail(smtp_config, addr_to)
	
if __name__ == "__main__":
	main()
