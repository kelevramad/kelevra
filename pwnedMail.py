#!/usr/bin/python
# coding=utf-8

import urllib
import urllib2
import json
from termcolor import colored
import argparse
import sys
import requests

def pwnedMail(email, hide):
	"Search email pwned - haveibeenpwned.com"

	if email is None or email == "":
		return

	url = "https://haveibeenpwned.com/api/v2/breachedaccount/"+email+"?includeUnverified=true"

	HEADERS = {
	'Host': 'haveibeenpwned.com',
	'User-Agent': 'Mozilla 5.10',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'pt-BR,en;q=0.4',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0'}

	#headers={ 'User-Agent': 'Mozilla/5.0' }

	req = urllib2.Request(url, headers=HEADERS)

	try:
		proxy = urllib2.ProxyHandler({
		    'http': '34.210.31.59:3128',
		    'https': '34.210.31.59:3128'
		})
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
		f = urllib2.urlopen(url)

		print f.read()

		print(colored('FILHO DA PUTA','red'))
		exit(0)

		#resp = urllib2.urlopen(req)
		#print resp.read()

		#exit(0)
	except urllib2.HTTPError, e:
		print "ERROR: ", e.read()
		if not hide:
			print(colored("[-] " + email + " - No breached accounts and no pastes!", "red"))
		return

	content = json.loads(resp.read())

	print(colored("[+] ", "green") + email + " - Pwned on {0} breached sites:".format(len(content)))

	for value in content: 
		print (colored("	[+] ", "blue") + value["Title"] + " \ Domain: " + value["Domain"] + " \ BreachDate: " + value["BreachDate"])

		compromised = "	--> Compromised data: "
		for key in value["DataClasses"]:
			compromised += format(key) + ", "

		print(compromised[:-2] + "\n\r")
	return

def main():

	parser = argparse.ArgumentParser(description='\';--have i been pwned? \n Check if you have an account that has been compromised in a data breach.')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', '--email', help='Email or username search site', required=False)
	group.add_argument('-f', '--file', type=argparse.FileType('r'), help='File name', required=False)
	parser.add_argument('-o', '--option', help='Show informations: ', required=False)
	parser.add_argument('-H', '--hide', help='Hide not found search email', action='store_true', required=False)
	args = parser.parse_args()

	print("Breaches you were pwned in")

	print("A \"breach\" is an incident where a site's data has been illegally accessed by hackers and then released publicly. Review the types of data that were compromised (email addresses, passwords, credit cards etc.) and take appropriate action, such as changing passwords. " + "\n\r")

	if args.hide:
		print(colored("* Hide not found search email\n\r", "yellow"))

	if args.email is not None:
		pwnedMail(args.email, args.hide)
		exit(0)
	elif args.file is not None:
		for line in args.file:
			pwnedMail(line.strip(), args.hide)

if __name__ == "__main__":
	main()

