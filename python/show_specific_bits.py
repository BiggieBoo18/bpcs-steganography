import sys
import numpy as np

from PIL import Image
from bitplane import read_as_numpy, to_bitplane, to_image

if len(sys.argv)<4:
    print("USAGE: {0} <COLOR> <BIT>".format(sys.argv[0]))
    print("    PATH:  image path")
    print("    COLOR: RED=0, GREEN=1, BLUE=2")
    print("    BIT  : 0~7")
    exit(1)
    
PATH  = sys.argv[1]
COLOR = int(sys.argv[2])
BIT   = int(sys.argv[3])

def extract_bitplane(arr, color, bit):
    if color==0: # RED
        arr = np.pad(arr[:,:,color, bit], [(0,0),(0,0),(0,16)], "constant", constant_values=(0))
    elif color==1: # GREEN
        arr = np.pad(arr[:,:,color, bit], [(0,0),(0,0),(8,8)], "constant", constant_values=(0))
    elif color==2: # BLUE
        arr = np.pad(arr[:,:,color, bit], [(0,0),(0,0),(16,0)], "constant", constant_values=(0))
    else:
        print("Unknown color")
        exit(1)
    arr = np.packbits(arr.astype("uint8"), axis=2)
    arr[arr>0] = 255
    return arr

arr = read_as_numpy(PATH)
if len(arr.shape)<3:
    print("Unsupported shape of image")
    exit(1)
arr = to_bitplane(arr) # arr.shape = (h, w, 3(color), 8(byte), 8(bitplane))
# arr = to_image(arr)  # arr.shape = (h, w, 3)
arr = extract_bitplane(arr.copy(), COLOR, BIT)
Image.fromarray(np.uint8(arr)).show()             # show image
# Image.fromarray(np.uint8(arr)).save("test.png") # save image
