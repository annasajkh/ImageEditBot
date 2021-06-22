import re
from api import auth
import tweepy
import handle_commands
from api import twitter

queues = []

class Listener(tweepy.StreamListener):
    def on_status(self, tweet):
        global root_tweet

        print(tweet.text)

        if not tweet.in_reply_to_status_id_str == None:
            root_tweet = twitter.get_status(tweet.in_reply_to_status_id_str)

            print(root_tweet.text)

            if "come" in root_tweet.text:
                print(root_tweet.text)

                cum = tweet.text.replace("come", "cum")
                twitter.update_status(cum, in_reply_to_status_id=root_tweet.id, auto_populate_reply_metadata=True)
                
                return


        # if there is no in_reply_to_status_id_str the it's not a comment
        if tweet.in_reply_to_status_id_str == None:
            root_tweet = tweet
        else:
            """
            if it's a comment then the root tweet must be above it
            in_reply_to_status_id_str is the id of above tweet
            """

            root_tweet = twitter.get_status(tweet.in_reply_to_status_id_str)


            if "media" in tweet.entities:
                for media in tweet.extended_entities["media"]:
                    url = media["media_url"]

                    # if root_tweet is a video or a gif then use the original tweet
                    if not "http://pbs.twimg.com/tweet_video_thumb/" in url and not "http://pbs.twimg.com/ext_tw_video_thumb/" in url:
                        root_tweet = tweet

        if "media" in root_tweet.entities:
            # loop each media
            for media in root_tweet.extended_entities["media"]:
                url = media["media_url"]
                # if it's a video or a gif then return
                if "http://pbs.twimg.com/tweet_video_thumb/" in url or "http://pbs.twimg.com/ext_tw_video_thumb/" in url:
                    return
        else:
            return

        # remove mentions, links, and \n
        text = re.sub("@[^\s]+", "", tweet.text)
        text = re.sub("https://[^\s]+", "", text)
        text = re.sub("\n", "", text)

        if not "=" in text:
            return
        
        # add tweet to the queues
        queues.append((twitter, tweet, root_tweet, text))


listener = Listener()
stream = tweepy.Stream(auth, listener=listener)


while True:
    try:
        stream.filter(track=["@ImageEditBot"],is_async=True)
    except Exception as e:
        if queues:
            first = queues.pop(0)
            handle_commands.handle(first[0],first[1],first[2],first[3])
