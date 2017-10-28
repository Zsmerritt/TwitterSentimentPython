
import re, tweepy, datetime, time, csv
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            #data = self.api.rate_limit_status()
            
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count, page, start, end):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            #fetched_tweets = self.api.search(q = query, rpp = count) 
            for tweet in tweepy.Cursor(self.api.search, q=query, until=end, lang="en").items(count):
            #print(fetched_tweets)
            # parsing tweets one by one
            #for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                #parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def writeToCSV(self):
        with open('sentiment.csv', 'a', newline='') as csvfile:    
            #Use csv Writer
            csvWriter = csv.writer(csvfile)
            # calling function to get tweets
            tweets = self.get_tweets(query = 'Bitcoin',count=1000, page = 1, start='2017-01-01', end='2017-10-27')

            if tweets==None:
                print('No Tweets')
            # picking positive tweets from tweets
            else:
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                positivePercent = 100*len(ptweets)/len(tweets)
            # percentage of positive tweets
                print("Positive tweets percentage:",positivePercent," %")
            # picking negative tweets from tweets
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                negativePercent = 100*len(ntweets)/len(tweets)
            # percentage of negative tweets
                print("Negative tweets percentage: ",negativePercent," %")

                nuetralPercent = 100*(len(tweets) - (len(ntweets) + len(ptweets)))/len(tweets)
            #print(nuetral)
            # percentage of neutral tweets
                print("Neutral tweets percentage:",nuetralPercent,"%")
                csvValue = datetime.datetime.now(),positivePercent,negativePercent,nuetralPercent
                csvWriter.writerow(csvValue)
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    while True:
        api.writeToCSV()
        time.sleep(15)###CHANGE TO BE 4 TIME A DAY
    #check to see if throttled
    #data = api.rate_limit_status()
    #print(data)
    


        
 
    # printing first 5 positive tweets
    #print("\n\nPositive tweets:")
    #for tweet in ptweets[:10]:
    #    print(tweet['text'])
 
    # printing first 5 negative tweets
    #print("\n\nNegative tweets:")
    #for tweet in ntweets[:10]:
    #    print(tweet['text'])
 
if __name__ == "__main__":
    # calling main function
    main()

