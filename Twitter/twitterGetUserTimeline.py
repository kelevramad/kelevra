#!/usr/bin/python
# coding: utf-8

import twitter

api = twitter.Api(consumer_key='consumer_key',
				  consumer_secret='consumer_secret',
				  access_token_key='access_token_key',
				  access_token_secret='access_token_secret',
				  sleep_on_rate_limit=True)

#tweets = api.GetUserTimeline(screen_name='Ancelmocom', count=200)
#for tweet in tweets:
#	if tweet.text.lower().find("FeCastanhari") > -1:
#		print tweet.text

#search = api.GetSearch("bolsonaro", count=200) # Replace happy with your search
#for tweet in search:
#    print(tweet.id, tweet.text)

#help(api.GetUserTimeline)

#t = api.GetUserTimeline(screen_name="Ancelmocom", count=10)
#tweets = [i.AsDict() for i in t]
#for t in tweets:
#	print(t['id'], t['text'])

#tweets = api.GetHomeTimeline()
#for tweet in tweets:
#    print tweet.text

print(api.VerifyCredentials())
