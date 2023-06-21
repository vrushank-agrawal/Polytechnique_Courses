#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 09:35:56 2018

@author: smith
"""

class Node:
    """A simple binary search tree Node class.
    Data attributes:
        - key: node key (for searching)
        - value: node data
        - left: left subtree
        - right: right subtree
    """

    def __init__(self, key, value, left, right):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Node({}, {}, {}, {})'.format(
            repr(self.key),
            repr(self.value),
            repr(self.left),
            repr(self.right))

    def __str__(self):
        return 'Tree node; key: {}, value: {}'.format(
            repr(self.key),
            repr(self.value))

    def search(self, key):
        """Binary search in this tree."""
        if self.key == key:
            return self.value
        if self.key > key and self.left is not None:
            return self.left.search(key)
        if self.key < key and self.right is not None:
            return self.right.search(key)
        return None

    def print_in_order(self):
        """Print all of the (key, value) pairs in this tree, sorted by key.
        Uses left-to-right tree traversal.
        """
        if self.left is not None:
            self.left.print_in_order()
        print('{}: {}'.format(self.key, self.value))
        if self.right is not None:
            self.right.print_in_order()

    def add(self, key, value):
        """Add a new (key, value) pair to the tree.
        If key is already present, then append value to a the list in that
        Node.  Otherwise, a new Node is created with the given value as the
        the only entry in its value list.
        """
        if key == self.key:
            if value not in self.value:
                self.value.append(value)
        elif key < self.key:
            if self.left is None:
                self.left = Node(key, [value], None, None)
            else:
                self.left.add(key, value)
        else: # key > self.key:
            if self.right is None:
                self.right = Node(key, [value], None, None)
            else:
                self.right.add(key, value)

    def height(self):
        """Return the height of this tree."""
        left_height = 0
        right_height = 0
        if self.left is not None:
            left_height = self.left.height() + 1
        if self.right is not None:
            right_height = self.right.height() + 1
        return max(left_height, right_height)

    def write_in_order_rec(self, file):
        """Recursive helper method for write_in_order."""
        if self.left is not None:
            self.left.write_in_order_rec(file)
        file.write('{}: {}\n'.format(self.key, self.value))
        if self.right is not None:
            self.right.write_in_order_rec(file)

    def write_in_order(self, filename):
        """Write the tree entries out, in order to the named file."""
        with open(filename, 'w') as file:
            self.write_in_order_rec(file)


def generate_index(filename):
    """Generate an index for the named file, writing it ot filename.index ."""
    outname = filename + '.index'
    bst = construct_bst_for_indexing(filename)
    bst.write_in_order(outname)

def split_in_words_and_lowercase(line):
    """Split a line of text into a list of lower-case words."""
    parts = line.strip('\n').replace('-', ' ').replace("'", " ").split()
    parts = [p.strip('",._;?!:()[]').lower() for p in parts]
    return [p for p in parts if p != '']

def construct_bst_for_indexing(filename):
    """Build the binary search tree for indexing the named file."""
    root = None
    with open(filename, 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1
            for word in split_in_words_and_lowercase(line):
                if root is None:
                    root = Node(word, [lineno], None, None)
                else:
                    root.add(word, lineno)
    return root


def example_bst():
    """Construct an example BST."""
    n_8 = Node(8, 'Eight', None, None)
    n_4 = Node(4, 'Four', None, None)
    n_3 = Node(3, 'Three', None, None)
    n_6 = Node(6, 'Six', None, None)
    n_7 = Node(7, 'Seven', None, None)
    n_10 = Node(10, 'Ten', None, None)
    n_14 = Node(14, 'Fourteen', None, None)
    n_13 = Node(13, 'Thirteen', None, None)
    n_8.left = n_4
    n_4.left = n_3
    n_4.right = n_6
    n_6.right = n_7
    n_8.right = n_10
    n_10.right = n_14
    n_14.left = n_13
    return n_8

