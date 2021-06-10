import html
import random
import numpy
import simpleeval
import edit_functions
import math
import urllib.request

from typing import Tuple
from PIL import Image as PillImage, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageEnhance


class Command:
    def __init__(self, img, entities, twitter, tweet):
        self.img = img
        self.entities = entities
        self.twitter = twitter
        self.tweet = tweet
    
    def rotate(self, value):
        try:
            value = edit_functions.clamp(int(value), -360, 360)
        except:
            raise Exception("there is something wrong with rotate value")
        
        self.img = self.img.rotate(value)
    
    def crop(self,value):
        value = edit_functions.to_array(value, 4)

        self.img = self.img.crop((value[0], value[1], value[2], value[3]))

    def blur(self, value):
        try:
            value = edit_functions.clamp(int(value), 0, 100)
        except:
            raise Exception("there is something wrong with blur value")

        self.img = self.img.filter(ImageFilter.GaussianBlur(value))
    
    def flip(self, value):
        if value == "h":
            self.img = self.img.transpose(PillImage.FLIP_LEFT_RIGHT)
        elif value == "v":
            self.img = self.img.transpose(PillImage.FLIP_TOP_BOTTOM)
        else:
            raise Exception("unknown argument")
    def text(self, value):
        value = value.split(";")

        try:
            value[1] = int(value[1])
            value[2] = int(value[2])
            value[3] = int(value[3])
        except:
            raise Exception("error while converting the values")
        
        draw = ImageDraw.Draw(self.img)
        draw.text((value[1], value[2]), value[0], (255,255,255),font=ImageFont.truetype("arial.ttf", value[3]))

    def min(self, value):
        try:
            value = edit_functions.clamp(int(value), 0, 17)
        except:
            raise Exception("there is something wrong with min value")

        self.img = self.img.filter(ImageFilter.MinFilter(value))
    
    def contour(self, value):
        if not value == "true":
            return
        
        self.img = self.img.filter(ImageFilter.CONTOUR)
    
    def enhance(self, value):
        if not value == "true":
            return
        
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    
    def emboss(self, value):
        if not value == "true":
            return
        
        self.img = self.img.filter(ImageFilter.EMBOSS)
    
    def grayscale(self, value):
        if not value == "true":
            return
    
        self.img = ImageOps.grayscale(self.img)
    
    def invert(self, value):
        if not value == "true":
            return
        
        self.img = ImageOps.invert(self.img)

    def contrast(self, value):
        try:
            value = edit_functions.clamp(int(value), -1000, 1000)
        except:
            raise Exception("there is something wrong with contrast value")
        
        self.img = edit_functions.change_contrast(self.img, value)
    
    def solarize(self, value):
        try:
            value = edit_functions.clamp(int(value), -100, 100)
        except:
            raise Exception("there is something wrong with solarize value")
        
        self.img = ImageOps.solarize(self.img, value)
    
    def edges(self, value):
        if not value == "true":
            return

        self.img = self.img.filter(ImageFilter.FIND_EDGES)
    
    def repeat(self, value):
        value = edit_functions.to_array(value, 2)

        self.img = self.img.resize((self.img.width // value[0], self.img.height // value[1]))
        self.img = edit_functions.get_concat_tile_repeat(self.img, value[0], value[1])
    
    def max(self, value):
        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with max value")

        self.img = self.img.filter(ImageFilter.MaxFilter(value))
    
    def median(self, value):
        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with median value")
            
        self.img = self.img.filter(ImageFilter.MedianFilter(value))
    
    def resize(self, value):
        value = edit_functions.to_array(value, 2)

        self.img = self.img.resize((edit_functions.clamp(value[0], 1, 8192), edit_functions.clamp(value[1], 1, 8192)))
    
    def brightness(self, value):
        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with brightness value")

        applier = ImageEnhance.Brightness(self.img)

        self.img = applier.enhance(value)
    
    def blend(self, value):
        try:
            value = float(value)
        except:
            raise Exception("there is something wrong with blend value")

        for i in range(len(self.entities) - 1):
            if i == 0:
                urllib.request.urlretrieve(self.entities[i]["media_url"], "img.png")
            if i < len(self.entities):
                urllib.request.urlretrieve(self.entities[i + 1]["media_url"], "img1.png")

            img = PillImage.open("img.png")
            img1 = PillImage.open("img1.png")
            img = edit_functions.blend(img, img1, value)
            img.save("img.png")

        r = self.twitter.media_upload("img.png")

        self.twitter.update_status(media_ids=[r.media_id], in_reply_to_status_id=self.tweet.id,
                            auto_populate_reply_metadata=True)
    def r(self, value):
        pixels = self.img.load()

        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                if type(pixels[i, j]) == tuple:
                    pixels[i, j] = (simpleeval.simple_eval(html.unescape(value), names={
                                        "r": pixels[i, j][0],
                                        "g": pixels[i, j][1],
                                        "b": pixels[i, j][2]
                                    }),
                                    pixels[i, j][1],
                                    pixels[i, j][2])
                else:
                        pixels[i, j] = simpleeval.simple_eval(html.unescape(value), names={
                                        "r": pixels[i, j]
                                    })
    
    def g(self, value):
        pixels = self.img.load()

        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):

                if type(pixels[i, j]) == tuple:
                    pixels[i, j] = (pixels[i, j][0],
                                    simpleeval.simple_eval(html.unescape(value), names={
                                        "r": pixels[i, j][0],
                                        "g": pixels[i, j][1],
                                        "b": pixels[i, j][2]
                                    }),
                                    pixels[i, j][2])
                else:
                        pixels[i, j] = simpleeval.simple_eval(html.unescape(value), names={
                                        "g": pixels[i, j]
                                    })
    def b(self, value):
        pixels = self.img.load()

        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):

                if type(pixels[i, j]) == tuple:
                    pixels[i, j] = (pixels[i, j][0],
                                    pixels[i, j][1],
                                    simpleeval.simple_eval(html.unescape(value), names={
                                        "r": pixels[i, j][0],
                                        "g": pixels[i, j][1],
                                        "b": pixels[i, j][2]
                                    })
                                    
                                    )
                else:
                        pixels[i, j] = simpleeval.simple_eval(html.unescape(value), names={
                                        "b": pixels[i, j]
                                    })

    def hue(self, value):
        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with hue value")

        HSV = self.img.convert("HSV")
        H, S, V = HSV.split()
        H = H.point(lambda x : value)
        self.img = PillImage.merge("HSV", (H, S, V)).convert("RGB")

    def wave(self, value):
        value = edit_functions.to_array(value, 2)

        A = self.img.width / value[1]
        w = value[0] / self.img.height
        shift = lambda x: A * numpy.sin(2.0 * numpy.pi * x * w)

        arr = numpy.array(self.img)

        for i in range(self.img.width):
            arr[:, i] = numpy.roll(arr[:, i], int(shift(i)))

        self.img = PillImage.fromarray(arr)

    def glitch(self, value):
        if not value == "true":
            try:
                value = edit_functions.clamp(int(value), 0, 80)
            except:
                raise Exception("there is something wrong with glitch value")

            arr = numpy.array(self.img)

            for i in range(self.img.width):
                arr[:, i] = numpy.roll(arr[:, i], random.randrange(-value, value))

            self.img = PillImage.fromarray(arr)
        else:
            self.img = self.img.point(lambda x : random.randint(0, 256))
    
    def mirror(self,value):
        #value[0] = h or v
        #value[1] = right or left
        value = value.split(";")

        pixels = self.img.load()

        if value[0] == 'h':
            half_size_x = math.ceil(self.img.size[0] / 2)

            if value[1] == "right":
                for i in range(self.img.size[0]):
                    for j in range(self.img.size[1]):
                        if i <= half_size_x:
                            pixels[i, j] = pixels[(half_size_x - i ) + half_size_x,j]
            elif value[1] == "left":
                for i in range(self.img.size[0]):
                    for j in range(self.img.size[1]):
                        if i >= half_size_x:
                            pixels[i, j] = pixels[half_size_x - (i - half_size_x),j]
            else:
                raise Exception("unknown argument")
        elif value[0] == 'v':
            if value[1] == "right":
                for i in range(self.img.size[0]):
                    for j in range(self.img.size[1]):
                        pass
            elif value[1] == "left":
                pass
            else:
                raise Exception("unknown argument")
        else:
            raise Exception("unknown argument")