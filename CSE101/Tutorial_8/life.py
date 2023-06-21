# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 09:36:07 2020

@author: 123
"""

class Point:
    """Encodes a live point in the Game of Life"""
    def __init__(self, x, y):
        """Initialize x- and y-coordinate of the point."""
        self.x = x
        self.y = y
    
    def __repr__(self):
        """Give a string representation of the Point for debugging."""
        return 'Point({}, {})'.format(self.x, self.y)
    
    def __eq__(self, other): 
        """Compare two Points' x- and y-coordinates."""
        return (self.x,self.y)==(other.x, other.y)
        
    def __hash__(self):
        """Compute a hash value for Points."""
        return hash((self.x,self.y))
            
    def get_neighbors(self):
        """Return the neighbors of the Point as a set.
        """
        s=set()
        for i in range(-1,2):
            for j in range(-1,2):
                if (i,j)!=(0,0):
                    s.add(Point(self.x+i, self.y+j))
        return s
        
class Board:
    """Store the current board and manipulate it.
    """
    def __init__(self, sizex, sizey, points):
        """Initialize size and initial points."""
        self.points = points
        self.sizex = sizex
        self.sizey = sizey
        self.x_size = sizex
        self.y_size = sizey
                        
    def is_legal(self, point):
        """Check if a given Point is on the board."""
        return self.sizex>point.x>=0 and self.sizey>point.y>=0
    
    def number_live_neighbors(self, p):
        """Compute the number of neighbors of p on the Board that are alive.
        """
        return len(self.points.intersection(p.get_neighbors()))
    
    def next_step(self):
        """Compute the points alive in the next round and update the 
        points of the Board.
        """
        points_alive = set()
        for point in self.points:
            if self.number_live_neighbors(point) in {2, 3}: points_alive.add(point)
        for p in self.points:
            for i in p.get_neighbors():
                if i in self.points or self.is_legal(i) == False: continue
                if self.number_live_neighbors(i) == 3: points_alive.add(i)
        self.points = points_alive
        
    def load_from_file(self, filename):
        """Load a board configuration from file. The file format is as follows:
        - The first two lines contain a number representing the size in x- and 
            y-coordinates, respectively.
        - Each of the following lines gives the coordinates of a single point,
            with the two coordinate values separated by a comma.
            Those are the points that are alive in the board to be loaded.
        """
        self.points = set()
        with open(filename) as f:
            self.x_size = int(f.readline())
            self.y_size = int(f.readline())
            for line in f.readlines():
                (one,two) = line.strip().split(',')
                self.points.add(Point(int(one.strip()), int(two.strip())))
                
    def toggle_point(self, x, y):
        """Add Point(x,y) if it is not in points, otherwise delete it from 
        points.
        """
        p=Point(x,y)
        if p in self.points: self.points.remove(p)
        elif p not in self.points: self.points.add(p)
    
    def save_to_file(self, filename):
        """Save a board to a file. The format is that described for
        load_from_file()
        """
        with open(filename, 'w') as f:
            f.write('{}\n'.format(self.sizex))
            f.write('{}\n'.format(self.sizey))
            for p in self.points:
                f.write('{},{}\n'.format(p.x, p.y))

def is_periodic(board):
    """Return True if the input board is periodic, otherwise False."""
    initial_points = board.points.copy()
    for i in range(2**board.sizex):
        board.next_step()
        if initial_points == board.points:
            return True
    return False