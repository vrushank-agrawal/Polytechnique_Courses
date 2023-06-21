#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 09:16:58 2019

@author: smith
"""
MISS = 1
HIT = 2
DESTROYED = 3

class Ship:
    """A ship that can be placed on the grid"""

    def __repr__(self):
        """Give a representation for debugging."""
        return "Ship('{}', {})".format(self.name, self.positions)

    def __init__(self, name, positions):
        """Initialize name and position. Set hits to empty set."""
        self.name = name
        self.positions = positions
        self.hits = set()

    def __eq__(self, other):
        return self.name == other.name \
            and self.positions == other.positions \
            and self.hits == other.hits

    def is_afloat(self):
        """True iff the ship has not been hit in every position."""
        for pos in self.positions:
            if pos not in self.hits:
                return True
        return False

    def shoot_at_ship(self, shot):
        """Check if the shot hits the ship. If so, remember the hit.
        Returns one of 'MISS', 'HIT', or 'DESTROYED'.
        """
        if shot in self.positions and shot not in self.hits:
            self.hits.add(shot)
            if not self.is_afloat():
                return 'DESTROYED'
            return 'HIT'
        return 'MISS'

class Grid:
    """Encodes the grid on which the Ships are placed. Also remembers the
    shots that have been fired so far and if they were hits.
    """
    def __init__(self, sizex, sizey):
        """Initializes a board of the given size."""
        self.sizex = sizex
        self.sizey = sizey
        self.ships = []
        self.misses = set()

    def add_ship(self, ship):
        """Add a ship to the grid."""
        self.ships.append(ship)

    def shoot(self, position):
        """Shoot at the given position."""
        for ship in self.ships:
            result = ship.shoot_at_ship(position)
            if result == 'HIT':
                return ('HIT', None)
            elif result == 'DESTROYED':
                return ('DESTROYED', ship)
        self.misses.add(position)
        return ('MISS', None)

class BlindGrid:
    """Encodes the opponent's view of the grid."""

    def __init__(self, grid):
        """Given a grid, initializes hits, misses and sunken ships."""
        self.sizex = grid.sizex
        self.sizey = grid.sizey
        self.misses = grid.misses
        self.hits = set()
        for ship in grid.ships:
            self.hits = self.hits.union(ship.hits)
        self.sunken_ships = [ship for ship in grid.ships if not ship.is_afloat()]
    

def create_ship_from_line(line):
    """Interpret a line 'NAME x_1:y_1 x_2:y_2 ... x_n:y_n\n' as a Ship."""
    parts = line.split()
    name = parts[0]
    positions = {tuple(int(n) for n in xy.split(':')) for xy in parts[1:]}
    return Ship(name, positions)

def load_grid_from_file(filename):
    """Load a grid of ships from a text file."""
    with open(filename, 'r') as input_file:
        coords = input_file.readline().strip()
        (x, y) = tuple(int(n) for n in coords.split(':'))
        res = Grid(x, y)
        for line in input_file:
            res.ships.append(create_ship_from_line(line))
    return res
