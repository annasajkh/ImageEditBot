import os
from PIL import Image
import cmds


img = Image.open('cat.png')

img = cmds.commands_list['multirand']('h;0;50;10;contrast=150', img)
img.save('out.png')

os.system('feh out.png')
