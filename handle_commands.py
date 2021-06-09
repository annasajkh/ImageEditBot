import html
import random
import urllib.request

import numpy
import simpleeval
from PIL import Image as PillImage, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageEnhance

import edit_functions
import glob
import os

keys = ["rotate", "crop", "blur", "flip", "text", "min", "contour",
        "enhance", "emboss", "grayscale", "invert", "contrast", "solarize",
        "edges", "repeat", "max", "median", "resize", "brightness", "blend",
        "hue", "pixel", "wave", "glitch"]


def handle(twitter, tweet, root_tweet, commands):
    try:
        media_ids = []
        entities = root_tweet.extended_entities["media"]
        global value
        global key
        for media in entities:
            urllib.request.urlretrieve(media["media_url"], "img.png")
            img: PillImage.Image = PillImage.open("img.png")
            global res
            for command in commands:
                if not "=" in command:
                    continue

                command = command.split("=")
                if len(command) < 2:
                    continue
                key = command[0].strip()
                value = command[1].strip()
                if not key in keys:
                    twitter.update_status(
                        f"@{tweet.user.screen_name} there is no '{key}' command :( please read https://github.com/annasajkh/Commands/blob/main/README.md",
                        media_ids=media_ids,
                        in_reply_to_status_id=tweet.id)
                    return
                if "blend" in commands and len(commands) > 1:
                    witter.update_status(
                        f"@{tweet.user.screen_name} blend cannot be chain with other command",
                        media_ids=media_ids,
                        in_reply_to_status_id=tweet.id)
                    return

                if key == "rotate":
                    try:
                        value = edit_functions.clamp(int(value), -360, 360)
                    except:
                        continue
                    img = img.rotate(value)
                elif key == "crop":
                    value = edit_functions.convert_value(value, 4)
                    if value == "":
                        continue
                    img = img.crop((value[0], value[1], value[2], value[3]))
                elif key == "blur":
                    try:
                        value = edit_functions.clamp(int(value), 0, 100)
                    except:
                        continue
                    img = img.filter(ImageFilter.GaussianBlur(value))
                elif key == "flip":
                    if value == "h":
                        img = img.transpose(PillImage.FLIP_LEFT_RIGHT)
                    elif value == "v":
                        img = img.transpose(PillImage.FLIP_TOP_BOTTOM)
                    else:
                        continue
                elif key == "text":
                    value = value.split(";")
                    if value == "":
                        continue
                    try:
                        value[1] = int(value[1])
                        value[2] = int(value[2])
                        value[3] = int(value[3])
                    except:
                        continue
                    draw = ImageDraw.Draw(img)
                    draw.text((value[1], value[2]), value[0], font=ImageFont.truetype("arial.ttf", value[3]))
                elif key == "min":
                    try:
                        value = edit_functions.clamp(int(value), 0, 17)
                    except:
                        continue
                    img = img.filter(ImageFilter.MinFilter(value))
                elif key == "contour":
                    if not value == "true":
                        continue
                    img = img.filter(ImageFilter.CONTOUR)
                elif key == "enhance":
                    if not value == "true":
                        continue
                    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
                elif key == "emboss":
                    if not value == "true":
                        continue
                    img = img.filter(ImageFilter.EMBOSS)
                elif key == "grayscale":
                    if not value == "true":
                        continue
                    img = ImageOps.grayscale(img)
                elif key == "invert":
                    if not value == "true":
                        continue
                    img = ImageOps.invert(img)
                elif key == "contrast":
                    try:
                        value = edit_functions.clamp(int(value), -1000, 1000)
                    except:
                        continue
                    img = edit_functions.change_contrast(img, value)
                elif key == "solarize":
                    try:
                        value = edit_functions.clamp(int(value), -100, 100)
                    except:
                        continue
                    img = ImageOps.solarize(img, value)
                elif key == "edges":
                    if not value == "true":
                        continue
                    img = img.filter(ImageFilter.FIND_EDGES)
                elif key == "repeat":
                    value = edit_functions.convert_value(value, 2)
                    if value == "":
                        continue
                    img = img.resize((img.width // value[0], img.height // value[1]))
                    img = edit_functions.get_concat_tile_repeat(img, value[0], value[1])
                elif key == "max":
                    try:
                        value = int(value)
                    except:
                        continue
                    img = img.filter(ImageFilter.MaxFilter(value))
                elif key == "median":
                    try:
                        value = int(value)
                    except:
                        continue
                    img = img.filter(ImageFilter.MedianFilter(value))
                elif key == "resize":
                    value = edit_functions.convert_value(value, 2)
                    if value == "":
                        continue

                    img = img.resize((edit_functions.clamp(value[0], 1, 8192), edit_functions.clamp(value[1], 1, 8192)))
                elif key == "brightness":
                    try:
                        value = int(value)
                    except:
                        continue
                    applier = ImageEnhance.Brightness(img)
                    img = applier.enhance(value)
                elif key == "blend":
                    try:
                        value = float(value)
                    except:
                        continue
                    for i in range(len(entities) - 1):
                        if i == 0:
                            urllib.request.urlretrieve(entities[i]["media_url"], "img.png")
                        if i < len(entities):
                            urllib.request.urlretrieve(entities[i + 1]["media_url"], "img1.png")
                        img = PillImage.open("img.png")
                        img1 = PillImage.open("img1.png")
                        img = edit_functions.blend(img, img1, value)
                        img.save("img.png")
                    r = twitter.media_upload("img.png")
                    twitter.update_status(media_ids=[r.media_id], in_reply_to_status_id=tweet.id,
                                          auto_populate_reply_metadata=True)
                    return
                elif key == "pixel":
                    try:
                        img = img.point(
                            lambda pixel: simpleeval.simple_eval(html.unescape(value), names={"pixel": pixel}))
                    except:
                        continue
                elif key == "hue":
                    try:
                        value = int(value)
                    except:
                        continue
                    HSV = img.convert("HSV")
                    H, S, V = HSV.split()
                    H = H.point(lambda p: value)
                    img = PillImage.merge("HSV", (H, S, V)).convert("RGB")
                elif key == "wave":
                    value = edit_functions.convert_value(value, 2)
                    if value == "":
                        continue
                    A = img.width / value[1]
                    w = value[0] / img.height
                    shift = lambda x: A * numpy.sin(2.0 * numpy.pi * x * w)

                    arr = numpy.array(img)
                    for i in range(img.width):
                        arr[:, i] = numpy.roll(arr[:, i], int(shift(i)))
                    img = PillImage.fromarray(arr)
                elif key == "glitch":
                    if not value == "true":
                        try:
                            value = edit_functions.clamp(int(value), 0, 80)
                        except:
                            continue
                        arr = numpy.array(img)
                        for i in range(img.width):
                            arr[:, i] = numpy.roll(arr[:, i], random.randrange(-value, value))
                        img = PillImage.fromarray(arr)
                    else:
                        img = img.point(lambda pixel: random.randint(0, 256))
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
        except:
            print("hmm")
