#!/usr/bin/python
# coding: utf-8

import twitter
import time
import sys

api = twitter.Api(consumer_key='consumer_key',
				  consumer_secret='consumer_secret',
				  access_token_key='access_token_key',
				  access_token_secret='access_token_secret',
				  sleep_on_rate_limit=True)

#users = api.GetFriends()

#for user in users:
#	print "[+] Mute - Screen Name: %s" %user.screen_name
#	#api.CreateMute(screen_name=user.screen_name)

def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timeformat = 'Waiting... {:02d}:{:02d}'.format(mins, secs)
		sys.stdout.write(timeformat + '\r')
		sys.stdout.flush()
		time.sleep(1)
		t -= 1

filename = "following.txt"

with open(filename) as f:
	content = f.read().splitlines()

for num, line in enumerate(content):
	if line is None:
		print "[+] Line: %s - Blank" %num+1
		continue

	try:
		result = api.CreateMute(screen_name=line)
		print "[+] Line: %s - Mute - Screen Name: %s" %(num+1, line)
	except twitter.error.TwitterError:
		countdown(60*15)

		#time.sleep(60*15)

		result = api.CreateMute(screen_name=line)
		print "[+] Line: %s - Mute - Screen Name: %s" %(num+1, line)
	except:
		print "[+] Line: %s - Screen Name: %s - Error: %s" %(num+1, line, sys.exc_info())
		continue

f.close()

