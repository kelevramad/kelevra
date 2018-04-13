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

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

filename = "filename.txt"

with open(filename) as f:
	content = f.read().splitlines()

for num, line in enumerate(content):
	try:
		result = api.create_friendship(line)
		print "[+] Line: %s - Following: %s" %(num+1, line)
	except:
		print "[+] Line: %s - User: %s - Error: %s" %(num+1, line, sys.exc_info())
		continue

f.close()

