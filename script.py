import os
from PIL import Image
import numpy as np
from numpy.lib import math
from cmds import commands_list
import cmds

from PIL import ImageFilter

img = Image.open('cat.png')

img = commands_list["glitch"]("true",img)

img.save('out.png')

os.system('feh out.png')
