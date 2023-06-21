# --------------------------------------------------------------------
import math

from heap import Heap

# --------------------------------------------------------------------
class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left  = left
        self.right = right

    def __repr__(self):
        return 'Node({}, {}, {})'.format(
            repr(self.value), self.left, self.right)

# --------------------------------------------------------------------
def huffman_stats(s):
    # We are first going to gather in `stats` the frequence of
    # occurence of all the single characters of `s`.
    stats = {}

    # We simply iterate over all the characters of `s`...
    for x in s:
        # ...and add `1` to `stats[x]`. Note that `stats.get(x, 0)`
        # returns `0` if `x` is not in `stats` -- this avoids us from
        # checking is `x` is in `stats` a priori.
        stats[x] = stats.get(x, 0) + 1

    # We then divide these frequencies by the length of `s` to
    # obtain the probabilities of appearance of the characters.
    return { x: v / len(s) for x, v in stats.items() }

# --------------------------------------------------------------------
def huffman_tree(freqs):
    # If the dictionary `freqs` is empty, we simply return an empty tree.
    if len(freqs) == 0:
        return None

    # Otherwise, we create an empty heap...
    heap = Heap()

    # ...that we populate with leaves, one of them per character `c`
    # appearing in `freqs`. We use the respective probabilities of
    # appearance for the weights.
    for x, p in freqs.items():
        heap.push(Node(x), p)

    # Then, while there are at least two nodes in the heap...
    while len(heap) > 1:
        # We pop two nodes with weights with lowest probabilities...
        n1, p1 = heap.pop()
        n2, p2 = heap.pop()

        # ...and push a new node:
        #
        #  - whose left and right children are the two nodes we just
        #    popped, and
        #  - whose weight is the sum of the weights of the two nodes we
        #    just popped.
        heap.push(Node(None, n1, n2), p1 + p2)

    # At that point, the heap only contains one element. We simply
    # return it (note the `[0]` that allows us to prune the associated
    # weight).
    return heap.pop()[0]

# --------------------------------------------------------------------
def _huffman_codes(node, code, codes):
    # The auxiliary function takes 3 parameters:
    #
    #  - `node`  : the node under consideration
    #  - `code`  : the path from the root node to `node`
    #  - `codes` : the dictionary where we will store the Huffman codes
    #
    # The parameter `code` is a string made of `0`s and `1`s, each
    # character (from left to right) indicating the choice we made
    # (left or right) when walking from the root to `node` -- where
    # `0` denotes "left" and `1` denotes "right".

    if node is not None:
        if node.value is None:
            # `node` is an internal node, i.e. it encodes no character.
            # This also means that the node has two children that we
            # must visit.

            # We hence visit the left child, extending `code` with `0`
            # since we go on the left...
            _huffman_codes(node.left , code + '0', codes)

            # ...and we visit the right child, extending `code` with `1
            # since we go on the right.
            _huffman_codes(node.right, code + '1', codes)
        else:
            # `node` is a leaf, i.e. it encodes the character `node.value`.
            #
            # We simply associate `code` to `node.value` in the table
            # `codes` -- remember that `code` is the path from the
            # root node to `node`.
            codes[node.value] = code

    return codes

def huffman_codes(tree):
    return _huffman_codes(tree, '', {})

# --------------------------------------------------------------------
def huffman_encode(tree, s):
    # We want to encode `d` under the Huffman tree `tree`.

    # We first compute the codes table from the Huffman tree.  I.e.,
    # `table[c]` contains the Huffman code of `c` for any character
    # `c` that is encoded by `tree`.
    table = huffman_codes(tree)

    # We then encode all the characters of `s` and concatenate the codes.
    return ''.join(table[x] for x in s)

# --------------------------------------------------------------------
def _huffman_decode1(node, s, i):
    # This function decodes one character from the "bit-string" `s`,
    # starting at position `i`. The parameter `node` is the Huffman
    # tree under consideration.

    # We walk down the tree, going on the left or on the right,
    # depending on the value `s[i]`. We stop when we reach a leaf
    # (i.e. when `node.value` is `None`).
    while node.value is None:
        assert i < len(s)
        node, i = (node.left if s[i] == '0' else node.right), i + 1

    # We are now at a left. We simply return the associated character,
    # along witht the new position `i` in `s`.
    return (node.value, i)

def huffman_decode(tree, s):
    i, aout = 0, []

    # We decode the character one by one, using `_huffman_decode1`,
    # storing the decoded characters in the list `aout`. The variable
    # `i` is the position of the next bit to be read from `s`.
    while i < len(s):
        c, i = _huffman_decode1(tree, s, i)
        aout.append(c)

    return ''.join(aout)

# --------------------------------------------------------------------
def huffman_compress(s):
    if s == '':
        return (None, '', 1)

    stats = huffman_stats(s)
    tree  = huffman_tree(stats)
    enc   = huffman_encode(tree, s)

    return (tree, enc, (8 * len(s)) / len(enc))
