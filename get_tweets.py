#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Get tweets from the twitter API by tweet ID from twiqs.nl

import tweepy
import codecs
import config

# Insert filename
FILENAME = "pizza"

# Authenticate to twitter
auth = tweepy.OAuthHandler(config.config['consumer_token'],  config.config['consumer_secret'])
auth.set_access_token(config.config['key'], config.config['secret'])
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Open file with tweet IDs
in_file = codecs.open(FILENAME)
lines = in_file.readlines()

# What line to start?
try:
	progress_file = codecs.open("progress", "r", "utf8")
	progress = progress_file.readlines()
	count = int(progress[-1])
except IOError:
	count = 1

# Loop through all IDs, get status and write to file
for line in lines[count:]:
	id = line.split()[1]
	count += 1
	try:
		status = api.get_status(id)
	except Exception, e:
		print (str(count)+" "+str(e)+"\n")
		continue
	tweet_text = status.text.encode('ascii', errors='ignore')
	tweet_text = tweet_text.replace('\n', ' ')
	with codecs.open("tweets_"+FILENAME, "a", "utf-8") as result_file:
		result_file.write(str(status.created_at)+'\t'+str(line))
		result_file.write(tweet_text.decode('ascii', errors='ignore'))
		result_file.write('\n')
	with codecs.open("progress", "w", "utf-8") as progress_file:
		progress_file.write(str(count))
		
print ("Finished!")
print ("Total: "+str(count))

# Close files
in_file.close()
