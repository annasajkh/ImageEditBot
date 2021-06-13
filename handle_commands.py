import urllib.request
import glob
import os
from cmds import commands_list

from PIL import Image


def handle(twitter, tweet, root_tweet, commands):
    global value
    global key
    global res
    
    media_ids = []
    entities = root_tweet.extended_entities["media"]
    
    try:

        for media in entities:
            urllib.request.urlretrieve(media["media_url"], "img.png")

            img = Image.open("img.png")
            
            for command in commands:

                if not "=" in command:
                    continue

                command = command.split("=")

                if len(command) < 2:
                    continue

                key = command[0].strip()
                value = command[1].strip()

                if not key in commands_list.keys():
                    raise Exception(f"there is no '{key}' command please read https://github.com/annasajkh/Commands/blob/main/README.org")
                
                img = commands_list[key](value, img)
            
            img.save("img.png")
            res = twitter.media_upload("img.png")

            if not res == "":
                media_ids.append(res.media_id)
                
        if not len(media_ids) == 0:
            for img_path in glob.glob("*.png"):
                os.remove(img_path)

            twitter.update_status(f"@{tweet.user.screen_name}", media_ids=media_ids, in_reply_to_status_id=tweet.id)
    except Exception as e:
        string = str(e)

        if (len(string) > 270):
            string = string[0:270]
        
        try:
            twitter.update_status(f"@{tweet.user.screen_name} {string}", in_reply_to_status_id=tweet.id)
        
        except Exception as e:
            print(e)
