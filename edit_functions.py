from typing import List
from PIL import Image as PillImage
import math

math_names = {

}
# get every function in math function except for if it has _ and put it in math_names
for math_func in dir(math):
    if not "_" in math_func:
        math_names[math_func] = getattr(math,math_func)

def blend(img1, img2, alpha):
    img2 = img2.resize(img1.size)

    return PillImage.blend(img1.convert("RGBA"), img2.convert("RGBA"), alpha)

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
