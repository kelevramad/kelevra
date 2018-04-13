#!/usr/bin/python
# coding: utf-8

import os
import sys
import email
import email.header
import imaplib
import datetime
import argparse

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0"
__description__ = "IMAP Hack E-mails"

__banner__ = """
------------------------------    --------------------------------
██╗███╗   ███╗ █████╗ ██████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗
██║████╗ ████║██╔══██╗██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██║██╔████╔██║███████║██████╔╝    ███████║███████║██║     █████╔╝ 
██║██║╚██╔╝██║██╔══██║██╔═══╝     ██╔══██║██╔══██║██║     ██╔═██╗ 
██║██║ ╚═╝ ██║██║  ██║██║         ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝         ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
------------------------------    --------------------------------
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
	'@yahoo' : 'imap.mail.yahoo.com',
	'@live' : 'imap-mail.outlook.com',
	'@hotmail' : 'imap-mail.outlook.com',
	'@office365' : 'outlook.office365.com',
	'@marriott' : 'mail.marriott.com',
	'@bt' : 'imap.btinternet.com',
	'@hyatt' : 'mail.hyatt.com',
}

__version = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__)

EMAIL_FOLDER = "Contatos"

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-i', '--input', dest='input', help='Input file with email:password for test imap.', type=argparse.FileType('r'))
	parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
	parser.add_argument('-b', '--beep', dest='beep', help='Beep alert when raw is live.', action='store_true')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def process_mailbox(M):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = decode[0]
        print 'Message %s: %s' % (num, subject)
        print 'Raw Date:', msg['Date']
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")


def imapSend():
	M = imaplib.IMAP4_SSL('imap.bol.com.br')

	try:
		user = 'user@mail.com'
		passwd = 'password'
		rv, data = M.login(user, passwd)
	except imaplib.IMAP4.error:
		print "LOGIN FAILED!!! "
		sys.exit(1)

	print rv, data

	rv, mailboxes = M.list()
	if rv == 'OK':
		print "Mailboxes:"
		print mailboxes

	sys.exit(1)

	rv, data = M.select(EMAIL_FOLDER)
	if rv == 'OK':
		print "Processing mailbox...\n"
		process_mailbox(M)
		M.close()
	else:
		print "ERROR: Unable to open mailbox ", rv

	M.logout()

def main():
	os.system('clear')

	print __banner__

	global _args
	_args = get_args()

	if _args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND) 

	imapSend()
	
if __name__ == '__main__':
	main()
