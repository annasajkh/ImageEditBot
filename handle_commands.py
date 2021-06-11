import cmds
import urllib.request
import glob
import os

from PIL import Image as PillImage



keys = ["rotate", "crop", "blur", "flip", "text", "min", "contour",
        "enhance", "emboss", "grayscale", "invert", "contrast", "solarize",
        "edges", "repeat", "max", "median", "resize", "brightness", "blend",
        "hue", "r","g","b", "wave", "glitch","mirror","pixel","square_crop"]


def handle(twitter, tweet, root_tweet, commands):
    global value
    global key
    global res
    
    media_ids = []
    entities = root_tweet.extended_entities["media"]
    
    try:

        for media in entities:
            urllib.request.urlretrieve(media["media_url"], "img.png")

            cmd : cmds.Command = cmds.Command(PillImage.open("img.png").convert("RGB"), entities, twitter, tweet)

            command_list = {
                "rotate": cmd.rotate,
                "crop": cmd.crop,
                "blur": cmd.blur,
                "flip": cmd.flip,
                "text": cmd.text,
                "min": cmd.min,
                "contour": cmd.contour,
                "enhance": cmd.enhance,
                "emboss": cmd.emboss,
                "grayscale": cmd.grayscale,
                "invert": cmd.invert,
                "contrast": cmd.contrast,
                "solarize": cmd.solarize,
                "edges": cmd.edges,
                "repeat": cmd.repeat,
                "max": cmd.max,
                "median": cmd.median,
                "resize": cmd.resize,
                "brightness": cmd.brightness,
                "blend": cmd.blend,
                "hue": cmd.hue,
                "r": cmd.r,
                "g": cmd.g,
                "b": cmd.b,
                "wave": cmd.wave,
                "glitch": cmd.glitch,
                "mirror": cmd.mirror,
                "pixel": cmd.pixel,
                "square_crop": cmd.square_crop
            }


            for command in commands:
                if not "=" in command:
                    continue

                command = command.split("=")

                if len(command) < 2:
                    continue

                key = command[0].strip()
                value = command[1].strip()

                if not key in keys:
                    raise Exception(f"there is no '{key}' command please read https://github.com/annasajkh/Commands/blob/main/README.org")
                
                if "blend" in commands and len(commands) > 1:
                    raise Exception("blend cannot be chain with other command")
                
                command_list[key](value)
            
            cmd.img.save("img.png")
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
