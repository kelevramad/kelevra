#!/usr/bin/python
# coding: utf-8

import tweepy
import sys
import json
import urllib2
import re
from HTMLParser import HTMLParser

#"http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=jsonp&jsonp=JSON_CALLBACK"

content = urllib2.urlopen("http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1")

json_data = json.loads(content.read())

tweet = json_data[0]['content']

cleanr = re.compile('<.*?>')
tweet = re.sub(cleanr, '', tweet)

tweet = HTMLParser().unescape(tweet)

consumerKey = "consumerKey"
consumerSecret = "consumerSecret"
accessToken = "accessToken"
accessTokenSecret = "accessTokenSecret"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

objTweet = api.update_status(tweet)

print "[+] Screen Name: %s" %api.me().screen_name
print "[+] Tweet: %s" %tweet
print "[+] Object Tweet: %s" %objTweet

