import urllib.request
import glob
import os
from cmds import commands_list

from PIL import Image
import traceback

# execute every commands to the target image
def execute_commands(img, commands_text):
    commands = commands_text.split(",")

    if len(commands) < 1:
        return
    
    for command in commands:

        if not "=" in command:
            continue

        command = command.split("=")

        # if there is no value like 'rotate= ' then ignore it
        if len(command) < 2:
            continue

        # get key and value
        key = command[0].strip()
        value = "=".join([x.strip() for x in command[1:]])

        if not key in commands_list.keys():
            raise Exception(f"there is no '{key}' command please read https://github.com/annasajkh/Commands/blob/main/README.org")
        
        # apply the function 
        img = commands_list[key](value, img)
    
    return img


def handle(twitter, tweet, root_tweet, commands_text):
    global value
    global key
    global res
    
    media_ids = []
    entities = root_tweet.extended_entities["media"]
    
    try:
        for media in entities:
            #download images
            urllib.request.urlretrieve(media["media_url"], "img.png")

            img = Image.open("img.png")

            img = execute_commands(img,commands_text)

            img.save("img.png")
            res = twitter.media_upload("img.png")

            if not res == "":
                media_ids.append(res.media_id)
        
        #if there is at least one image succesfully uploaded then delete the image from storage
        if not len(media_ids) == 0:
            for img_path in glob.glob("*.png"):
                os.remove(img_path)

            twitter.update_status(f"@{tweet.user.screen_name}", media_ids=media_ids, in_reply_to_status_id=tweet.id)
    except Exception as e:
        traceback.print_exc()

        string = str(e)

        #if the error message is larger than 280 charcter then crop it
        if (len(string) > 280):
            string = string[0:280]
        
        try:
            # try sending error messages
            twitter.update_status(f"@{tweet.user.screen_name} {string}", in_reply_to_status_id=tweet.id)
        except Exception as e:
            print(e)
