import cmds
import urllib.request
import glob
import os

from PIL import Image as PillImage

keys = ["rotate", "crop", "blur", "flip", "text", "min", "contour",
        "enhance", "emboss", "grayscale", "invert", "contrast", "solarize",
        "edges", "repeat", "max", "median", "resize", "brightness", "blend",
        "hue", "r","g","b", "wave", "glitch","mirror","pixel"]


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

            for command in commands:
                if not "=" in command:
                    continue

                command = command.split("=")

                if len(command) < 2:
                    continue

                key = command[0].strip()
                value = command[1].strip()

                if not key in keys:
                    raise Exception(f"there is no '{key}' command please read https://github.com/annasajkh/Commands/blob/main/README.md")
                
                if "blend" in commands and len(commands) > 1:
                    raise Exception("blend cannot be chain with other command")

                if key == "rotate":
                    cmd.rotate(value)

                elif key == "crop":
                    cmd.crop(value)

                elif key == "blur":
                    cmd.blur(value)

                elif key == "flip":
                    cmd.flip(value)

                elif key == "text":
                    cmd.text(value)

                elif key == "min":
                    cmd.min(value)

                elif key == "contour":
                    cmd.contour(value)

                elif key == "enhance":
                    cmd.enhance(value)

                elif key == "emboss":
                    cmd.emboss(value)

                elif key == "grayscale":
                    cmd.grayscale(value)

                elif key == "invert":
                    cmd.invert(value)

                elif key == "contrast":
                    cmd.contrast(value)

                elif key == "solarize":
                    cmd.solarize(value)

                elif key == "edges":
                    cmd.edges(value)

                elif key == "repeat":
                    cmd.repeat(value)

                elif key == "max":
                    cmd.max(value)

                elif key == "median":
                    cmd.median(value)
                    
                elif key == "resize":
                    cmd.resize(value)
                    
                elif key == "brightness":
                    cmd.brightness(value)

                elif key == "blend":
                    cmd.blend(value)

                    return
                elif key == "r":
                    cmd.r(value)

                elif key == "g":
                    cmd.g(value)

                elif key == "b":
                    cmd.b(value)

                elif key == "hue":
                    cmd.hue(value)

                elif key == "wave":
                    cmd.wave(value)
                    
                elif key == "glitch":
                    cmd.glitch(value)

                elif key == "mirror":
                    cmd.mirror(value)
                    
                elif key == "pixel":
                    cmd.pixel(value)
            
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
