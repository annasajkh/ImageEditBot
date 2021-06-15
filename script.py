import os
from PIL import Image
import numpy as np
from numpy.lib import math
from cmds import commands_list
import cmds

from PIL import ImageFilter

img = Image.open('cat.png')

img = commands_list["resize"]("200;999999999999",img)

# img_arr = np.array(img)

# for i in range(img.height):
#     img_arr[i, :] = np.roll(img_arr[i, :],int(math.sin(i / 10) * math.cos(i) * 10),0)
#     img_arr[:, i] = np.roll(img_arr[:, i],int(math.cos(i/ 10) * math.sin(i) * 10),0)


#img = cmds.commands_list["multirand"]("v;0;50;10;contrast=200;blur=10",img)
# img = cmds.commands_list['multirand']('h;0;50;10;contrast=150', img)

img.save('out.png')

os.system('feh out.png')
