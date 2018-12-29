from argparse import ArgumentParser

from PIL import Image

import numpy as np
import bpcs  as bp

parser = ArgumentParser()
parser.add_argument("-i", "--image",  type=str,       help="encoded image path")
parser.add_argument("-s", "--secret", type=str,       help="secret text file path")
parser.add_argument("-o", "--output", type=str,       help="output text file path")
parser.add_argument("--verbose", action="store_true", help="verbose")
args = parser.parse_args()

blocksize = (8,8)
ath       = 0.45 # complexity threshold

if args.image:
    arr = bp.read_image_as_numpy(args.image)
    arr = bp.to_binary(arr)

    COLOR = 1
    if len(arr.shape)==4: # RGB
        COLOR = 3
    elif len(arr.shape)==3: # gray-scale
        arr = arr.reshape(arr.shape[:2]+(1, arr.shape[2],))
        COLOR = 1
    else:
        print("Unsupported shape of image")
        exit(1)
    n_valid_blocks = 0
    for color in range(COLOR):
        for bit in (7, -1, -1):
            bitplane = bp.extract_bitplane(arr, color, bit)
            cpx      = bp.complexity(bitplane)
            if args.verbose:
                print("image complexity =", cpx)
            for i, (x, y, block) in enumerate(bp.get_block_as_iter(bitplane, blocksize)):
                cpx = bp.complexity(block)
                if args.verbose:
                    print("  block[{0}] complexity =".format(i), cpx)
                if cpx>ath:
                    n_valid_blocks += 1
    print("number of valid blocks =", n_valid_blocks)
    print("valid embed size       =", n_valid_blocks*blocksize[0]*blocksize[1], "bit")

if args.secret:
    arr = bp.read_message_as_numpy(args.secret, blocksize)
    arr = bp.to_binary(arr)
    secret_blocks, conj_map = bp.secret_blocks(arr, blocksize, ath)
    n_blocks = len(secret_blocks+conj_map)
    print("secret message size    =", n_blocks*blocksize[0]*blocksize[1], "bit")
