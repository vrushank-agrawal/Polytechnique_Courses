# ----------------------------------------------------------------
# For convenience, we define a "smart" constructor that will build a
# composite quadtree from four subtrees, ensuring that the resulting
# tree is minimal in the case that the arguments are four uniform
# quadrants of the same color.
def composite(nw, ne, sw, se):
    nd = (nw, ne, sw, se)
    if all(n[0] == 'u' for n in nd):
        if len(set(n[1] for n in nd)) == 1:
            return ('u', nd[0][1])
    return ('c', nd)

# ----------------------------------------------------------------
def image_to_qtree(n, d):
    # We define an auxiliary function that converts the 2^k by 2^k subregion
    # of the image starting at row i, column j to a quadtree.  It can be
    # written using a simple recursion.
    def doit(k, i, j):
        # Base case (k == 0) => a single pixel is a uniform quadtree
        if k == 0:
            return ('u', d[i][j])
        # Recursive case (k > 0) => we compute the "midpoint" of the
        #   subregion, call ourselves recursively on the appropriate
        #   subsubregions, and finally combine the resulting quadtrees
        #   using our smart constructor `composite`.
        md = 1 << (k-1)
        nw = doit(k-1, i     , j     )
        ne = doit(k-1, i     , j + md)
        sw = doit(k-1, i + md, j     )
        se = doit(k-1, i + md, j + md)

        return composite(nw, ne, sw, se)

    # To compute the quadtree of the entire image, we call the
    # auxiliary function setting k = n and i = j = 0.
    return doit(n, 0, 0)

# ----------------------------------------------------------------
def qtree_to_image(n, q):
    # This version of qtree_to_image works in a similar way (but backwards)
    # to image_to_qtree, defining an auxiliary function that overwrites
    # a subregion of the image from a subtree of the quadtree.
    data = [[0] * (1 << n) for _ in range(1 << n)]

    def doit(k, i, j, node):
        if node[0] == 'c':
            md = 1 << (k-1)
            nw = doit(k-1, i     , j     , node[1][0])
            ne = doit(k-1, i     , j + md, node[1][1])
            sw = doit(k-1, i + md, j     , node[1][2])
            se = doit(k-1, i + md, j + md, node[1][3])
        else:
            for i0 in range(i, i + (1 << k)):
                for j0 in range(j, j + (1 << k)):
                    data[i0][j0] = node[1]

    doit(n, 0, 0, q); return data

def qtree_to_image_v2(n, q):
    # Here is an alternative version of qtree_to_image defined by
    # a direct recursion without using an auxiliary function.

    # Base case (uniform) => return a block of pixels of the same color.
    if q[0] == 'u':
        return [[q[1] for _ in range (1 << n)] for _ in range (1 << n)]
    assert (q[0] == 'c')
    # Recursive case (composite) => call ourselves recursively, then
    #   stitch the resulting images together by concatenating the
    #   rows of the western hemisphere and the eastern hemisphere.
    nw = qtree_to_image_v2(n-1, q[1][0])
    ne = qtree_to_image_v2(n-1, q[1][1])
    sw = qtree_to_image_v2(n-1, q[1][2])
    se = qtree_to_image_v2(n-1, q[1][3])
    return [wrow + erow for (wrow,erow) in zip(nw + sw, ne + se)]

# --------------------------------------------------------------------
def qtree_to_bits(node):
    if node[0] == 'u':
        return '01' if node[1] else '00'
    return '1' + ''.join(qtree_to_bits(q) for q in node[1])

# --------------------------------------------------------------------
def _bits_to_qtree(s, i):
    if i >= len(s):
        raise ValueError

    if s[i] == '1':
        nw, i = _bits_to_qtree(s, i+1)
        ne, i = _bits_to_qtree(s, i)
        sw, i = _bits_to_qtree(s, i)
        se, i = _bits_to_qtree(s, i)
        return ('c', (nw, ne, sw, se)), i

    if s[i] == '0':
        if i+1 == len(s):
            raise ValueError
        if s[i+1] == '0':
            return ('u', 0), i+2
        if s[i+1] == '1':
            return ('u', 1), i+2

    raise ValueError

# --------------------------------------------------------------------
def bits_to_qtree(s):
    node, i = _bits_to_qtree(s, 0)
    if i != len(s):
        raise ValueError
    return node

# --------------------------------------------------------------------
def inverse(q):
    if q[0] == 'u':
        return ('u', 1 - q[1])
    return ('c', tuple(inverse(q[1][i]) for i in range(4)))
    # or more verbosely but equivalently:
    # return ('c', (inverse(q[1][0]), inverse(q[1][1]), inverse(q[1][2]), inverse(q[1][3])))

# --------------------------------------------------------------------
def rotate(q):
    if q[0] == 'u':
        return q
    return composite(*(rotate(q[1][i]) for i in (2, 0, 3, 1)))

# --------------------------------------------------------------------
def zoom(q):
    # quadtrees may already be visualized at any resolution!
    return q

# --------------------------------------------------------------------
def fractal(k):
    if k <= 0:
        return ('u', 0)
    f, b = fractal(k-1), ('u', 1)

    return ('c', (
        ('c', (f, f, f, b)),
        ('c', (f, f, b, f)),
        ('c', (f, b, f, f)),
        ('c', (b, f, f, f)),
    ))
