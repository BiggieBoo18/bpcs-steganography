import sys
import numpy    as np
import bitplane as bp

from PIL import Image

if len(sys.argv)<4:
    print("USAGE: {0} <COLOR> <BIT>".format(sys.argv[0]))
    print("    PATH:  image path")
    print("    COLOR: RED=0, GREEN=1, BLUE=2")
    print("    BIT  : 0~7 (0:MSB, 7:LSB)")
    exit(1)
    
PATH  = sys.argv[1]
COLOR = int(sys.argv[2])
BIT   = int(sys.argv[3])

def merge_bitplane_to_image(bitplane, arr, color):
    arr = bp.to_image(arr)
    img = np.zeros(arr.shape)
    img[:,:,color] = bitplane
    return img

arr = bp.read_image_as_numpy(PATH)
if len(arr.shape)<3:
    print("Unsupported shape of image")
    exit(1)
arr = bp.to_binary(arr) # arr.shape = (h, w, 3(color), 8(byte))
# arr = to_image(arr)  # arr.shape = (h, w, 3)
bitplane = bp.extract_bitplane(arr, COLOR, BIT)
bitplane[bitplane>0] = 255
img = merge_bitplane_to_image(bitplane, arr, COLOR)
Image.fromarray(np.uint8(img)).show()           # show image
# Image.fromarray(np.uint8(arr)).save("test.png") # save image
