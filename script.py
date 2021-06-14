import cmds
from PIL import Image

img = Image.open('cat.png')

cmds.commands_list['multi']('0;0;100;50;grayscale=true', img).save('out.png')
