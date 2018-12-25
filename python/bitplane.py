import numpy as np

from PIL import Image

def read_as_numpy(path):
    img = Image.open(path) # read img
    arr = np.array(img)    # convert to numpy array
    return arr

def to_bitplane(arr):
    if len(arr.shape)==3:
        return np.unpackbits(arr, axis=2) # [[[128,128,128]...]...] => [[[100000001000000010000000]...]...]
    # elif len(arr.shape)==2:
    #     return np.unpackbits(arr, axis=1)
    else:
        print("Unsupported shape of image")
        exit(1)

def complexity(arr):
    print(arr.shape)
    n_rows, n_cols = arr.shape[:2]
    max_cpx = ((n_rows-1)*n_cols)+((n_cols-1)*n_rows)
    k = 0
    for i in range(1, n_rows):
        print(np.any(np.logical_xor(arr[:,i], arr[:,i-1]), axis=1))
        # k += np.logical_xor(arr[:,i,:], arr[:,i-1,:])
        # print(k)
        exit()
    print(arr)

def pbc_to_cgc(arr):
    """
    ref:http://datahide.org/BPCSj/pbc-vs-cgc-j.html
    """
    arr = arr.reshape(arr.shape[:2]+(3, 8, )) # divide each color (h, w, 24) => (h, w, 3, 8)
    cgc = arr.copy()
    for i in range(1, 8):
        cgc[:,:,:,i] = np.logical_xor(arr[:,:,:,i-1], arr[:,:,:,i]) # gi = bi-1^bi
    cgc = cgc.reshape(cgc.shape[:2]+(3*8, ))
    return cgc

def cgc_to_pbc(arr):
    """
    ref:http://datahide.org/BPCSj/pbc-vs-cgc-j.html
    """
    arr = arr.reshape(arr.shape[:2]+(3, 8, )) # divide each color (h, w, 24) => (h, w, 3, 8)
    pbc = arr.copy()
    for i in range(1, 8):
        pbc[:,:,:,i] = np.logical_xor(arr[:,:,:,i], pbc[:,:,:,i-1]) # bi = gi^bi-1
    pbc = pbc.reshape(pbc.shape[:2]+(3*8, ))
    return pbc
