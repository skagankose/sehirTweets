#!/usr/bin/env python
# encoding: utf-8

import tweepy
import csv
import re
import sys

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def getAllTweets(userName, sample=True):
	# Twitter only allows access to a users most recent 3240 tweets with this method

	# authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# initialize a list to hold all the tweepy Tweets
	alltweets = []

	# make initial request for most recent tweets (200 is the maximum allowed count)
	while True:
		try:
			new_tweets = api.user_timeline(screen_name=userName,count=200,max_id=oldest)
			break
		except:
			pass

	# save most recent tweets
	alltweets.extend(new_tweets)

	if not sample:

		# save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1


		# keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print("getting tweets before %s" % (oldest))

			#all subsiquent requests use the max_id param to prevent duplicates
			while True:
				try:
					new_tweets = api.user_timeline(screen_name=userName,count=200,max_id=oldest)
					break
				except:
					pass

			# save most recent tweets
			alltweets.extend(new_tweets)

			# update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1

			print("...%s tweets downloaded so far" % (len(alltweets)))

	''' unused
	# transform the tweepy tweets into a 2D array that will populate the csv
	outTweets = [tweet.text for tweet in alltweets]
	'''

	LABEL = "-"

	f = open('data/raw/%s_tweets.csv' % userName, 'wt')
	writer = csv.writer(f)

	# writer.writerow(["id","created_at","text"])
	for aTweet in alltweets:
		if aTweet.lang == "tr":
			writer.writerow((LABEL, str(aTweet.text)))

	f.close()
