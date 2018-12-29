import sys
import numpy as np
import bpcs  as bp

from PIL import Image

if len(sys.argv)<4:
    print("USAGE: {0} <PATH> <COLOR> <BIT>".format(sys.argv[0]))
    print("    PATH:  image path")
    print("    COLOR: GRAY=-1, RED=0, GREEN=1, BLUE=2")
    print("    BIT  : 0~7 (0:MSB, 7:LSB)")
    exit(1)

PATH  = sys.argv[1]
COLOR = int(sys.argv[2])
BIT   = int(sys.argv[3])

arr = bp.read_image_as_numpy(PATH)
# arr = bp.pbc_to_cgc(arr)
arr = bp.to_binary(arr)
if len(arr.shape)<2 or len(arr.shape)>3:
    print("Unsupported shape of image")
    exit(1)

# image complexity
bitplane = bp.extract_bitplane(arr, COLOR, BIT) # extract bitplane as binary, shape is (h, w)
cpx      = bp.complexity(bitplane)
print("image complexity =", cpx)

# block complexity
for i, (x, y, block) in enumerate(bp.get_block_as_iter(bitplane, (8,8))):
    cpx = bp.complexity(block)
    print("block[{0}] complexity =".format(i), cpx)
