import sys
import numpy as np
import bpcs  as bp

from PIL import Image

if len(sys.argv)<2:
    print("USAGE: {0} <PATH>".format(sys.argv[0]))
    print("    PATH:  encoded image path")
    exit(1)
    
PATH = sys.argv[1]

blocksize = (8,8)
ath       = 0.45 # complexity threshold

arr = bp.read_image_as_numpy(PATH)
arr = bp.to_binary(arr)
decoded = bp.decode(arr, blocksize, ath)
print("[decoded code]")
print(decoded)
