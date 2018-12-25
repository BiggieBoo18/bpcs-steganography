import sys
import numpy as np

from PIL import Image
from bitplane import read_as_numpy, to_bitplane

if len(sys.argv)<4:
    print("USAGE: {0} <COLOR> <BIT>".format(sys.argv[0]))
    print("    PATH:  image path")
    print("    COLOR: RED=0, GREEN=1, BLUE=2")
    print("    BIT  : 0~7")
    exit(1)
    
PATH  = sys.argv[1]
COLOR = int(sys.argv[2])
BIT   = int(sys.argv[3])

def create_mask(arr, color):
    msk = np.zeros(arr.shape, dtype=np.uint8) # create mask
    return msk

def extract_bitplane(arr, color, bit):
    msk = create_mask(arr, color)
    msk[:,:,color] = msk[:,:,color]+2**bit    # extract specific bits
    arr = to_bitplane(arr)
    msk = to_bitplane(msk)
    arr = np.logical_and(arr, msk)            # arr = arr&mask
    arr = np.packbits(arr, axis=2)
    arr[arr==2**bit] = 255
    return arr

arr = read_as_numpy(PATH)
if len(arr.shape)<3:
    print("Unsupported shape of image")
    exit(1)
arr = extract_bitplane(arr.copy(), COLOR, BIT)
Image.fromarray(np.uint8(arr)).show()             # show image
# Image.fromarray(np.uint8(arr)).save("test.png") # save image
