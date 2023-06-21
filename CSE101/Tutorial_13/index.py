# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 09:58:18 2021

@author: user
"""
class Node:
    def __init__(self, key, value, left, right):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value and self.left == other.left and self.right == other.right

    def __repr__(self):
        return f'Node({repr(self.key)}, {repr(self.value)}, {repr(self.left)}, {repr(self.right)})'

    def __str__(self):
        return f'Tree node; key: {self.key}, value: {self.value}'    

    def search(self, key):
        """Binary search of the element."""
        if self.key == key:
            return self.value
        if self.key > key and self.left is not None:
            return self.left.search(key)
        if self.key < key and self.right is not None:
            return self.right.search(key)
        return None
    
    def print_in_order(self):
        """Prints all values sorted in order of key."""
        if self.left is not None:
            self.left.print_in_order()
        print('{}: {}'.format(self.key, self.value))
        if self.right is not None:
            self.right.print_in_order()
            
    def add(self, key, value):
        """Adds a new pair to the tree."""
        if key == self.key:
            if value not in self.value:
                self.value.append(value)
        elif key < self.key:
            if self.left is None:
                self.left = Node(key, [value], None, None)
            else: self.left.add(key, value)
        elif key > self.key:
            if self.right is None:
                self.right = Node(key, [value], None, None)
            else: self.right.add(key, value)
            
    def write_in_order(self, filename):
        """Write all key: value pairs in the index tree
        to the named file, one entry per line.
        """
        with open(filename, 'w') as f1:
            self.write_in_order_rec(f1)

    def write_in_order_rec(self, file):
        """Recursive helper method for write_in_order."""
        if self.left is not None:
            self.left.write_in_order_rec(file)
        file.write('{}: {}\n'.format(self.key, self.value))
        if self.right is not None:
            self.right.write_in_order_rec(file)

    def height(self):
        """Returns the height of the BST."""
        height = [0,0]                          # left-height and right-height
        if self.left is not None:
            height[0] = self.left.height() + 1
        if self.right is not None:
            height[1] = self.right.height() + 1
        return max(height)
    
    def list_in_order(self):
        """Converts a BST into a sorted list."""
        if self.left and self.right is not None:
            return self.left.list_in_order() + [(self.key, f'{self.value}')] + self.right.list_in_order()
        if self.left is not None:
            return self.left.list_in_order() + [(self.key, f'{self.value}')]
        if self.right is not None:
            return [(self.key, f'{self.value}')] + self.right.list_in_order()
        return [(self.key, f'{self.value}')]


def example_bst():
    """Construct an example BST."""
    n3 = Node(3, 'Three', None, None)
    n4 = Node(4, 'Four', None, None)
    n6 = Node(6, 'Six', None, None)
    n7 = Node(7, 'Seven', None, None)
    n8 = Node(8, 'Eight', None, None)
    n10 = Node(10, 'Ten', None, None)
    n13 = Node(13, 'Thirteen', None, None)
    n14 = Node(14, 'Fourteen', None, None)
    n8.right = n10
    n10.right = n14
    n14.left = n13
    n8.left = n4
    n4.left = n3
    n4.right = n6
    n6.right = n7
    return n8


def split_in_words_and_lowercase(line):
    """Split a line of text into a list of lower-case words."""
    parts = line.strip('\n').replace('-', ' ').replace("'", " ").replace('"', ' ').split()
    parts = [p.strip('",._;?!:()[]').lower() for p in parts]
    return [p for p in parts if p != '']

def construct_bst_for_indexing(filename):
    """Returns BST for indexing a file."""
    root = None
    with open(filename, 'r') as f1:
        lineindex = 0
        for line in f1:
            lineindex+=1
            for word in split_in_words_and_lowercase(line):
                if root is None:
                    root = Node(word, [lineindex], None, None)
                else: root.add(word, lineindex)
    return root


def generate_index(textfile, indexfile):
    """Constructs a BST for textfile and and writes the sorted index in indexfile."""
    temp = construct_bst_for_indexing(textfile)
    temp.write_in_order(indexfile)


def balanced_bst(sorted_list):
    """Return balanced BST constructed from sorted list."""
    return balanced_bst_rec(sorted_list, 0, len(sorted_list))

def balanced_bst_rec(sorted_list, lower, upper):
    """Recursive helper function for balanced_bst."""
    mid=(lower+upper)//2
    root=Node(sorted_list[mid][0], sorted_list[mid][1], None, None)
    if lower<mid:
        root.left=balanced_bst_rec(sorted_list, lower, mid)
    if mid+1<upper:
         root.right=balanced_bst_rec(sorted_list, mid+1, upper)
    return root