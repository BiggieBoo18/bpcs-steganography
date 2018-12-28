import sys
import numpy as np
import bpcs  as bp

from PIL import Image

if len(sys.argv)<3:
    print("USAGE: {0} <IPATH> <SPATH>".format(sys.argv[0]))
    print("    IPATH:  image path")
    print("    SPATH:  secret file path")
    exit(1)
    
IPATH = sys.argv[1]
SPATH = sys.argv[2]

blocksize = (8,8)
ath       = 0.45 # complexity threshold

# prepare secret blocks
arr = bp.read_message_as_numpy(SPATH, blocksize)
arr = bp.to_binary(arr)
secret_blocks, conj_map = bp.secret_blocks(arr, blocksize, ath)

# encode
arr = bp.read_image_as_numpy(IPATH)
arr = bp.to_binary(arr)
arr = bp.encode(arr, secret_blocks, conj_map, blocksize, ath)
# print(arr[:,:,0,7][0:8,0:8])
arr = bp.to_image(arr)
# Image.fromarray(np.uint8(arr)).show()
Image.fromarray(np.uint8(arr)).save("images/encoded.png")
