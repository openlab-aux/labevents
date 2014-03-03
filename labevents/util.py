import string
import random

def random_string(char_count):
    return "".join([random.choice(string.ascii_letters+string.digits) 
                    for x in range(char_count)]) 
