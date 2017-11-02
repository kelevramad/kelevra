import argparse
import urllib2



parser = argparse.ArgumentParser(description="Search query in pastebin.com")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-s", "--search", type=str, help="Search query in pastebin.com", required=True)
parser.add_argument("-g", "--generic", type=str, help="Generic string add pastebin.com")
args = parser.parse_args()

url = 'https://pastebin.com/search?q=' + args.search

if args.verbose:
	print parser.parse_args()
	print url
	
	request_headers = {
	'CF-RAY': '3589d1e9bc034aa2-GRU',
	'Content-Encoding': 'gzip',
	'Content-Type': 'text/html; charset=utf-8',
	'Server': 'cloudflare-nginx',
	'Vary': 'Accept-Encoding',
	'X-Firefox-Spdy': 'h2',
	'X-Frame-Options': 'SAMEORIGIN',
	'X-XSS-Protection': '1; mode=block',
	'x-content-type-options': 'nosniff'}

	request = urllib2.Request(url, headers=request_headers)
	contents = urllib2.urlopen(request).read()
	print contents

	# do something
	response.close()  # best practice to close the file
  
