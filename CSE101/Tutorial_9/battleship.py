# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:23:48 2020

@author: 123
"""

class Ship:
    """A ship that can be placed on the grid"""

    def __repr__(self):
        """Give a representation for debugging."""
        return "Ship('{}', {})".format(self.name, self.positions)

    def __init__(self, name, positions):
        """Initialize name and position. Set hits to empty set."""
        self.name=name
        self.positions=positions
        self.hits=set()
    
    def __eq__(self, other):
        return (self.name,self.positions,self.hits)==(other.name, other.positions, other.hits)
    
    def is_afloat(self):
        for p in self.positions:
            if p not in self.hits:
                return True
        return False
    
    def take_shot(self, shot):
        """Check if the shot hits the ship. If so, remember the hit.
        Returns one of 'MISS', 'HIT', or 'DESTROYED'.
        """
        if shot in self.positions and shot not in self.hits:
            self.hits.add(shot)
            if self.hits == self.positions : return 'DESTROYED'
            return 'HIT'
        return 'MISS'

    
class Grid:
    """Encodes the grid on which the Ships are placed. Also remembers the 
    shots that have been fired so far and if they were hits.
    """
    def __init__(self, x_size, y_size):
        """Initializes a board of the given size."""
        self.x_size=x_size
        self.y_size=y_size
        self.ships=[]
        self.misses=set()
        
    def add_ship(self, ship):
        """Add a Ship to the grid."""
        self.ships.append(ship)
        
    def shoot(self, position):
        for ship in self.ships:
            if ship.take_shot(position)=="HIT": return ('HIT', None)
            elif ship.hits == ship.positions: return ('DESTROYED', ship)
        self.misses.add(position)
        return ('MISS', None)
    
class BlindGrid:
    """Encodes the opponent's view of the grid."""

    def __init__(self, grid):
        """Given a grid, initializes hits, misses and sunken ships."""
        self.x_size = grid.x_size
        self.y_size = grid.y_size
        self.misses = grid.misses
        self.hits=set()
        for ship in grid.ships:
            self.hits = self.hits.union(ship.hits)
        self.sunken_ships = [ship for ship in grid.ships if not ship.is_afloat()]
        
def create_ship_from_line(line):
    items=line.split(' ')
    name=items.pop(0)
    pos={tuple((int(x)) for x in i.split(':')) for i in
         items}
    return Ship(name, pos)

def load_grid_from_file(filename):
    with open(filename, 'r') as f1:
        size = f1.readline().strip()
        (x, y) = tuple(int(i) for i in size.split(':'))
        g1 = Grid(x, y)
        for line in f1:
            g1.ships.append(create_ship_from_line(line))
    return g1


