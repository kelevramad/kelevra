#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import argparse
import requests

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Bin Checker"

__banner__ = """
 /$$$$$$$  /$$                  /$$$$$$  /$$                           /$$                          
| $$__  $$|__/                 /$$__  $$| $$                          | $$                          
| $$  \ $$ /$$ /$$$$$$$       | $$  \__/| $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$   /$$$$$$ 
| $$$$$$$ | $$| $$__  $$      | $$      | $$__  $$ /$$__  $$ /$$_____/| $$  /$$/ /$$__  $$ /$$__  $$
| $$__  $$| $$| $$  \ $$      | $$      | $$  \ $$| $$$$$$$$| $$      | $$$$$$/ | $$$$$$$$| $$  \__/
| $$  \ $$| $$| $$  | $$      | $$    $$| $$  | $$| $$_____/| $$      | $$_  $$ | $$_____/| $$      
| $$$$$$$/| $$| $$  | $$      |  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$$| $$      
|_______/ |__/|__/  |__/       \______/ |__/  |__/ \_______/ \_______/|__/  \__/ \_______/|__/      
"""

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

VERSION = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__) 

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-b', '--bin', dest='bin', help='Bin checker - The first 6 or 8 digits of a payment card number (credit cards, debit cards, etc.) . Ex: "37834235"')
	group.add_argument('-i', '--input', dest='input', help='Input file with the first 6 or 8 digits of a payment card number (credit cards, debit cards, etc.).', type=argparse.FileType('r'))
	parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
	parser.add_argument('-f', '--filter', dest='filter', help='Filter options: number-length,number-luhn,scheme,type,brand,prepaid,country-numeric,country-alpha2,country-name,country-emoji,country-currency,country-latitude,country-longitude,bank-name,bank-url,bank-phone,bank-city.')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=VERSION)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(0)

	return parser.parse_args()

def bin_checker(num, lines, raw):
	arr_raw = re.split(r'[:;|]', raw)

	#{
	#  "number": {
	#    "length": 16,
	#    "luhn": true
	#  },
	#  "scheme": "visa",
	#  "type": "debit",
	#  "brand": "Visa/Dankort",
	#  "prepaid": false,
	#  "country": {
	#    "numeric": "208",
	#    "alpha2": "DK",
	#    "name": "Denmark",
	#    "emoji": "🇩🇰",
	#    "currency": "DKK",
	#    "latitude": 56,
	#    "longitude": 10
	#  },
	#  "bank": {
	#    "name": "Jyske Bank",
	#    "url": "www.jyskebank.dk",
	#    "phone": "+4589893300",
	#    "city": "Hjørring"
	#  }
	#}

	try:
		bin_checker = arr_raw[0][:8]

		url = 'https://lookup.binlist.net/' + bin_checker
		resp = requests.get(url, headers={"Accept-Version":"3"})
		data = resp.json()

		_str = ""
		global filters

		if len(filters) == 0:
			filters = ['number-length','number-luhn','scheme','type','brand','prepaid','country-numeric','country-alpha2','country-name','country-emoji',
						'country-currency','country-latitude','country-longitude','bank-name','bank-url','bank-phone','bank-city']

		for f in filters:
			if data.get('number'):
				if f == 'number-length' and data['number'].get('length'): _str += 'number-length:%s|' %(data['number']['length'])
				if f == 'number-luhn' and data['number'].get('luhn'): _str += 'number-luhn:%s|' %(data['number']['luhn'])
			if f == 'scheme' and data.get('scheme'): _str += 'scheme:%s|' %(data['scheme'])
			if f == 'type' and data.get('type'): _str += 'type:%s|' %(data['type'])
			if f == 'brand' and data.get('brand'): _str += 'brand:%s|' %(data['brand'])
			if f == 'prepaid' and data.get('prepaid'): _str += 'prepaid:%s|' %(data['prepaid'])
			if data.get('country'):
				if f == 'country-numeric' and data['country'].get('numeric'): _str += 'country-numeric:%s|' %(data['country']['numeric'])
				if f == 'country-alpha2' and data['country'].get('alpha2'): _str += 'country-alpha2:%s|' %(data['country']['alpha2'])
				if f == 'country-name' and data['country'].get('name'): _str += 'country-name:%s|' %(data['country']['name'])
				if f == 'country-emoji' and data['country'].get('emoji'): _str += 'country-emoji:%s|' %(data['country']['emoji'])
				if f == 'country-currency' and data['country'].get('currency'): _str += 'country-currency:%s|' %(data['country']['currency'])
				if f == 'country-latitude' and data['country'].get('latitude'): _str += 'country-latitude:%s|' %(data['country']['latitude'])
				if f == 'country-longitude' and data['country'].get('longitude'): _str += 'country-longitude:%s|' %(data['country']['longitude'])
			if data.get('bank'):
				if f == 'bank-name' and data['bank'].get('name'): _str += 'bank-name:%s|' %(data['bank']['name'])
				if f == 'bank-url' and data['bank'].get('url'): _str += 'bank-url:%s|' %(data['bank']['url'])
				if f == 'bank-phone' and data['bank'].get('phone'): _str += 'bank-phone:%s|' %(data['bank']['phone'])
				if f == 'bank-city' and data['bank'].get('city'): _str += 'bank-city:%s|' %(data['bank']['city'])

		print ("%s[+]%s Num/Lines: %s/%s - Raw: %s - Check: %s" %(CGREEN, CEND, num, lines, raw, _str))
		if _args.output: file_write.write('[+] Num/Lines: %s/%s - Raw: %s - Check: %s\n' %(num, lines, raw, _str.encode('utf8')))
	except:
		print ('%s[-]%s %s - Dead - %s' %(CRED, CEND, raw, sys.exc_info()[1]))
		if _args.output: file_write.write('[-] %s - Dead - %s | %s | %s\n' %(raw, sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
		
		if _args.debug: print ('    => %s[-]%s Unexpected error: %s' %(CRED, CEND, sys.exc_info()[1]))
		if _args.output: file_write.write('    => [-] Unexpected error: %s | %s | %s' %(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
		return

def main():
	os.system('clear')

	print (__banner__)
	
	global _args, filters, file_write

	_args = get_args()
	filters = []
	
	if _args.debug:
		print ("%s[!]%s Mode Debug On" %(CYELLOW, CEND)) 

	if _args.output:	
		file_write = open(_args.output.name, 'w')
		print ("%s[*]%s File output: %s" %(CBLUE, CEND, _args.output.name)) 
		file_write.write('[*] File output: %s\n' %_args.output.name)

	if _args.filter:
		print ("%s[*]%s Filter: %s" %(CBLUE, CEND, _args.filter)) 
		if _args.output: file_write.write('[*] Filter: %s\n' %_args.filter)
		filters = _args.filter.split(',')

	if _args.bin:
		bin_checker(1, 1, _args.bin)
	elif _args.input:
		lines = sum(1 for line in open(_args.input.name))
		print ("%s[*]%s File input: %s" %(CBLUE, CEND, _args.input.name))
		print ("%s[*]%s Lines: %s"  %(CBLUE, CEND, str(lines)))
		if _args.output: file_write.write('[*] File input: %s\n' %_args.input.name)
		if _args.output: file_write.write('[*] Lines: %s\n' %str(lines))

		for num, raw in enumerate(_args.input, 1):
			bin_checker(num, lines, raw.strip())

		sys.exit(0)

if __name__ == '__main__':
	main()

