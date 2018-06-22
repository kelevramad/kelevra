#!/usr/bin/python
# coding: utf-8

import tweepy
import time
import csv

consumerKey = "consumerKey"
consumerSecret = "consumerSecret"
accessToken = "accessToken"
accessTokenSecret = "accessTokenSecret"

HEADER = ['Screenname']

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

print "[+] %s" %api.me().screen_name
print "[+] %s" %api.me().friends_count

following = tweepy.Cursor(api.friends, count=200).items()

with open('geiselpresente.csv', 'w') as csvfile:
	csv_writer = csv.writer(csvfile)
	csv_writer.writerow(HEADER)
	
	while True:
		try:
			follow = next(following)
		except tweepy.TweepError:
			#sys.exit(0)
			print("Wait 15 minutes...")
			time.sleep(60*15)
			follow = next(following)
		except StopIteration:
			print("StopIteration...")
			break
		print ("Screen Name @" + follow.screen_name)
		csv_writer.writerow([follow.screen_name])
		csvfile.flush()

