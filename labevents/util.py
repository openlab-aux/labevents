import string
import random

import Image

def random_string(char_count):
    return "".join([random.choice(string.ascii_letters+string.digits) 
                    for x in range(char_count)]) 
    
def crop_square_image(file):
    i = Image.open(file)
    width, height = i.size
    delta = abs(width-height)
    if width > height:
        left = delta/2
        right = width-delta/2
        upper = 0
        lower = height
    else:
        left = 0
        right = width
        upper = delta/2
        lower = height-delta/2
        
    i = i.crop((left, upper, right, lower))
    return i
