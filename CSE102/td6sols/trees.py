#! /usr/bin/env python3

# --------------------------------------------------------------------
import math

# --------------------------------------------------------------------
class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left  = left
        self.right = right

# --------------------------------------------------------------------
T1 = Node(0, Node(1, Node(2), Node(3)), Node(4, Node(5)))
T2 = Node(0, Node(1), Node(2, Node(3), Node(4, Node(5))))
T3 = Node(11, Node(10, Node(9, None, Node(8)), Node(7)), Node(6))

# --------------------------------------------------------------------
def size(node):
    # We solve this problem recursively
    #
    #  - If node = None -> we have zero nodes
    #
    #  - Otherwise, we (recursively) count the number of nodes in
    #    resp. the left and right children and return their sum plus 1
    #    (for counting the actual node)

    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)

# --------------------------------------------------------------------
def sum_values(node):
    # We solve this problem recursively
    #
    #  - If node = None -> we return 0 (the neutral for additiion)
    #
    #  - Otherwise, we (recursively) sum the values of nodes in
    #    resp. the left and right children and return their sum plus
    #    the value of the actual node.
    #
    # Note that by defining `sum_values(None)` as 0, we do not have to
    # check that `node.left` or `node.right` is not `None.

    if node is None:
        return 0
    return node.value + sum_values(node.left) + sum_values(node.right)

# --------------------------------------------------------------------
def accumulate(node, f, acc):
    # We want to *fold* f on the values of `node`, starting at `acc`.
    #
    # I.e. if `node` contains the values `x0`, `x1`, ..., `xn`,
    # we want to compute:
    #
    #   f(xn, f(x_{n-1}, ..., f(f1, f(x0, acc)) ...))
    #
    # Note that the result may depend on the application
    # order. However, for associative-commutative operators, the
    # application order is irrelevant.

    # If `root` is `None`, we are done and we return the accumulator
    # value.
    if node is None:
        return acc

    # Otherwise
    acc = accumulate(node.left , f, acc) # Fold `f` on the left  sub-tree
    acc = accumulate(node.right, f, acc) # Fold `f` on the right sub-tree
    acc = f(node.value, acc)             # Apply `f` to the current node

    return acc

# --------------------------------------------------------------------
def _second_min(node):
    # We write an auxiliary function that returns a pair that contains
    # the two smallest values of the tree rooted at `node` - with
    # duplicates, the smallest element first.

    if node is None:
        # For the empty tree, we simply return `(math.inf, math.inf)`
        # We do not choose this at random: `math.inf` is a neutral
        # element for `min`.
        return (math.inf, math.inf)

    # We obtain the two smallest elements of the left subtree...
    minl, sminl = _second_min(node.left )

    # ...and do the same for the right subtree.
    minr, sminr = _second_min(node.right)

    # Finally, the two smallest values of the tree rooted at `node`
    # are the two smallest values among `minl`, `sminl`, `minr`,
    # `sminr` and the actual node value `node.value`.
    #
    # We simply create a list that contains this 5 elements, sort it
    # and take the two first values.
    mins = sorted([minl, sminl, node.value, minr, sminr])

    return (mins[0], mins[1])

def second_min(root):
    return _second_min(root)[1]

# --------------------------------------------------------------------
def height(node):
    # We solve this problem by a direct reduction.

    # By definition, the height of the empty tree is None
    if node is None:
        return -1

    # Now, if the root is not `None`, we recursively compute the
    # height of the left and right subtrees. Now, from the definition
    # of height, the height of tree rooted at `node`, if 1 plus the
    # maximum of the height of its subtrees.
    #
    # Note that by choosing `-1` for the height of the empty subtree,
    # we do not have to check that wether `node.left` or `node.right`
    # is `None`.
    return 1 + max(height(node.left), height(node.right))

# --------------------------------------------------------------------
def mirrored(lnode, rnode):
    # We are give a recursive definition of being mirror trees:
    #
    # `lnode` is a mirror tree or `rnode` iff both are empty or i)
    #  they have equal values at the root, ii) the left subtree of
    #  `lnode` is a mirror of the right subtree of `rnode`, and iii)
    #  the right subtree of `lnode` is a mirror of the left subtree of
    #  `rnode`.
    #
    # It remains to implement that

    # First, we count the number of `None` parameters.
    #
    # Note that int(True) = 1 and int(False) = 0
    cnull = (lnode is None) + (rnode is None)

    if cnull > 0:
        # If at least 1 of the parameters if `None`, then `lnode` is a
        # mirror of `rnode` iff both are empty (i.e. equal to `None`)
        return cnull == 2

    # Otherwise, both are non empty. We just check that they have the
    # same root value and that their left-right and right-left
    # children are mirror trees.
    return \
        lnode.value == rnode.value         and \
        mirrored(lnode.left , rnode.right) and \
        mirrored(lnode.right, rnode.left )

# --------------------------------------------------------------------
def check_symmetry(root):
    # A tree is symmetric if it is its own mirror image.
    return mirrored(root, root)

# --------------------------------------------------------------------
def check_BST(node, lmin = -math.inf, lmax = math.inf):
    # We again solve this function recursively. We added two extra
    # arguments and the function is s.t.
    #
    #  - the tree rooted at `node` is a BST
    #
    #  - all the values in the tree rooted at `node` are in the
    #    range `lmin`..`lmax`.
    #
    # When `lmin` (resp. `lmax`) is equal to `-math.inf`
    # (resp. `math.inf`) -- i.e. their default values -- this amounts
    # to check that `node` is a BST.

    if node is None:
        # The empty tree is a BST and validate the extra restrictions.
        return True

    # Otherwise, we check that `node.value` is in the range
    # `lmin`..`lmax` and that `node.left` and `node.right` are
    # BST. However, we cannot keep the range `lmin`..`lmax`
    # here. Indeed, being a BST is not *compositional*, `node.left`
    # and `node.right` could be BST while `node` is not.
    #
    # If we want `node` to be a BST, we need that:
    #  i)  `node.left` and `node.right` are BST,
    #  ii)  all the values in `node.left` are smaller than `node.value`,
    #  iii) all the values in `node.right` are greater than `node.value`.
    #
    # This is why we check that `node.left` (resp. `node.right`) is a
    # BST in the range `lmin`..`node.value`
    # (resp. `node.value`..`lmax`).

    return \
        (lmin <= node.value <= lmax)            and \
        check_BST(node.left , lmin, node.value) and \
        check_BST(node.right, node.value, lmax)

    # Mini-puzzle: Observe that this version of check_BST(root) will
    # make up to 2*n comparisons to check that a tree with n nodes is
    # a BST. Can you modify check_BST to use fewer comparisons? What
    # is the minimum number needed?

# --------------------------------------------------------------------
def min_BST(node, acc = math.inf):
    # By definition, the smallest value of a BST is the value attached
    # to its left-mode node. here, we implement the function
    # recursively. The second argument is the smallest element we have
    # seen so far.
    return acc if node is None else min_BST(node.left, node.value)

# --------------------------------------------------------------------
def _min_diff(node):
    # Here again, we write an auxiliary function that returns a
    # triplet containing:
    #
    #  - the smallest value of the absolute difference between the
    #    values in different nodes of the tree rooted at `node`,
    #
    #  - the smallest value among the nodes of the tree rooted at
    #    `node` (or `None` if `node` is empty),
    #
    #  - the greatest value among the nodes of the tree rooted at
    #    `node` (or `None` if `node` is empty).

    if node is None:
        # For the empty tree, we return `math.inf` since `math.inf` is
        # a neutral element for `min` (given that we are computing a
        # minimum).
        return (math.inf, None, None)

    # We call the function recursively on the left and right subtrees
    mdl, minl, maxl = _min_diff(node.left )
    mdr, minr, maxr = _min_diff(node.right)

    # Now, since we have a BST:
    #
    #  - `node.value` is lower than any value in `node` right
    #    subtree. Hence, the (absolute) difference between
    #    `node.value` and one value of its right subtree is bounded by
    #    the (absolute) value between `node.value` and the minimal
    #    value of its right subtree.
    #
    #  - likewise, the (absolute) difference between `node.value` and
    #    one value of its left subtree is bounded by the (absolute)
    #    difference between `node.value` and the maximal value of its
    #    left subtree.
    #
    #  - last, again because we are working on a BST, the (absolute)
    #    difference between a value in the left subtree and a value in
    #    the right subtree is going to be bounded by the two values
    #    above.
    #
    #  In consequence, the smallest absolute value of the difference
    #  between the values in different nodes of the tree rooted is the
    #  smallest element among:
    #
    #  - the smallest value of the absolute differences in `node.left`,
    #
    #  - the smallest value of the absolute differences in `node.right`,
    #
    #  - the absolute difference between node.value and the greatest
    #    value in the left subtree,
    #
    #  - the absolute difference between node.value and the smallest
    #    value in the right subtree.
    #
    # Note that we do not use the absolute value in the expression
    # below: this is because we know that `node.value >= maxl` and
    # `minr <= node.value`.
    #
    # Note also that we have to consider that `maxl` or `minr` could
    # be `None`.

    return (
        # The absolute smallest difference in `node`
        min(mdl, mdr,
            node.value - (-math.inf if maxl is None else maxl),
            (math.inf if minr is None else minr) - node.value),
        # The minimal value in `node`
        node.value if minl is None else minl,
        # The maximal value in `node`
        node.value if maxr is None else maxr,
    )

min_diff = lambda node : _min_diff(node)[0]

# --------------------------------------------------------------------
def _count_distinct(node):
    # Here again, we write an auxiliary function that returns a
    # triplet containing:
    #
    #  - the number of distinct values present in `node`,

    #  - the smallest value among the nodes of the tree rooted at
    #    `node` (or `None` if `node` is empty),

    #  - the greatest value among the nodes of the tree rooted at
    #    `node` (or `None` if `node` is empty).


    if node is None:
        # We first handle the case of the empty tree
        return (0, None, None)

    cl, minl, maxl = _count_distinct(node.left )
    cr, minr, maxr = _count_distinct(node.right)

    # Now we simply sums `cl` + `cr` and add `1` to take `node.value`
    # into account. However, we might already have counted
    # `node.value` in the left and/or right subtrees. But, since we
    # are working on a BST, we know that:
    #
    # - If `node.value` appears in the left subtree, then it must be
    #   the maximal element of `node.left`.
    #
    # - Likewise, if `node.value` appears in the right subtree, it
    #   must be its minimal element.

    return (
          1           # Count this node
        + cl          # + the number of distinct elements in `node.left`
        + cr          # + the number of distinct elements in `node.right`
        # `node.value` has already been counted in `node.left`
        - (node.value == maxl)
        # `node.value` has already been counted in `node.right`
        - (node.value == minr),

        node.value if minl is None else minl,
        node.value if maxr is None else maxr,
    )

def count_distinct(tree):
    return _count_distinct(tree)[0]

# --------------------------------------------------------------------
def bst_remove(node, x):
    if node is None:
        # Base case, we did not find `x`
        return
  
    # If the value to be deleted is smaller than (resp. greater than)
    # the node's value, the delete it from the left (resp. right`)
    # child
    if x < node.value:
        node.left = bst_remote(node.left, x)
  
    elif x > node.value:
        node.right = bst_remove(node.right, x)
  
    else: 
        # If `x` is equal to `node.value`, then this is the node to be
        # deleted. First, we deal with the case where `node` has no
        # children or one child.

        if root.left is None:
            return root.right

        if root.right is None:
            return root.left

        # It remains the case where `node` have two children
        #
        # We first find the left-most child in `node`'s right child.
        # We also keep track of the left-mode child parent.

        parent, current = None, node.right
        while current.left is not None:
            parent, current = current, current.left

        # We remove the left-most node from the tree
        if parent is node:
            parent.right = current.right
        else:
            parent.left  = current.right

        # Set `node` value to (now removed) left-mode child value.
        node.value = current.value
  
    return root 

# --------------------------------------------------------------------
def bst_elements(node):
    # We simply use the in-order traversal (i.e. left-child, node
    # value and right-child)
    if node is None:
        return []
    return bst_elements(node.left) + [node.value] + bst_elements(node.right)

