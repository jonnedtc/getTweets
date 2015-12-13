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

skipped = 0
success = 0

# Create log_file file
log_file = open('log_file.txt', 'w')

# Create empty utf8 file
result_file = codecs.open("tweets_"+FILENAME+".txt", "w", "utf8")

# Open file with tweet IDs
in_file = codecs.open("source\\"+FILENAME)
lines = in_file.readlines()

# Loop through all IDs, get status and write to file
for line in lines[1:]:
	id = line.split()[1]
	try:
		status = api.get_status(id)
	except Exception, e:
		skipped = skipped + 1
		log_file.write(str(success+skipped+1)+" ")
		log_file.write(str(e)+"\n")
		continue
	result_file.write(str(status.created_at)+'\t'+str(line))
	result_file.write(status.text.replace('\n', ' ')+'\n')
	success = success + 1
		
log_file.write("Finished!")
log_file.write("Succesful: "+str(success))
log_file.write("Succesful: "+str(skipped))

# Close files
in_file.close()
result_file.close()
log_file.close()
