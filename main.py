import re, os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

from dotenv import load_dotenv
load_dotenv()

class TwitterClient(object):
    # Twitter Class for Sentiment Analysis

    def __init__(self):
        print(object)
        # keys and tokens from the Twitter Dev Console
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        # Clean tweet text by removing links, special characters
        return " ".join(
            re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet
            ).split()
        )

    def get_tweet_sentiment(self, tweet, polarity=0.5, subjectivity=0.5):
        # Utility function to classify sentiment of passed tweet
        # using textblob's sentiment method
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > polarity:
            return "positive"
        elif (-1 * polarity) <= analysis.sentiment.polarity and analysis.sentiment.polarity <= polarity:
            return "neutral"
        elif analysis.sentiment.polarity < (-1 * polarity):
            return "negative"

    def get_tweets(self, query, count=10, polarity=0.5, subjectivity=0.5):
        # Fetch tweets and parse them
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet["text"] = tweet.text
                # saving sentiment of tweet
                parsed_tweet["sentiment"] = self.get_tweet_sentiment(tweet.text, polarity, subjectivity)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepyException as e:
            # print error (if any)
            print("Error : " + str(e))


def checker(queryModel):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # initiating search parameters
    # query = "Andrew Tate"
    # max_tweets = 1000
    # min_retweets = 5
    # min_faves = 5
    # min_replies = 5
    # lang = "en"
    # filter_replies = True
    # final query
    if queryModel['max_tweets'] > 5000:
        queryModel['max_tweets'] = 5000

    query = f"{queryModel['query']} min_faves:{queryModel['min_faves']} min_replies:{queryModel['min_replies']} min_retweets:{queryModel['min_retweets']} lang:{queryModel['lang']}"
    
    if queryModel['filter_replies']:
        query = f"{query} -filter:replies"
    # calling function to get tweets
    tweets = api.get_tweets(query=query, count=queryModel['max_tweets'], polarity=queryModel['polarity'], subjectivity=queryModel['subjectivity'])

    # picking positive, negative and neutral tweets from tweets
    ptweets = []
    ntweets = []
    neutweets = []
    for tweet in tweets:
        if tweet["sentiment"] == "positive":
            ptweets.append(tweet)
        elif tweet["sentiment"] == "negative":
            ntweets.append(tweet)
        else:
            neutweets.append(tweet)
    try:
        positivePerc = 100 * len(ptweets) / len(tweets)
        negativePerc = 100 * len(ntweets) / len(tweets)
        neutralPerc = 100 * len(neutweets) / len(tweets)
        # picking positive tweets from tweets
        # ptweets = [tweet for tweet in tweets if tweet["sentiment"] == "positive"]
        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(positivePerc))
        # picking negative tweets from tweets
        # ntweets = [tweet for tweet in tweets if tweet["sentiment"] == "negative"]
        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(negativePerc))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} %".format(neutralPerc))
    except ZeroDivisionError:
        positivePerc = 0
        negativePerc = 0
        neutralPerc = 0
        print(" ZeroDivisionError: No tweets found for this query")

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet["text"])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet["text"])
    
    result = {
        "positivePerc": positivePerc,
        "negativePerc": negativePerc,
        "neutralPerc": neutralPerc,
        "positiveTweets": ptweets[:10],
        "negativeTweets": ntweets[:10],
        "neutralTweets": neutweets[:10],
    }
    return result


if __name__ == "__main__":
    # calling main function
    checker()
