import re
from api import auth
import os
import tweepy
import handle_commands
from api import twitter


class Listener(tweepy.StreamListener):
    def on_status(self, tweet):
        global root_tweet

        if tweet.in_reply_to_status_id_str == None:
            root_tweet = tweet
        else:
            root_tweet = twitter.get_status(tweet.in_reply_to_status_id_str)
            if "media" in tweet.entities:
                for media in tweet.extended_entities["media"]:
                    url = media["media_url"]
                    if not "http://pbs.twimg.com/tweet_video_thumb/" in url and not "http://pbs.twimg.com/ext_tw_video_thumb/" in url:
                        root_tweet = tweet

        if "media" in root_tweet.entities:
            for media in root_tweet.extended_entities["media"]:
                url = media["media_url"]
                if "http://pbs.twimg.com/tweet_video_thumb/" in url or "http://pbs.twimg.com/ext_tw_video_thumb/" in url:
                    return
        else:
            return

        text = re.sub("@[^\s]+", "", tweet.text)
        text = re.sub("https://[^\s]+", "", text)
        text = re.sub("\n", "", text.lower())

        if not "=" in text:
            return

        commands = text.split(",")

        if len(commands) < 1:
            return

        handle_commands.handle(twitter, tweet, root_tweet, commands)


listener = Listener()
stream = tweepy.Stream(auth, listener=listener)

while True:
    try:
        stream.filter(track=["@ImageEditBot"])
    except Exception as e:
        print(e)