#!/usr/bin/env python3

import random, copy, math

import pygame as pg

### The level.py file contains the representation of the level
import level

### some convenient color names
green  = pg.Color('#00FF00')
black  = pg.Color('black')
yellow = pg.Color('yellow')

class Pacman:
    # Pacman modes
    ALIVE = 0
    DEAD = 1

    def __init__(self, level):
        self.level = level      # the "level" is the current board
        self.score = 0          # the score the Pac-Man has achieved
        self.pos = (0, 0)       # the cell coordinates of the Pac-Man
        ### The above are dummy values; the real values come from
        ### the following .reset() function
        self.reset()

    def reset(self):
        """Set the default values for the starting state of the Pac-Man."""
        (pr, pc, pw, ph) = self.level.pit
        self.pos = (pr + ph, pc + pw // 2)
        self.score = 0
        # maybe set other variables/attributes?

    def update(self, millis, ghosts):
        """Update the Pac-Man's state.

        millis: number of milliseconds that have elapsed since the last
                time update() was called
        ghosts: a list of all the ghost entities on the level. The Pac-Man
                should **not** modify the ghost entities, but is allowed
                to retrieve information about the ghosts"""
        # TODO
        pass

    def process_event(self, event):
        """Make the Pac-Man respond to the event, if relevant. It should
        only respond to the movement keys (WASD or the arrow keys)."""
        # TODO
        pass

    def render(self, window):
        """Draw the Pac-Man on the given window"""
        # scale params
        cw = window.get_width() // (self.level.width + 2)
        ch = window.get_height() // (self.level.height + 2)
        y = int((self.pos[0] + 1) * ch)
        x = int((self.pos[1] + 1) * cw)
        ## body, a yellow circle
        pg.draw.circle(window, yellow, (x + cw//2, y + ch//2), cw * 2 // 5)
        ## mouth, a black filled wedge
        pg.draw.polygon(window, black, [(x + cw//2, y + ch//2), (x + cw, y), (x + cw, y + ch)])
