import os
from Tkinter import Tk
from tkFileDialog import askopenfilename

from PIL import Image, ImageDraw

#import Image
#import ImageDraw

def get_user_art():
    Tk().withdraw() #stop Tk's root window
    # show an "Open" dialog box and return the path to the selected file
    filename = askopenfilename()
    print("user requested art %s" % (filename))

    im = Image.open(filename)
    size = 24,24
    im.thumbnail(size)

    filename = "tmp_user_art.png"
    filepath = os.path.join('data', filename)
    im.save(filepath)
    
    add_alpha(filepath)
    return filename

def add_alpha(filepath):

    im = Image.open(filepath)
    transparent_area = (0,0,0,0)

    mask=Image.new('L', im.size, color=255)
    draw=ImageDraw.Draw(mask) 
    draw.rectangle(transparent_area, fill=0)
    im.putalpha(mask)
    im.save(filepath)

if __name__ == '__main__':
    print get_user_art()

