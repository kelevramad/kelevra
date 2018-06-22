#!/usr/bin/python
# coding: utf-8

import tweepy
from textblob import TextBlob

consumerKey = "consumerKey"
consumerSecret = "consumerSecret"
accessToken = "accessToken"
accessTokenSecret = "accessTokenSecret"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

tweets = api.search('bolsonaro')

for tweet in tweets:
	frase = TextBlob(tweet.text)

	if frase.detect_language() != 'en':
		traducao = TextBlob(str(frase.translate(to='en')))
		print('Tweet: {0} - Sentimento: {1}'.format(tweet.text, traducao.sentiment))
	else:
		print('Tweet: {0} - Sentimento: {1}'.format(tweet.text, frase.sentiment))

