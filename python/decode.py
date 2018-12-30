from argparse import ArgumentParser

from PIL import Image

import numpy as np
import bpcs  as bp

parser = ArgumentParser()
parser.add_argument("-i", "--image",  type=str, help="encoded image path", required=True)
parser.add_argument("-o", "--output", type=str, help="output text file path", required=True)
args = parser.parse_args()

blocksize = (8,8)
ath       = 0.45 # complexity threshold

arr = bp.read_image_as_numpy(args.image)
arr = bp.to_binary(arr)
decoded = bp.decode(arr, blocksize, ath)
print("[decoded code]")
print(decoded)
if decoded:
    fp = open(args.output, "w")
    fp.write(decoded)
    fp.close()
else:
    print("Invalid image!")
