# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 11:39:13 2021

Title: Conway's Game of Life

@author: 
"""

GROUP = [
  "vrushank.agrawal@polytechnique.edu",
  "evdokia.gneusheva@polytechnique.edu",
]


import copy
import math
import numpy as np
import weakref

HC = weakref.WeakValueDictionary()

def hash_consing(s):
    return HC.setdefault(s, s)

class Universe:
    def round(self):
        """Compute (in place) the next generation of the universe"""
        raise NotImplementedError

    def get(self, i, j):
        """Returns the state of the cell at coordinates (ij[0], ij[1])"""
        raise NotImplementedError

    def rounds(self, n):
        """Compute (in place) the n-th next generation of the universe"""
        for _i in range(n):
            self.round()

# --------------------------------------------------------------------
# Exercise 1

class NaiveUniverse(Universe):
    def __init__(self, n, m, cells):
        self.cells = cells
        self.rows = n
        self.cols = m
                
    def get_neighbors(self, x, y):
        """Return valid neighbors of the Point as a set.
        """
        s=set()
        for i in range(max(0, x-1), min(self.rows, x+2)):
            for j in range(max(0, y-1), min(self.cols, y+2)):
                if (i,j)!=(x,y) and self.get(i, j): 
                    s.add((i, j))
        return s

    def round(self):
        cells_new = copy.deepcopy(self.cells)
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = len(self.get_neighbors(i, j))
                if not self.get(i, j) and neighbors == 3:
                    cells_new[i][j] = True
                if self.get(i, j) and not neighbors in (2,3):
                    cells_new[i][j] = False
        self.cells = copy.deepcopy(cells_new)

    def get(self, i, j):
        return self.cells[i][j]

# --------------------------------------------------------------------

class AbstractNode:
    BIG = True
    
    def __init__(self):
        self._hash = None
        self._cache = None
        
    def __hash__(self):
        if self._hash is None:
            self._hash = (
                self.population,
                self.level     ,
                self.nw        ,
                self.ne        ,
                self.sw        ,
                self.se        ,
            )
            self._hash = hash(self._hash)
        return self._hash
        
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, AbstractNode):
            return False
        return \
            self.level      == other.level      and \
            self.population == other.population and \
            self.nw         is other.nw         and \
            self.ne         is other.ne         and \
            self.sw         is other.sw         and \
            self.se         is other.se
            
        
    # ----------------------------------------------------------------
    # Exercise 11 auxiliary function
    
    def get_quad(self, key):
        if key == (0, 0): return self.nw
        if key == (0, 1): return self.ne
        if key == (1, 0): return self.sw
        if key == (1, 1): return self.se
        
    @property
    def cache(self):
        return self._cache
    
    @property
    def level(self):
        """Level of this node"""
        return None

    @property
    def population(self):
        """Total population of the area"""
        return None
        
    # ----------------------------------------------------------------
    # Exercise 2

    @staticmethod
    def zero(k):
        if k == 0:
            return AbstractNode.cell(0)
        else:
            quad = AbstractNode.zero(k-1)
            return AbstractNode.node(quad, quad, quad, quad)
        
    # ----------------------------------------------------------------
    # Exercise 3

    def extend(self):
        
        if self.level == 0:
            cell = AbstractNode.zero(0)
            return AbstractNode.node(cell, self, cell, cell)
        
        quad = self.zero(self.nw.level)
        
        return AbstractNode.node(
                    AbstractNode.node(quad, quad, quad, self.nw), 
                    AbstractNode.node(quad, quad, self.ne, quad), 
                    AbstractNode.node(quad, self.sw, quad, quad), 
                    AbstractNode.node(self.se, quad, quad, quad))
            
    # ----------------------------------------------------------------
    # Exercise 4 auxiliary function
    
    def get_quadtree(self, quad_tree, i, j):
        return AbstractNode.node(quad_tree[i][j], quad_tree[i][j+1], quad_tree[i+1][j], quad_tree[i+1][j+1])
    
    # ----------------------------------------------------------------
    # Exercise 4, 8 , and 13
    
    def forward(self, l = None):   
        
        # ------------------------------------------------------------
        # Exercise 9
        
        if self.population == 0:
            return self.zero(self.level - 1)
        
        l = (self.level - 2) if l is None else l
        
        if self.cache is None:
            self._cache = [None] * (self.level - 1)
        
        if self.cache[l] is not None:
            return self.cache[l]
        
        quad_tree = [ [self.nw.nw, self.nw.ne, self.ne.nw, self.ne.ne ], 
                    [self.nw.sw, self.nw.se, self.ne.sw, self.ne.se ], 
                    [self.sw.nw, self.sw.ne, self.se.nw, self.se.ne ], 
                    [self.sw.sw, self.sw.se, self.se.sw, self.se.se ] ]
        
        if l == (self.level - 2):
            
            if self.level < 2: return None
            
            if self.level == 2:
                temp = 0
                for i in quad_tree:
                    for j in i:
                        temp = (temp << 1) | j.population
                    
                self._cache[l] = self.level2_bitmask(temp)
                return self.cache[l]
            
            else:
                child_quadtree = [[None for i in range(3)] for j in range(3)]
                for i in range(3):
                    for j in range(3):
                        child_quadtree[i][j] = self.get_quadtree(quad_tree, i, j).forward()
                        
                quad_tree = child_quadtree
                
                child_quadtree = [[None for i in range(2)] for j in range(2)]
                for i in range(2):
                    for j in range(2):
                        child_quadtree[i][j] = self.get_quadtree(quad_tree, i, j).forward()
                        
                self.cache[l] = self.get_quadtree(child_quadtree, 0, 0) 
                return self.cache[l]   

        else:
            child_quadtree = [[None for i in range(3)] for j in range(3)]
            for i in range(3):
                for j in range(3):
                    child_quadtree[i][j] = self.get_quadtree(quad_tree, i, j).center_uni()
                    
            quad_tree = child_quadtree
            
            child_quadtree = [[None for i in range(2)] for j in range(2)]
            for i in range(2):
                for j in range(2):
                    child_quadtree[i][j] = self.get_quadtree(quad_tree, i, j).forward(l)
            
            self.cache[l] = self.get_quadtree(child_quadtree, 0, 0) 
            return self.cache[l]  
            
    # ----------------------------------------------------------------

    nw = property(lambda self : None)
    ne = property(lambda self : None)
    sw = property(lambda self : None)
    se = property(lambda self : None )

    # ----------------------------------------------------------------
    # Exercise 6
    
    @staticmethod
    def canon(node):
        return hash_consing(node)
    
    # ----------------------------------------------------------------
    # Exercise 7

    @staticmethod
    def cell(alive):
        return hash_consing(CellNode(alive))
    
    @staticmethod
    def node(nw, ne, sw, se):
        return hash_consing(Node(nw, ne, sw, se))
    
    # ----------------------------------------------------------------
    # Exercise 12 and 13 auxiliary function
    
    def center_uni(self):
        return AbstractNode.node(self.nw.se, self.ne.sw,
                    self.sw.ne, self.se.nw)
    
    # ----------------------------------------------------------------
    # Exercise 12 auxiliary function
    
    def peripheral_alive(self):        
        
        if self.population == self.center_uni().population:
            return False
        
        return True

# --------------------------------------------------------------------
# Exerise 10 auxiliary function

def pos_5(bit):
    """
    aux func for level2_bitmask
    """
    return (( (1 << 3) - 1 ) & (bit))  + \
            (((bit >> 4) & 1 ) << 3)   + \
            (((bit >> 6) & 1 ) << 4)   + \
            (((bit >> 8) & 0b111 ) << 5)
            
# --------------------------------------------------------------------
    
class CellNode(AbstractNode):
    def __init__(self, alive):
        super().__init__()
        self._alive = bool(alive)

    level      = property(lambda self : 0)
    population = property(lambda self : int(self._alive))
    alive      = property(lambda self : self._alive)


class Node(AbstractNode):
    def __init__(self, nw, ne, sw, se):
        super().__init__()

        self._level      = 1 + nw.level
        self._population = nw.population + ne.population + sw.population + se.population
        self._nw = nw
        self._ne = ne
        self._sw = sw
        self._se = se
            
    # ----------------------------------------------------------------
    # Exercise 10

    @staticmethod
    def level2_bitmask(mask):
        
        vals = [5,6,9,10]
        temp = []
        
        for i in vals:
            num = pos_5(mask >> i-5)
            count = 0
            while (num):
                count += num & 1
                num >>= 1
            if mask >> i & 1:
                if count not in (2,3): temp.append(0)
                else: temp.append(1)
            else:
                if count == 3: temp.append(1)
                else: temp.append(0)
        
        return AbstractNode.node(
                    AbstractNode.cell(temp[3]), 
                    AbstractNode.cell(temp[2]), 
                    AbstractNode.cell(temp[1]), 
                    AbstractNode.cell(temp[0]))
    
    # ----------------------------------------------------------------
    
    level      = property(lambda self : self._level)
    population = property(lambda self : self._population)

    nw = property(lambda self : self._nw)
    ne = property(lambda self : self._ne)
    sw = property(lambda self : self._sw)
    se = property(lambda self : self._se)

# --------------------------------------------------------------------

class HashLifeUniverse(Universe):
    def __init__(self, *args):
        if len(args) == 1:
            self._root = args[0]
        else:
            self._root = HashLifeUniverse.load(*args)

        self._generation = 0

    @staticmethod
    def load(n, m, cells):
        level = math.ceil(math.log(max(1, n, m), 2))

        mkcell = getattr(AbstractNode, 'cell', CellNode)
        mknode = getattr(AbstractNode, 'node', Node    )

        def get(i, j):
            i, j = i + n // 2, j + m // 2
            return \
                i in range(n) and \
                j in range(m) and \
                cells[i][j]
                
        def create(i, j, level):
            if level == 0:
                return mkcell(get (i, j))

            noffset = 1 if level < 2 else 1 << (level - 2)
            poffset = 0 if level < 2 else 1 << (level - 2)

            nw = create(i-noffset, j+poffset, level - 1)
            sw = create(i-noffset, j-noffset, level - 1)
            ne = create(i+poffset, j+poffset, level - 1)
            se = create(i+poffset, j-noffset, level - 1)
            
            return mknode(nw=nw, ne=ne, sw=sw, se=se)
                
        return create(0, 0, level)

    # ----------------------------------------------------------------
    # Exercise 11

    def get(self, i, j):
        
        node = self._root
        level = node.level
        size = np.power(2, level)
        
        if -size <= min(i, j) and max(i, j) < size:
            
            while level!=0:
                
                x = 1 if j >= 0 else 0
                y = 1 if i >= 0 else 0
                
                l = [-1 if level < 2 else - np.power(2, level - 2), 0 if level < 2 else np.power(2, level - 2) ]
                
                i -= l[y]
                j -= l[x]
                
                node = node.get_quad((1 - x, y))
                
                level -= 1
            
            return node.alive
        
        return False


    # ----------------------------------------------------------------
    # Exercise 12

    def extend(self, k):
        k = max(k, 2)

        while self.root.level < k:
            self._root = self.root.extend()
        
        if self.root.peripheral_alive():
            self._root = self.root.extend()
            
            
    # ----------------------------------------------------------------
    # Exercise 14
    
    def rounds(self, n):
        i = 0
        while np.power(2, i) <= n:
            if (n >> i) & 1:
                self.extend(i+2)
                self._root = self.root.extend()
                self._root = self.root.forward(i)
            i += 1
            
        self._generation += n

    def round(self):
        return self.rounds(1)

    @property
    def root(self):
        return self._root
        
    @property
    def generation(self):
        return self._generation