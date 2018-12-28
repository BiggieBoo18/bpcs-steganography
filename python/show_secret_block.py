import sys
import numpy as np
import bpcs  as bp

from PIL import Image

if len(sys.argv)<2:
    print("USAGE: {0} <PATH>".format(sys.argv[0]))
    print("    PATH:  secret file path")
    exit(1)
    
PATH = sys.argv[1]

blocksize = (8,8)
ath       = 0.45 # complexity threshold

arr  = bp.read_message_as_numpy(PATH, blocksize)
arr  = bp.to_binary(arr)
for x, y, block in bp.get_block_as_iter(arr, blocksize):
    cpx = bp.complexity(block)
    print(block)
    print(block.shape)
    print("original complexity  =", cpx)
    if cpx<ath:
        block = bp.complication(block)
        print("converted complexity =", bp.complexity(block))
    print("="*30)
