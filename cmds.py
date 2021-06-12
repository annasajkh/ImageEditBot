import html
import random
import numpy
import simpleeval
import edit_functions
from multiprocessing import Pool
import urllib.request

from PIL import Image as PillImage, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageEnhance

value_global = ""

#wrapper to avoid can't pickle error
def modify_r(pixel):
    return (int(simpleeval.simple_eval(html.unescape(value_global), names={
                                        "r": pixel[0],
                                        "g": pixel[1],
                                        "b": pixel[2],
                                        "math":edit_functions.math_names
                                        })),
                                        pixel[1],
                                        pixel[2])

#wrapper to avoid can't pickle error
def modify_g(pixel):
    return (pixel[0],
            int(simpleeval.simple_eval(html.unescape(value_global), names={
                "r": pixel[0],
                "g": pixel[1],
                "b": pixel[2],
                "math":edit_functions.math_names
            })),
            pixel[2])

#wrapper to avoid can't pickle error
def modify_b(pixel):
    return (pixel[0],
            pixel[1],
            int(simpleeval.simple_eval(html.unescape(value_global), names={
                "r": pixel[0],
                "g": pixel[1],
                "b": pixel[2],
                "math":edit_functions.math_names
            })
            ))

class Command:
    def __init__(self, img, entities, twitter, tweet):
        self.img = img
        self.entities = entities
        self.twitter = twitter
        self.tweet = tweet
    
    def rotate(self, value):
        try:
            # convert value to int and clamp it between -360 -> 360
            value = edit_functions.clamp(int(value), -360, 360)
        except:
            raise Exception("there is something wrong with rotate value")
        
        self.img = self.img.rotate(value,expand=True)


    
    def crop(self,value):
        #convert value;value;value;value -> [value,value,value,value]
        value = edit_functions.to_array(value, 4)

        #convert all value array to int and clamp it between 0 - 100
        value[0] = edit_functions.clamp(int(value[0]),0,100)
        value[1] = edit_functions.clamp(int(value[1]),0,100)
        value[2] = edit_functions.clamp(int(value[2]),0,100)
        value[3] = edit_functions.clamp(int(value[3]),0,100)

        #calculate percentages x,y,width,height
        self.img = self.img.crop(  (value[0] / 100 * self.img.size[0], 
                                    value[1] / 100 * self.img.size[1], 
                                    value[2] / 100 * self.img.size[0], 
                                    value[3] / 100 * self.img.size[1]))

    def blur(self, value):
        try:
            #value = number
            # convert value to int and clamp it between -0 - 100
            value = edit_functions.clamp(int(value), 0, 100)
        except:
            raise Exception("there is something wrong with blur value")

        self.img = self.img.filter(ImageFilter.GaussianBlur(value))
    
    def flip(self, value):
        #value = true or false

        if value == "h":
            self.img = self.img.transpose(PillImage.FLIP_LEFT_RIGHT)
        elif value == "v":
            self.img = self.img.transpose(PillImage.FLIP_TOP_BOTTOM)
        else:
            raise Exception("unknown argument")
        
    def text(self, value):
        #value = string;number;number;number

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
        #value = number

        try:
            value = edit_functions.clamp(int(value), 0, 17)
        except:
            raise Exception("there is something wrong with min value")

        self.img = self.img.filter(ImageFilter.MinFilter(value))
    
    def contour(self, value):
        #value = true or false

        if not value == "true":
            return
        
        self.img = self.img.filter(ImageFilter.CONTOUR)
    
    def enhance(self, value):
        #value = true or false

        if not value == "true":
            return
        
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    
    def emboss(self, value):
        #value = true or false

        if not value == "true":
            return
        
        self.img = self.img.filter(ImageFilter.EMBOSS)
    
    def grayscale(self, value):
        #value = true or false

        if not value == "true":
            return
    
        self.img = ImageOps.grayscale(self.img)
    
    def invert(self, value):
        #value = true or false

        if not value == "true":
            return
        
        self.img = ImageOps.invert(self.img)

    def contrast(self, value):
        #value = number

        try:
            value = edit_functions.clamp(int(value), -1000, 1000)
        except:
            raise Exception("there is something wrong with contrast value")
        
        self.img = edit_functions.change_contrast(self.img, value)
    
    def solarize(self, value):
        #value = number

        try:
            value = edit_functions.clamp(int(value), -100, 100)
        except:
            raise Exception("there is something wrong with solarize value")
        
        self.img = ImageOps.solarize(self.img, value)
    
    def edges(self, value):
        #value = true or false

        if not value == "true":
            return

        self.img = self.img.filter(ImageFilter.FIND_EDGES)
    
    def repeat(self, value):
        #value = number;number

        value = edit_functions.to_array(value, 2)

        self.img = self.img.resize((self.img.width // value[0], self.img.height // value[1]))
        self.img = edit_functions.get_concat_tile_repeat(self.img, value[0], value[1])
    
    def max(self, value):
        #value = number

        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with max value")

        self.img = self.img.filter(ImageFilter.MaxFilter(value))
    
    def median(self, value):
        #value = number

        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with median value")
            
        self.img = self.img.filter(ImageFilter.MedianFilter(value))
    
    def resize(self, value):
        #value = number;number

        value = edit_functions.to_array(value, 2)

        self.img = self.img.resize((edit_functions.clamp(value[0], 1, 8192), edit_functions.clamp(value[1], 1, 8192)))
    
    def brightness(self, value):
        #value = number

        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with brightness value")

        applier = ImageEnhance.Brightness(self.img)

        self.img = applier.enhance(value)
    
    def blend(self, value):
        #value = number

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
        #value = expression

        global value_global

        value_global = value

        list_of_pixels = list(self.img.getdata())
        pool = Pool(4)
        new_list_of_pixels = pool.map(modify_r,list_of_pixels)

        pool.close()
        pool.join()
        self.img.putdata(new_list_of_pixels)

    
    def g(self, value):
        #value = expression

        global value_global

        value_global = value

        list_of_pixels = list(self.img.getdata())
        pool = Pool(4)
        new_list_of_pixels = pool.map(modify_g,list_of_pixels)

        pool.close()
        pool.join()
        self.img.putdata(new_list_of_pixels)

    def b(self, value):
        #value = expression

        global value_global

        value_global = value

        list_of_pixels = list(self.img.getdata())
        pool = Pool(4)
        new_list_of_pixels = pool.map(modify_b,list_of_pixels)

        pool.close()
        pool.join()
        self.img.putdata(new_list_of_pixels)

    def hue(self, value):
        #value = number
        try:
            value = int(value)
        except:
            raise Exception("there is something wrong with hue value")

        HSV = self.img.convert("HSV")
        H, S, V = HSV.split()
        H = H.point(lambda x : value)
        self.img = PillImage.merge("HSV", (H, S, V)).convert("RGB")

    def wave(self, value):
        #value = number;number
        value = edit_functions.to_array(value, 2)

        A = self.img.width / value[1]
        w = value[0] / self.img.height
        shift = lambda x: A * numpy.sin(2.0 * numpy.pi * x * w)

        arr = numpy.array(self.img)

        for i in range(self.img.width):
            arr[:, i] = numpy.roll(arr[:, i], int(shift(i)))

        self.img = PillImage.fromarray(arr)


    def glitch(self, value):
        #value = true or false
        if not value == "true":
            try:
                value = edit_functions.clamp(int(value), -256, 256)
            except:
                raise Exception("there is something wrong with glitch value")

            arr = numpy.array(self.img)

            for i in range(self.img.width):
                arr[:, i] = numpy.roll(arr[:, i], random.randrange(-value, value))

            self.img = PillImage.fromarray(arr)
        else:
            self.img = self.img.point(lambda x : random.randint(-256, 256))
    
    def mirror(self,value):
        #value = right or left or top or bottom

        pixels = self.img.load()

        half_size_x = self.img.size[0] // 2
        half_size_y = self.img.size[1] // 2

        if value == "left":
            for i in range(self.img.size[0]):
                for j in range(self.img.size[1]):
                    if i <= half_size_x:
                        pixels[i, j] = pixels[half_size_x - i + half_size_x - 1,j]
        elif value == "right":
            for i in range(self.img.size[0]):
                for j in range(self.img.size[1]):
                    if i >= half_size_x:
                        pixels[i, j] = pixels[half_size_x - (i - half_size_x),j]
        elif value == "top":
            for i in range(self.img.size[0]):
                for j in range(self.img.size[1]):
                    if j <= half_size_y:
                        pixels[i, j] = pixels[i,half_size_y - j + half_size_y - 1]
        elif value == "bottom":
            for i in range(self.img.size[0]):
                for j in range(self.img.size[1]):
                    if j >= half_size_y:
                        pixels[i, j] = pixels[i,half_size_y - (j - half_size_y)]
        else:
            raise Exception("unknown argument")

    def pixel(self, value):
        #value = expression

        self.img = self.img.point(lambda pixel: int(simpleeval.simple_eval(html.unescape(value), 
                                        names={
                                            "pixel":pixel,
                                            "math":edit_functions.math_names
                                            })))

    def square_crop(self, value):
        # value = number
        value = int(value)

        half_size_x = self.img.size[0] // 2
        half_size_y = self.img.size[1] // 2

        self.img = self.img.crop((  half_size_x - value,
                                    half_size_y - value,
                                    half_size_x + value,
                                    half_size_y + value))
    
    def binary(self, value):
        self.grayscale("true")
        value = int(value)
        pixels = self.img.load()
        
        for i in range(self.img.size[0]):
                for j in range(self.img.size[1]):
                    if pixels[i, j] >= value:
                        pixels[i, j] = 255
                    else:
                        pixels[i, j] = 0