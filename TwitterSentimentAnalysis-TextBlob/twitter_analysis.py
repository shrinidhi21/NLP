import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterAnalysis(object):

    def __init__(self):

        c_key = "j4ZglH2X0Cw7JvR49xhO5jZXZ"
        c_secret = "moPh0K9zH0WbfhnchIBoaUGFNXb1krIe1Fp3W5wu0LBi3P3GqV"
        a_token = "1391580322622414849-6T3BaqQspQ421RLOWCvaz3M1DBx9KS"
        a_secret = "0Q47joCGQ0MCLtTDLn3SqtU2oJzWMUl7JQRLGQPzRj3nL"

        try:
            self.auth = OAuthHandler(c_key, c_secret)
            self.auth.set_access_token(a_token, a_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Failed")

    def tweet_clean(self, tweet):
        return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        sentiment_score = TextBlob(self.tweet_clean(tweet))

        if sentiment_score.sentiment.polarity > 0:
            return 'positive'
        elif sentiment_score.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            tweets_list = self.api.search(q=query, count=count)

            for tweet in tweets_list:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as err:
            print("Error: " + str(err))


def main():
    api = TwitterAnalysis()
    tweets = api.get_tweets(query='india', count=20)

    pos_tweet = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets : {}%".format(100*len(pos_tweet)/len(tweets)))

    neg_tweet = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets : {}%".format(100 * len(neg_tweet) / len(tweets)))

    print(f"Neutral tweets percentage: {100 * (len(tweets) - (len(pos_tweet) + len(neg_tweet))) / len(tweets)} % ")

    print("\n\nPositive tweets:")
    for tweet in pos_tweet[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in neg_tweet[:10]:
        print(tweet['text'])


if __name__ == '__main__':
    main()
