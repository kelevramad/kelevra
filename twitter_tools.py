#!/usr/bin/python
# coding: utf-8

import os
import csv
import sys
import time
import twitter
import argparse

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Twitter Tools"

__banner__ = """
___________       .__  __    __                 ___________           .__          
\__    ___/_  _  _|__|/  |__/  |_  ___________  \__    ___/___   ____ |  |   ______
  |    |  \ \/ \/ /  \   __\   __\/ __ \_  __ \   |    | /  _ \ /  _ \|  |  /  ___/
  |    |   \     /|  ||  |  |  | \  ___/|  | \/   |    |(  <_> |  <_> )  |__\___ \ 
  |____|    \/\_/ |__||__|  |__|  \___  >__|      |____| \____/ \____/|____/____  >
                                      \/                                        \/ 
----------------------------------------------- -----------------------------------"""

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLACK = '\033[90m'
CEND = '\033[0m'

__version = '%s[+]%s %s - Version: %s' %(CGREEN, CEND, __description__, __version__)

api = twitter.Api(consumer_key = 'consumer_key',
				consumer_secret = 'consumer_secret',
				access_token_key = 'access_token_key',
				access_token_secret = 'access_token_secret',
				sleep_on_rate_limit = True)

def get_args():
	parser = argparse.ArgumentParser(description=__description__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--following', dest='following', help='Input file for following, one user per line.', type=argparse.FileType('r'))
	group.add_argument('--followers', dest='followers', help='Choose a screen name to save file with a user''s followers')
	group.add_argument('--get-following', dest='get_following', help='Get my following users and save de file.', action='store_true')
	group.add_argument('--unfollowing', dest='unfollowing', help='Input file for unfollowing, one user per line.', type=argparse.FileType('r'))
	parser.add_argument('-m', '--mute', dest='mute', help='Mute after following.', action='store_true')
	parser.add_argument('-u', '--unmute', dest='unmute', help='Unmute after unfollowing.', action='store_true')
	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version)

	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timeformat = 'Waiting... {:02d}:{:02d}'.format(mins, secs)
		sys.stdout.write("%s[!]%s %s\r" %(CYELLOW, CEND, timeformat))
		sys.stdout.flush()
		time.sleep(1)
		t -= 1

def following(filename):
	print "%s[+]%s .: Following :." %(CGREEN, CEND)

	with open(filename) as f:
		content = f.read().splitlines()

	print "%s[+]%s Total Lines: %s" %(CGREEN, CEND, len(content))

	for num, line in enumerate(content):
		if line is None or line == '':
			print "%s[!]%s Line: %s - Blank" %(CYELLOW, CEND, str(num+1))
			continue

		try:
			user = api.CreateFriendship(screen_name=line)

			if args.mute: 
				result = api.CreateMute(screen_name=line)
				mute = "/Mute" 
			else:
				mute = ""

			print "%s[+]%s Line: %s - Following%s - Screen Name: %s" %(CGREEN, CEND, num+1, mute, line)
		except twitter.error.TwitterError as twittererror:
			if twittererror[0][0]["code"] != 88:
				print "%s[-]%s Line: %s - Screen Name: %s - Message: %s" %(CRED, CEND, num+1, line, twittererror[0][0]["message"])
				continue
			else:
				countdown(60*15)

				user = api.CreateFriendship(screen_name=line)
				result = api.CreateMute(screen_name=line)
				print "%s[+]%s Line: %s - Following/Mute - Screen Name: %s" %(CGREEN, CEND, num+1, line)
		except:
			print "%s[-]%s Line: %s - Screen Name: %s - Error: %s" %(CRED, CEND, num+1, line, sys.exc_info())
			continue

	f.close()

def followers(name):
	HEADER = ['Screenname']
	user = api.GetUser(screen_name=name)

	print "%s[+]%s .: Get Followers :." %(CGREEN, CEND)
	print "%s[+]%s Screen Name: %s" %(CGREEN, CEND, user.screen_name)
	print "%s[+]%s Followers Count: %s" %(CGREEN, CEND, user.followers_count)

	with open(name + '.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(HEADER)

		followers, counter = [], 1
		while not len(followers) % 100:
			try:
				followers += api.GetFollowers(screen_name=name, cursor=counter, count=300)
				counter += 1
				for follower in followers:
					print "%s[+]%s Screen Name: %s" %(CGREEN, CEND, follower.screen_name)
					csv_writer.writerow([follower.screen_name])
					csvfile.flush()
			except twitter.error.TwitterError as twittererror:
				print "%s[-]%s Message Error: %s" %(CRED, CEND, twittererror[0][0]["message"])
				countdown(60*15)
			except StopIteration:
				print "%s[-]%s StopIteration..." %(CRED, CEND)
				break
			except:
				print sys.exc_info()

def unfollowing(filename):
	print "%s[+]%s .: Unfollowing :." %(CGREEN, CEND)

	with open(filename) as f:
		content = f.read().splitlines()

	print "%s[+]%s Total Lines: %s" %(CGREEN, CEND, len(content))

	for num, line in enumerate(content):
		if line is None or line == '':
			print "%s[!]%s Line: %s - Blank" %(CYELLOW, CEND, str(num+1))
			continue

		try:
			user = api.DestroyFriendship(screen_name=line)

			if args.unmute: 
				result = api.DestroyMute(screen_name=line)
				str_mute = "/unmute" 
			else:
				str_mute = ""

			print "%s[+]%s Line: %s - Unfollowing%s - Screen Name: %s" %(CGREEN, CEND, num+1, str_mute, line)
		except twitter.error.TwitterError as twittererror:
			if twittererror[0][0]["code"] != 88:
				print "%s[-]%s Line: %s - Screen Name: %s - Message: %s" %(CRED, CEND, num+1, line, twittererror[0][0]["message"])
				continue
			else:
				countdown(60*15)

				user = api.DestroyFriendship(screen_name=line)

				if args.unmute: 
					result = api.DestroyMute(screen_name=line)
					str_mute = "/unmute" 
				else:
					str_mute = ""

				print "%s[+]%s Line: %s - Unfollowing%s - Screen Name: %s" %(CGREEN, CEND, num+1, str_mute, line)
		except:
			print "%s[-]%s Line: %s - Screen Name: %s - Error: %s" %(CRED, CEND, num+1, line, sys.exc_info())
			continue

	f.close()

def get_following():
	HEADER = ['Screenname']
	owner = api.VerifyCredentials()

	print "%s[+]%s .: Get Following :." %(CGREEN, CEND)
	print "%s[+]%s Name: %s" %(CGREEN, CEND, owner.name)
	print "%s[+]%s Screen Name: %s" %(CGREEN, CEND, owner.screen_name)
	print "%s[+]%s Description: %s" %(CGREEN, CEND, owner.description)
	print "%s[+]%s Following Count: %s" %(CGREEN, CEND, owner.friends_count)
	print "%s[+]%s Filename: %s" %(CGREEN, CEND, owner.screen_name + '.csv')

	with open(owner.screen_name + '.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(HEADER)

		followings, counter = [], 1

		while not len(followings) % 100:
			try:
				followings += api.GetFriends(cursor=counter, count=300)
				counter += 1

				for following in followings:
					print "%s[+]%s Screen Name: %s" %(CGREEN, CEND, following.screen_name)
					csv_writer.writerow([following.screen_name])
					csvfile.flush()
			except twitter.error.TwitterError as twittererror:
				print "%s[-]%s Message Error: %s" %(CRED, CEND, twittererror[0][0]["message"])
				countdown(60*15)
			except StopIteration:
				print "%s[-]%s StopIteration..." %(CRED, CEND)
				break
			except:
				print sys.exc_info()

def main():
	os.system('clear')

	print __banner__

	global args

	args = get_args()

	if args.debug:
		print "%s[!]%s Mode Debug On" %(CYELLOW, CEND)

	if args.following:
		following(args.following.name)
	elif args.followers:
		followers(args.followers)
	elif args.unfollowing:
		unfollowing(args.unfollowing.name)
	elif args.get_following:
		get_following()

if __name__ == '__main__':
	main()


