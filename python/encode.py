from argparse import ArgumentParser

from PIL import Image

import numpy as np
import bpcs  as bp

parser = ArgumentParser()
parser.add_argument("-i", "--image",  type=str, help="dummy image path")
parser.add_argument("-s", "--secret", type=str, help="secret message text file path")
parser.add_argument("-o", "--output", type=str, help="output image path")
args = parser.parse_args()

blocksize = (8,8)
ath       = 0.45 # complexity threshold

# prepare secret blocks
arr = bp.read_message_as_numpy(args.secret, blocksize)
arr = bp.to_binary(arr)
secret_blocks, conj_map = bp.secret_blocks(arr, blocksize, ath)

# encode
arr = bp.read_image_as_numpy(args.image)
arr = bp.to_binary(arr)
arr = bp.encode(arr, secret_blocks, conj_map, blocksize, ath)
if arr:
    arr = bp.to_image(arr)
    Image.fromarray(np.uint8(arr)).show()
    Image.fromarray(np.uint8(arr)).save(args.output)
else:
    print("Invalid dummy image size or secret file size!")
