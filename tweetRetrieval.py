import tweepy, csv, json, codecs, datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Access tokens 


def main():
	#api = tweepy.API(auth)

	#data = api.rate_limit_status()

	#print(data['resources']['statuses']['/statuses/search'])
	#print(data)
	print('what is your query')
	query = input()
	print('Start Date, (2015-01-30)')
	start = input()
	print('End Date, (2015-02-30)')
	end = input()
	sentiment(query,start, end)

def sentiment(query, start, end):
	auth = tweepy.auth.OAuthHandler('<CONSUMERKEY>', '<CONSUMERSECRET>')
	auth.set_access_token('ACCESSTOKEN', 'ACCESSTOKENSECRET')
	api = tweepy.API(auth)


	#data = api.rate_limit_status()

	#print(data['resources']['statuses']['/statuses/search'])
	#print(data['resources']['users']['/users/search'])
	# Open/Create a file to append data
	csvFile = open('tweets.csv', 'w')
	#Use csv Writer
	csvWriter = csv.writer(csvFile)
	#f = codecs.open('abc.csv',encoding='utf-8', mode='a')

	#print(tweepy.Cursor(api.search, q='Bitcoin', since='2008-01-01', until='2017-01-01', lang="en").items(10000))


	for tweet in tweepy.Cursor(api.search, q='and', since='2008-01-01', until='2017-01-01', lang="en").items(20):
		#Write a row to the csv file/ I use encode utf-8
		print(tweet)#['statuses']['text']);
		#csvWriter.writerow([tweet['statuses']['text']])



if __name__ == "__main__": 
# calling main function
    main()
