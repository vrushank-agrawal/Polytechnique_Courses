# --------------------------------------------------------------------
def uint16_to_bitstring(x):
    return [(x >> (15 - i)) & 0b1 for i in range(16)]

# an alternative implementation, which builds up the list of bits from
# right to left (i.e., starting with the least significant bits)
def uint16_to_bitstring_v2(x):
    w = [0]*16           # initialize an array of size 16
    for i in range(16):  
        w[15-i] = x & 1  # read the least significant bit of x
        x >>= 1          # shift all the bits right by 1 (== divide x by 2)
    return w

# --------------------------------------------------------------------
def bitstring_to_uint16(w):
    return sum(w[i] << (15-i) for i in range(16))

# an alternative implementation, which interprets the list of bits as
# an integer scanning from left to right (i.e., starting from the most
# significant bits)
def bitstring_to_uint16_v2(w):
    x = 0                     # initialize to 0
    for i in range(16):  
        x = (x << 1) + w[i]   # shift left by 1 (== multiply x by 2)
                              # and add the current bit
    return x

# --------------------------------------------------------------------
def mod_pow2(n, k):
    return n & ((1 << k) - 1)

# --------------------------------------------------------------------
def is_pow2(n):
    return (0 < n) and (n & (n - 1) == 0)

# --------------------------------------------------------------------
def set_mask(w, m):
    return w | m

# --------------------------------------------------------------------
def toggle_mask(w, m):
    return w ^ m

# --------------------------------------------------------------------
def clear_mask(w, m):
    return w & (~ m)
