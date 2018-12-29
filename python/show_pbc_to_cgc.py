import sys
import numpy as np
import bpcs  as bp

from PIL import Image

if len(sys.argv)<2:
    print("USAGE: {0} <PATH>".format(sys.argv[0]))
    print("    PATH:  image path")
    exit(1)
    
PATH  = sys.argv[1]

arr = bp.read_image_as_numpy(PATH)
if len(arr.shape)<2 or len(arr.shape)>3:
    print("Unsupported shape of image")
    exit(1)
arr = bp.to_binary(arr)
arr = bp.pbc_to_cgc(arr)
# arr = bp.cgc_to_pbc(arr)
arr = bp.to_image(arr)
Image.fromarray(np.uint8(arr)).show()             # show image
# Image.fromarray(np.uint8(arr)).save("test.png") # save image
