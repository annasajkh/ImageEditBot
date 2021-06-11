import random
from typing import List
from PIL import Image as PillImage
import math

math_names = {

}

for math_func in dir(math):
    if not "_" in math_func:
        math_names[math_func] = getattr(math,math_func)

def blend(img1, img2, alpha):
    img2 = img2.resize(img1.size)
    return PillImage.blend(img1.convert("RGBA"), img2.convert("RGBA"), alpha)


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def to_array(value, min_length):
    value : List = value.split(";")

    if len(value) < min_length:
        raise Exception("not enough arguments")
    
    try:
        #loop each list of string and convert it to int
        for i in range(len(value)):
            value[i] = value[i].strip()
            value[i] = int(value[i])
    except Exception as e:
        raise Exception("error while converting values")
    
    return value


def get_concat_h_repeat(img, column):
    result = PillImage.new("RGB", (img.width * column, img.height))
    for x in range(column):
        result.paste(img, (x * img.width, 0))
    return result


def get_concat_v_repeat(img, row):
    result = PillImage.new("RGB", (img.width, img.height * row))
    for x in range(row):
        result.paste(img, (0, x * img.height))
    return result


def get_concat_tile_repeat(img, column, row):
    result_h = get_concat_h_repeat(img, column)
    return get_concat_v_repeat(result_h, row)


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        value = 128 + factor * (c - 128)
        return max(0, min(255, value))

    return img.point(contrast)
