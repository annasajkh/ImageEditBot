import cmds
from PIL import Image

img = Image.open('cat.png')

cmds.commands_list['multi']('5;5;100;50;impact=woah:contrast=30:blur=20;contrast=50:max=17', img).save('out.png')
