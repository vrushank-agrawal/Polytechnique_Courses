# --------------------------------------------------------------------
import huffman

# To write the binary huffman implementation in a more modular way, we
# will introduce two auxiliary classes BitInBuffer and BitOutBuffer
# below.  These provide an interface for accessing the input and the
# output as though they were streams of bits, by doing some bitwise
# arithmetic "under the hood".

# --------------------------------------------------------------------
class EndOfBuffer(Exception):
    pass

class BitInBuffer:
    def __init__(self, data):
        self._pos  = (0, 0)
        self._data = data

    @staticmethod
    def _next_position(pos, bpos):
        return (pos + (bpos + 1) // 8, (bpos + 1) % 8)

    def remaining(self):
        return 8 * (len(self._data) - self._pos[0]) - self._pos[1]

    def empty(self):
        return self.remaining() == 0

    def sync(self):
        if self._pos[1] != 0:
            self._pos = (self._pos[0] + 1, 0)

    def pop_bit(self):
        if self.remaining() < 1:
            raise EndOfBuffer
        b = (self._data[self._pos[0]] >> (7-self._pos[1])) & 0b1
        self._pos = BitInBuffer._next_position(*self._pos)
        return b

    def pop_bytes(self, n):
        assert 0 <= n
        if self.remaining() < 8 * n:
            raise EndOfBuffer
        if self._pos[1] == 0:
            # We are aligned
            self._pos = (self._pos[0] + n, 0)
            return self._data[self._pos[0] - n:self._pos[0]]
        aout, (c, b) = bytearray(), self._pos
        for i in range(n):
            aout.append(
                ( (self._data[c+i  ] <<    b) & 0xff)
                | (self._data[c+i+1] >> (8-b)       ))
        self._pos = (c+n, b); return bytes(aout)
        
    def pop_byte(self):
        return self.pop_bytes(1)[0]

# --------------------------------------------------------------------
class BitOutBuffer:
    def __init__(self):
        self._data = bytearray()
        self._bpos = 8

    def pad(self):
        if self._bpos != 8:
            self.push_bits(0, 8 - self._bpos)
            self._bpos = 8

    def contents(self):
        return bytes(self._data)

    def push_bit(self, b):
        self.push_bits(1, int(b))

    def push_bits(self, n, bs):
        bs &= (1 << n) - 1

        if self._bpos > 0 and self._bpos < 8:
            rem = 8 - self._bpos
            if n <= rem:
                self._data[-1] |= bs << (rem - n)
                self._bpos += n
            else:
                self._data[-1] |= bs >> (n - rem)
                self._bpos += rem
            n -= min(n, rem)

        while n >= 8:
            self._data.append((bs >> (n - 8)) & 0xff)
            n -= 8

        if n > 0:
            self._data.append((bs << (8 - n)) & 0xff)
            self._bpos = n
            
    def push_byte(self, b):
        self.push_bytes(bytes([b]))

    def push_bytes(self, bs):
        if not bs:
            return
        if self._bpos == 8:
            # We are aligned
            self._data.extend(bs)
        else:
            for b in bs:
                b &= 0xff
                self._data[-1] |= b >> self._bpos
                self._data.append((b << (8 - self._bpos)) & 0xff)


# Now we can write bhuffman_bcodes, bhuffman_encode, and
# bhuffman_decode very similarly to how we wrote their non-binary
# versions, using auxiliary functions.
                
# --------------------------------------------------------------------
def _huffman_bcodes(node, depth, code, codes):
    if node is not None:
        if node.value is None:
            _huffman_bcodes(node.left , depth + 1, code << 1 | 0, codes)
            _huffman_bcodes(node.right, depth + 1, code << 1 | 1, codes)
        else:
            codes[node.value] = (depth, code)
    return codes

def huffman_bcodes(tree):
    return _huffman_bcodes(tree, 0, 0, {})

# --------------------------------------------------------------------
def _huffman_bencode_tree(node, buf):
    if node is not None:
        if node.value is None:
            buf.push_bit(0)
            _huffman_bencode_tree(node.left , buf)
            _huffman_bencode_tree(node.right, buf)
        else:
            buf.push_bit(1)
            buf.push_byte(ord(node.value))
    return buf

def huffman_bencode_tree(node):
    return _huffman_bencode_tree(node, BitOutBuffer()).contents()

# --------------------------------------------------------------------
def _huffman_bdecode_tree(buf):
    if buf.empty():
        return None
    if buf.pop_bit():
        return huffman.Node(chr(buf.pop_byte()))
    left  = _huffman_bdecode_tree(buf)
    right = _huffman_bdecode_tree(buf)
    return huffman.Node(None, left, right)

def huffman_bdecode_tree(data):
    return _huffman_bdecode_tree(BitInBuffer(data))

# --------------------------------------------------------------------
def _huffman_bencode(tree, s, buf):
    codes = huffman_bcodes(tree)
    for x in s:
        buf.push_bits(*codes[x])
    return buf

def huffman_bencode(tree, s):
    return _huffman_bencode(tree, s, BitOutBuffer()).contents()

# --------------------------------------------------------------------
def _huffman_bdecode(tree, buf, n):
    if n == 0:
        return ''
    if tree.value is not None:
        return tree.value * n

    aout = []
    for _ in range(n):
        current = tree
        while current.value is None:
            current = current.right if buf.pop_bit() else current.left
        aout.append(current.value)
    return ''.join(aout)

def huffman_bdecode(tree, data, n):
    return _huffman_bdecode(tree, BitInBuffer(data), n)

# --------------------------------------------------------------------
def huffman_bcompress(s):
    tree = huffman.huffman_tree(huffman.huffman_stats(s))
    buf  = BitOutBuffer()

    buf.push_bytes(int.to_bytes(len(s), 4, 'little'))
    _huffman_bencode_tree(tree, buf)
    buf.pad(); _huffman_bencode(tree, s, buf)

    return buf.contents()

# --------------------------------------------------------------------
class InvalidHuffmanStream(Exception):
    pass

def _huffman_buncompress(data):
    try:
        buf  = BitInBuffer(data)
        ln   = int.from_bytes(buf.pop_bytes(4), 'little')
        tree = _huffman_bdecode_tree(buf)

        buf.sync(); return (ln, tree, _huffman_bdecode(tree, buf, ln))

    except EndOfBuffer:
        raise InvalidHuffmanStream

def huffman_buncompress(data):
    return _huffman_buncompress(data)[-1]

# Now binary huffman compression is an actual text compression
# algorithm (as opposed to the non-binary version which is an
# anti-compression algorithm), although this is still only apparent
# for larger texts due to the overhead of storing the tree.

# Below are some examples:

# >>> import bhuffman
# >>> s = "Hello world! How are you doing these days?"
# >>> c = bhuffman.huffman_bcompress(s)
# >>> c
# b"*\x00\x00\x00\x16U\xce\xc2R\x16\x89\xfa\xf2\xba\xdaKz\xd9dH\x0b\xbd\xc8\x90\xdd\x16\xeb8AU7'j\xfc\xc99\x8f\xa34v\xb8\xff\xbf\xde\xa8\x10\xd6lK"
# >>> bhuffman.huffman_buncompress(c)
# 'Hello world! How are you doing these days?'
# >>> len(s)/len(c)
# 0.8571428571428571
# >>> s = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# >>> c = bhuffman.huffman_bcompress(s)
# >>> len(s)/len(c)
# 1.6481481481481481
# >>> s = "Lorem" * 1000
# >>> c = bhuffman.huffman_bcompress(s)
# >>> len(s)/len(c)
# 3.3090668431502315
