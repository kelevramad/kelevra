#!/usr/bin/python
# coding: utf-8

import tweepy
import time
import sys
import csv

consumerKey = "consumerKey"
consumerSecret = "consumerSecret"
accessToken = "accessToken"
accessTokenSecret = "accessTokenSecret"

HEADER = ['Screenname']

#screenname = 'screen_name'
screenname = ['screen_name']

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

for name in screenname:
	user = api.get_user(name)
	print "[+] %s" %user.screen_name
	print "[+] %s" %user.followers_count

	followers = tweepy.Cursor(api.followers, screen_name=name, count=200).items()

	with open(name + '.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(HEADER)
		
		while True:
			try:
				follower = next(followers)
			except tweepy.TweepError:
				#sys.exit(0)
				print("Wait 15 minutes...")
				time.sleep(60*15)
				follower = next(followers)
			except StopIteration:
				print("StopIteration...")
				break
			print ("Screen Name @" + follower.screen_name)
			csv_writer.writerow([follower.screen_name])
			csvfile.flush()
			#try:
			#	result = api.create_friendship(user.id)
			#except:
			#	continue
