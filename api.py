import tweepy
import os

auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"],os.environ["ACCESS_TOKEN_SECRET"])

twitter = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
