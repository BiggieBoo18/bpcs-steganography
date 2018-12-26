import numpy as np

from PIL import Image

def read_as_numpy(path):
    img = Image.open(path) # read img
    arr = np.array(img)    # convert to numpy array
    return arr

def to_bitplane(arr):
    if len(arr.shape)==3: # 3 channels (R, G, B)
        arr = np.unpackbits(arr, axis=2) # [[[128,128,128]...]...] => [[[100000001000000010000000]...]...]
        arr = arr.reshape(arr.shape[:2]+(3, 8, )) # divide each color (h, w, 24) => (h, w, 3, 8)
        bitplane = np.zeros(arr.shape+(8,), dtype="uint8") # (h, w, 3(color), 8(byte), 8(bitplane))
        for i in range(8):
            bitplane[:,:,:,:,i] = np.unpackbits(np.left_shift(arr[:,:,:,i].reshape(arr.shape[:2]+(3,1,)), i), axis=3) # arr[:, :, :, i] =>reshape=> (h, w, 3, 1) =>left_shift=>unpackbits=> (h, w, 3, i, 8)
        return bitplane
    # elif len(arr.shape)==2:
    #     return np.unpackbits(arr, axis=1)
    else:
        print("Unsupported shape of image")
        exit(1)
    return None

def to_image(arr):
    if len(arr.shape)==5: # 3 channels (R, G, B)
        img = np.zeros(arr.shape[:2]+(3, 8,), dtype="uint8") # (h, w, 3, 8)
        for i in range(8):
            img[:,:,:,7-i] = np.packbits(arr[:,:,:,i], axis=3).reshape(arr.shape[:3])
        img[img>0] = 1
        img = img.reshape(img.shape[:2]+(24,))
        img = np.packbits(img, axis=2)
        return img
    else:
        print("Unsupported shape of image")
        exit(1)
    return None

def pbc_to_cgc(arr):
    """
    ref:http://datahide.org/BPCSj/pbc-vs-cgc-j.html
    """
    arr = np.unpackbits(arr, axis=2).reshape(arr.shape[:2]+(3,8,))
    cgc = arr.copy()
    for i in range(1, 8):
        cgc[:,:,:,i] = np.logical_xor(arr[:,:,:,i-1], arr[:,:,:,i]) # gi = bi-1^bi
    cgc = np.packbits(cgc.reshape(cgc.shape[:2]+(3*8, )), axis=2)
    return cgc

def cgc_to_pbc(arr):
    """
    ref:http://datahide.org/BPCSj/pbc-vs-cgc-j.html
    """
    arr = np.unpackbits(arr, axis=2).reshape(arr.shape[:2]+(3,8,))
    pbc = arr.copy()
    for i in range(1, 8):
        pbc[:,:,:,i] = np.logical_xor(arr[:,:,:,i], pbc[:,:,:,i-1]) # bi = gi^bi-1
    pbc = np.packbits(pbc.reshape(pbc.shape[:2]+(3*8, )), axis=2)
    return pbc

def extract_bitplane(arr, color, bit):
    bitplane = np.packbits(arr[:,:,:,bit], axis=3)        # (h,w,color,byte,bitplane)=>(h,w,color,1)
    bitplane = bitplane[:,:,color].reshape(arr.shape[:2]) # (h,w,color,1)=>(h,w)
    bitplane[bitplane>0] = 1
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
