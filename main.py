import re
from api import auth
import tweepy
import handle_commands
from api import twitter

queues = []


class Listener(tweepy.StreamListener):
    def on_status(self, tweet):
        global root_tweet

        # if it is not a comment then it is the root tweet
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

        # remove junk
        text = re.sub("@[^\s]+", "", tweet.text)
        text = re.sub("https://[^\s]+", "", text)
        text = re.sub("\n", "", text)

        if not "=" in text:
            return

        commands = text.split(",")

        if len(commands) < 1:
            return
        
        # add tweet to the queues
        queues.append((twitter, tweet, root_tweet, commands))


listener = Listener()
stream = tweepy.Stream(auth, listener=listener)


while True:
    try:
        """
        this will throw exception when other thread is already running
        we can take advantage of that and we will know when other thread is already running
        or not
        """
        stream.filter(track=["@ImageEditBot"],is_async=True)
    except Exception as e:
        """
        when there is an exception aka when other thread is already running then remove first item
        from the queues and procees the commands and if the bot is processing the command
        and you call it it will add it to the queues
        """
        if queues:
            first = queues.pop(0)
            handle_commands.handle(first[0],first[1],first[2],first[3])