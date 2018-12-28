import numpy as np

from PIL import Image

SHINOBI = np.array([ord(c) for c in "SHINOBI"], dtype=np.uint8) # tail of secret data
TAIL    = np.array([ord(c) for c in "TAIL"],    dtype=np.uint8) # tail of conjuction map

def read_image_as_numpy(path):
    img = Image.open(path) # read img
    arr = np.array(img)    # convert to numpy array
    return arr

def padding(arr, blocksize):
    block_row,block_col = blocksize
    n_row = len(arr)
    lack_row = block_row-n_row%block_row
    if lack_row>0:
        wb = create_wb((lack_row, 8)) # ascii only,so 8bit. wb is [[1,0,1,0,1,0,1,0]*lack_row]
        arr = np.concatenate((arr, np.packbits(wb))) # concatenate arr and packed wb
    return arr

def read_message_as_numpy(path, blocksize):
    fp  = open(path, "r")
    msg = fp.read()
    msg = np.array([ord(c) for c in msg], dtype=np.uint8)
    msg = np.concatenate((msg, SHINOBI))
    msg = padding(msg, blocksize)
    fp.close()
    return msg

def to_binary(arr):
    if len(arr.shape)==3: # 3 channels (R, G, B)
        arr = np.unpackbits(arr, axis=2) # [[[128,128,128]...]...] => [[[100000001000000010000000]...]...]
        arr = arr.reshape(arr.shape[:2]+(3, 8, )) # divide each color (h, w, 24) => (h, w, 3, 8)
        return arr
    # elif len(arr.shape)==2:
    #     return np.unpackbits(arr, axis=1)
    elif len(arr.shape)==1:
        org = arr.shape             # original shape
        arr = np.unpackbits(arr)
        arr = arr.reshape(org+(8,)) # (original shape*bits) => (original shape, 8)
        return arr
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

def get_block_as_iter(bitplane, blocksize):
    n_rows, n_cols = bitplane.shape
    for y in range(0, n_rows, blocksize[0]):
        for x in range(0, n_cols, blocksize[1]):
            block = bitplane[y:y+blocksize[0], x:x+blocksize[1]]
            if block.shape==blocksize:
                yield x, y, block
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

def create_wb(size):
    if size[1]==1:
        return np.array([[1]*size[0]])
    wb = np.tile([1, 0], (size[0],size[1]))[:size[0], :size[1]]
    if len(wb[1::2])>0:
        wb[1::2] = 1-wb[1::2] # invert only odd rows
    return wb

def complication(block):
    wb = create_wb(block.shape)
    return np.uint8(np.logical_xor(block, wb))

def conjugation_map(arr, blocksize):
    # create conjugation map (NOTE: not complication)
    arr = np.concatenate((arr, TAIL))
    arr = padding(arr, blocksize)
    arr = to_binary(arr)
    conj_map = []
    for i, (x, y, block) in enumerate(get_block_as_iter(arr, blocksize)):
        conj_map.append(block)
    return conj_map
    
def secret_blocks(arr, blocksize, ath):
    # create secret blocks
    secret_blocks = []
    conj_map      = np.array([0]*int(arr.shape[0]/arr.shape[1]), dtype=np.uint8)
    for i, (x, y, block) in enumerate(get_block_as_iter(arr, blocksize)):
        cpx = complexity(block)
        if cpx<ath:
            block       = complication(block)
            conj_map[i] = 1
        secret_blocks.append(block)
    # create conjugation map (NOTE: not complication)
    conj_map = conjugation_map(conj_map, blocksize)
    return secret_blocks, conj_map

def encode(arr, secret_blocks, conj_map, blocksize, ath):
    secret_blocks = secret_blocks[:]
    conj_map      = conj_map[:]
    for color in range(3):
        for bit in (7, -1, -1):
            bitplane = extract_bitplane(arr, color, bit)
            for i, (x, y, block) in enumerate(get_block_as_iter(bitplane, blocksize)):
                if conj_map:
                    bitplane[y:y+blocksize[0], x:x+blocksize[1]] = conj_map.pop(0)
                elif complexity(block)>ath:
                    bitplane[y:y+blocksize[0], x:x+blocksize[1]] = secret_blocks.pop(0)
                if not secret_blocks:
                    break
            arr[:,:,color,bit] = bitplane
            if not secret_blocks:
                return arr
    return arr

def decode_block(block):
    decoded = np.packbits(block).tolist()
    decoded = "".join([chr(c) for c in decoded])
    return decoded

def decode(arr, blocksize, ath):
    conj     = True
    conj_map = []
    decoded  = ""
    shinobi  = "".join([chr(c) for c in SHINOBI])
    tail     = "".join([chr(c) for c in TAIL])
    for color in range(3):
        for bit in (7, -1, -1):
            bitplane = extract_bitplane(arr, color, bit)
            for x, y, block in get_block_as_iter(bitplane, blocksize):
                if conj:
                    decoded += decode_block(block)
                    if tail in decoded:
                        conj_map = [ord(c) for c in decoded[:decoded.index(tail)]]
                        conj     = False
                        decoded  = ""
                elif complexity(block)>ath:
                    if conj_map and conj_map.pop(0):
                        decoded += decode_block(complication(block))
                    else:
                        decoded += decode_block(block)
                    if shinobi in decoded:
                        return decoded[:decoded.index(shinobi)]
    return decoded
