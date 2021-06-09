import re
import auth
import os
import tweepy
import handle_commands


class Listener(tweepy.StreamListener):
    def on_status(self, tweet):
        global root_tweet

        if tweet.in_reply_to_status_id_str == None:
            root_tweet = tweet
        else:
            root_tweet = api.get_status(tweet.in_reply_to_status_id_str)
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
        handle_commands.handle(api, tweet, root_tweet, commands)


auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"],os.environ["ACCESS_TOKEN_SECRET"])



api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

listener = Listener()
stream = tweepy.Stream(auth, listener=listener)
stream.filter(track=["@ImageEditBot"])
