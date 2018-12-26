import sys
import numpy as np

from PIL import Image
from bitplane import read_as_numpy, to_binary, to_image, pbc_to_cgc, cgc_to_pbc

if len(sys.argv)<2:
    print("USAGE: {0} <PATH>".format(sys.argv[0]))
    print("    PATH:  image path")
    exit(1)
    
PATH  = sys.argv[1]

arr = read_as_numpy(PATH)
if len(arr.shape)<3:
    print("Unsupported shape of image")
    exit(1)
arr = to_binary(arr)
arr = pbc_to_cgc(arr)
# arr = cgc_to_pbc(arr)
arr = to_image(arr)
Image.fromarray(np.uint8(arr)).show()             # show image
# Image.fromarray(np.uint8(arr)).save("test.png") # save image
