import numpy as np

from PIL import Image

def read_as_numpy(path):
    img = Image.open(path) # read img
    arr = np.array(img)    # convert to numpy array
    return arr

def to_binary(arr):
    if len(arr.shape)==3: # 3 channels (R, G, B)
        arr = np.unpackbits(arr, axis=2) # [[[128,128,128]...]...] => [[[100000001000000010000000]...]...]
        arr = arr.reshape(arr.shape[:2]+(3, 8, )) # divide each color (h, w, 24) => (h, w, 3, 8)
        return arr
    # elif len(arr.shape)==2:
    #     return np.unpackbits(arr, axis=1)
    else:
        print("Unsupported shape of image")
        exit(1)
    return None

def to_image(arr):
    if len(arr.shape)==4: # for 3 channels (R, G, B)
        arr = arr.reshape(arr.shape[:2]+(arr.shape[2]*arr.shape[3],)) # (h, w, 3, 8) => (h, w, 24)
        arr = np.packbits(arr, axis=2)
        return arr
    else:
        print("Unsupported shape of image")
        exit(1)
    return None

def pbc_to_cgc(arr):
    """
    ref:http://datahide.org/BPCSj/pbc-vs-cgc-j.html
    """
    if len(arr.shape)==3 and arr.shape[2]==3:
        print("Please first convert to binary. i.e. arr = to_binary(arr)")
        exit(1)
    cgc = arr.copy()
    for i in range(1, 8):
        cgc[:,:,:,i] = np.logical_xor(arr[:,:,:,i-1], arr[:,:,:,i]) # gi = bi-1^bi
    return cgc

def cgc_to_pbc(arr):
    """
    ref:http://datahide.org/BPCSj/pbc-vs-cgc-j.html
    """
    if len(arr.shape)==3 and arr.shape[2]==3:
        print("Please first convert to binary. i.e. arr = to_binary(arr)")
        exit(1)
    pbc = arr.copy()
    for i in range(1, 8):
        pbc[:,:,:,i] = np.logical_xor(arr[:,:,:,i], pbc[:,:,:,i-1]) # bi = gi^bi-1
    return pbc

def extract_bitplane(arr, color, bit):
    bitplane = arr[:,:,color,bit] # bitplane shape is (h, w) 2d array
    return bitplane

def get_block_as_iter(arr, blocksize, color, bit):
    bitplane = extract_bitplane(arr, color, bit) # extract bitplane as binary, shape is (h, w)
    n_rows, n_cols = bitplane.shape
    for y in range(0, n_rows, blocksize[0]):
        for x in range(0, n_cols, blocksize[1]):
            block = bitplane[y:y+blocksize[0], x:x+blocksize[1]]
            if block.shape==blocksize:
                yield block
    return None

def complexity(bitplane):
    n_rows, n_cols = bitplane.shape # bitplane shape is (h, w) 2d array
    max_cpx        = ((n_rows-1)*n_cols)+((n_cols-1)*n_rows) # max complexity
    k              = 0
    xor  = np.logical_xor(bitplane[1:], bitplane[:-1])       # row complexity
    k   += len(xor[xor==True])
    xor  = np.logical_xor(bitplane[:,1:], bitplane[:,:-1])   # col complexity
    k   += len(xor[xor==True])
    return k/max_cpx*1.0
