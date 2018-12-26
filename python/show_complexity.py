import sys
import numpy    as np
import bitplane as bp

from PIL import Image

if len(sys.argv)<4:
    print("USAGE: {0} <PATH>".format(sys.argv[0]))
    print("    PATH:  image path")
    print("    COLOR: RED=0, GREEN=1, BLUE=2")
    print("    BIT  : 0~7")
    exit(1)
    
PATH  = sys.argv[1]
COLOR = int(sys.argv[2])
BIT   = int(sys.argv[3])

arr = bp.read_as_numpy(PATH)
# arr = bp.pbc_to_cgc(arr)
arr = bp.to_bitplane(arr)
if len(arr.shape)<3:
    print("Unsupported shape of image")
    exit(1)

# image complexity
bitplane = bp.extract_bitplane(arr, COLOR, BIT) # extract bitplane as binary, shape is (h, w)
cpx      = bp.complexity(bitplane)
print("image complexity =", cpx)

# block complexity
for i, block in enumerate(bp.get_block_as_iter(arr, (8,8), COLOR, BIT)):
    cpx = bp.complexity(block)
    print("block[{0}] complexity =".format(i), cpx)
