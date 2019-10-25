#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import m3u8
import logging
import argparse
import requests

from urlparse import urlparse
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Check IPTV Playlist"

__banner__ = """
   _____ _               _      _____ _____ _________      __  _____  _             _ _     _   
  / ____| |             | |    |_   _|  __ \__   __\ \    / / |  __ \| |           | (_)   | |  
 | |    | |__   ___  ___| | __   | | | |__) | | |   \ \  / /  | |__) | | __ _ _   _| |_ ___| |_ 
 | |    | '_ \ / _ \/ __| |/ /   | | |  ___/  | |    \ \/ /   |  ___/| |/ _` | | | | | / __| __|
 | |____| | | |  __/ (__|   <   _| |_| |      | |     \  /    | |    | | (_| | |_| | | \__ \ |_ 
  \_____|_| |_|\___|\___|_|\_\ |_____|_|      |_|      \/     |_|    |_|\__,_|\__, |_|_|___/\__|
                                                                               __/ |            
                                                                              |___/             
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
	group.add_argument('-u', '--url', dest='url', help='Url file m3u or m3u8')
	group.add_argument('-i', '--input', dest='input', help='Input file m3u or m3u8.', type=argparse.FileType('r'))
	parser.add_argument('-o', '--output', dest='output', help='Output file m3u.', type=argparse.FileType('w'))
	parser.add_argument('-t', '--timeout', dest='timeout', help='URL timeout in seconds.', type=int)
	parser.add_argument('-d', '--deep', dest='deep', help='Nested playlist deep.', type=int)
	parser.add_argument('-l', '--log', dest='log', help='Output file log.', type=argparse.FileType('w'))
	parser.add_argument('--thread', dest='thread', help='Execute in thread.', type=int)
	parser.add_argument('--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=VERSION)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()


def show_msg(msg):

	if _args.thread:
		if not msg.endswith('\n'): msg = msg + '\n'
		sys.stdout.write(msg)
		sys.stdout.flush()
	else:
		print msg

	if _args.log:
		if not msg.endswith('\n'): msg = msg + '\n'
		_file_log.write(msg)

def write_output(item):
	if _args.output:
		_file_output.writelines("{0}\n{1}\n\n".format(item['metadata'], item['url']))

def filter_streams(content):

	playlist_items = []

	if content[0] != '#EXTM3U' and content[0].encode("ascii", "ignore").decode("utf-8").strip() != '#EXTM3U':
		raise Exception("Invalid EXTM3U header")

	url_indexes = [i for i, s in enumerate(content) if s.startswith('http')]

	if len(url_indexes) < 1:
		raise Exception("Invalid file, no URLs")

	for u in url_indexes:
		detail = {
			'metadata': content[u - 1],
			'url': content[u]
		}
		playlist_items.append(detail)

	return playlist_items

def verify_video_link(num, total, item, indent=0):
	try:
		url = item['url']
		msg_url = item['url'][:100]+'...' if len(item['url']) > 100 else item['url']
		r = requests.head(url, timeout=_timeout)

		if indent == 0:
			write_output(item)

	except Exception as e:
		show_msg("{}{}[-]{} {}/{} - ERROR loading video URL: {}".format(' ' * indent * 2, CRED, CEND, num, total, msg_url))
		if _args.debug:
			show_msg(" => {}[-]{} Line: {} - Unexpected error: {}".format(CRED, CEND, sys.exc_info()[-1].tb_lineno, str(e)))
		return
	else:
		video_stream = 'Content-Type' in r.headers and ('video' in r.headers['Content-Type'] or 'octet-stream' in r.headers['Content-Type'])
		if r.status_code != 200:
			show_msg("{}{}[-]{} {}/{} - ERROR video URL: {} - {}".format(' ' * indent * 2, CRED, CEND, num, total, r.status_code, msg_url))
			return
		elif video_stream:
			show_msg("{}{}[+]{} {}/{} - OK loading video data: {}".format(' ' * indent * 2, CGREEN, CEND, num, total, msg_url))
			return
		else:
			show_msg("{}{}[-]{} {}/{} - ERROR unknown URL: {}".format(' ' * indent * 2, CRED, CEND, num, total, msg_url))
			return

def verify_playlist_link(num, total, item, indent=0):
	try:
		url = item['url']
		msg_url = item['url'][:100]+'...' if len(item['url']) > 100 else item['url']
		m3u8_obj = m3u8.load(url, timeout=_timeout) # TODO parando aqui
		show_msg("{}{}[+]{} {}/{} - OK playlist data: {}".format(' ' * indent * 2, CGREEN, CEND, num, total, msg_url))
		
		if indent == 0:
			write_output(item)

	except Exception as e:
		show_msg("{}{}[-]{} {}/{} - ERROR loading playlist: {}".format(' ' * indent * 2, CRED, CEND, num, total, msg_url))
		if _args.debug:
			show_msg(" => {}[-]{} Line: {} - Unexpected error: {}".format(CRED, CEND, sys.exc_info()[-1].tb_lineno, str(e)))
		return

	if _deep_playlist > 0:
		for index, nested_playlist in zip(range(_deep_playlist), m3u8_obj.data['playlists']):
			item['url'] = '{0}{1}'.format(m3u8_obj.base_uri, nested_playlist['uri'])
			verify_playlist_link(num, total, item, indent=1)

		for index, segment in zip(range(_deep_playlist), m3u8_obj.data['segments']):
			item['url'] = '{0}{1}'.format(m3u8_obj.base_uri, segment['uri'])
			verify_video_link(num, total, item, indent=1)

def check_playlist_items(num, total, item):
	
	try:
		title = item['metadata'].split(',')[-1]
		url = item['url']
		msg_url = item['url'][:100]+'...' if len(item['url']) > 100 else item['url']

		if url.endswith('.ts'):
			verify_video_link(num, total, item)
		elif url.endswith('.m3u8'):
			verify_playlist_link(num, total, item)
		else:
			try:
				r = requests.head(url, timeout=_timeout)
			except Exception, e:
				show_msg("{}[-]{} {}/{} - ERROR loading URL: {}".format(CRED, CEND, num, total, msg_url))
				if _args.debug:
					show_msg(" => {}[-]{} Line: {} - Unexpected error: {}".format(CRED, CEND, sys.exc_info()[-1].tb_lineno, str(e)))
				return
			else:
				video_stream = 'Content-Type' in r.headers and ('video' in r.headers['Content-Type'] or 'octet-stream' in r.headers['Content-Type'])
				playlist_link = 'Content-Type' in r.headers and 'x-mpegurl' in r.headers['Content-Type']

			if r.status_code != 200:
				show_msg("{}[-]{} {}/{} - ERROR loading URL: {}".format(CRED, CEND, num, total, msg_url))
				return
			elif video_stream:
				show_msg("{}[+]{} {}/{} - OK loading video data: {}".format(CGREEN, CEND, num, total, msg_url))
				write_output(item)
				return
			elif playlist_link:
				verify_playlist_link(num, total, item)
			else:
				show_msg("{}[-]{} {}/{} - ERROR unknown URL: {}".format(CRED, CEND, num, total, msg_url))
				return

	except Exception as e:
		show_msg("{}[-]{} {}/{} - Item: {} - Error: {}".format(CRED, CEND, num, total, item, str(e)[:100]))
		if _args.debug:
			show_msg(" => {}[-]{} Line: {} - Unexpected error: {}".format(CRED, CEND, sys.exc_info()[-1].tb_lineno, str(e)))
		return

def main():
	global _args
	global _file_log
	global _file_output
	global _timeout
	global _m3u_content
	global _deep_playlist

	os.system('clear')

	print __banner__

	_args = get_args()

	if _args.timeout: _timeout = _args.timeout
	else: _timeout = None

	if _args.deep: _deep_playlist = _args.deep
	else: _deep_playlist = 0

	if _args.log:
		_file_log = open(_args.log.name, 'w')
		_file_log.write(__banner__)

	if _args.output:
		_file_output = open(_args.output.name, 'w')
		_file_output.write("#EXTM3U\n\n")

	if _args.debug: show_msg("{}[!]{} Mode Debug On".format(CYELLOW, CEND))
	if _args.log: show_msg("{}[*]{} File log: {}".format(CBLUE, CEND, _args.log.name))
	if _args.output: show_msg("{}[*]{} File output: {}".format(CBLUE, CEND, _args.output.name))
	if _args.timeout: show_msg("{}[*]{} Timeout: {}".format(CBLUE, CEND, str(_args.timeout)))
	if _args.thread: show_msg("{}[*]{} Deep playlist: {}".format(CBLUE, CEND, _deep_playlist))
	if _args.thread: show_msg("{}[*]{} Thread: {}".format(CBLUE, CEND, _args.thread))

	if _args.url or _args.input:
		try:
			if _args.url:
				show_msg("{}[*]{} URL: {}".format(CBLUE, CEND, _args.url))

				response = requests.post(_args.url, timeout=_timeout)
				_m3u_content = response.text.encode('utf8').splitlines()
				response.close()
			else:
				show_msg("{}[*]{} File input: {}".format(CBLUE, CEND, _args.input.name))

				with open(_args.input.name) as f:
					_m3u_content = f.readlines()
					_m3u_content = [x.strip() for x in _m3u_content]

			playlist_items = filter_streams(_m3u_content)

			total_items = len(playlist_items)

			show_msg("{}[*]{} Playlist Items: {}".format(CBLUE, CEND, total_items))

			#if _args.thread:
			#	with ThreadPoolExecutor(max_workers=_args.thread) as executor:
			#		future_tasks = {executor.submit(check_playlist_items, item): item for item in enumerate(playlist_items, 1)}
			#		try:
			#			for future in as_completed(future_tasks, timeout=10):
			#				result = future.result()
			#				#print "Result=%s" %result
			#			pool.shutdown(wait=False)
			#		except Exception as e:
			#			print "ERR: %s" %e

			if _args.thread: pool = ThreadPoolExecutor(max_workers=_args.thread)
			for num, item in enumerate(playlist_items, 1):
				if _args.thread:
					pool.submit(check_playlist_items, num, total_items, item)
				else:
					check_playlist_items(num, total_items, item)
			if _args.thread: pool.shutdown(wait=True)

		except KeyboardInterrupt:
			show_msg("{}[!]{} Keyboard Interrupt...".format(CYELLOW, CEND))
		except Exception as e:
			show_msg("{}[-]{} Error: {}".format(CRED, CEND, str(e)[:100]))
			if _args.debug:
				show_msg("	=> {}[-]{} Line: {} - Unexpected error: {}".format(CRED, CEND, sys.exc_info()[-1].tb_lineno, str(e)))
		finally:
			if _args.log: _file_log.close()
			if _args.output: _file_output.close()


if __name__ == '__main__':
	main()

