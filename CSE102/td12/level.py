#!/usr/bin/env python3

import math
import pygame as pg

black    = pg.Color('black')
blue     = pg.Color('#0000F0')
darkblue = pg.Color('#000044')
yellow   = pg.Color('yellow')

class Level:
    ### What each cell can be
    EMPTY     = 0
    WALL      = 1
    PILL      = 2
    POWERPILL = 3
    PIT       = 4

    @classmethod
    def is_pill(cls, cell):
        return cell == cls.PILL

    def __init__(self, width, height, walls):
        """Create a new level

        Args:
          width: width of the maze
          height: height of the maze
          walls: interior wall rectangles
        """
        assert height % 2 == 1
        self.width = width + 2
        self.height = height + 2
        self.walls = walls
        self.num_pills = 0

        self.cell = [[Level.EMPTY] * self.width for _ in range(self.height)]
        # exterior walls
        for col in range(self.width):
            self[0, col] = Level.WALL
            self[self.height - 1, col] = Level.WALL
        for row in range(self.height):
            self[row, 0] = Level.WALL
            self[row, self.width - 1] = Level.WALL
        self[self.height // 2 - 1, 0] = Level.EMPTY
        self[self.height // 2 - 1, self.width - 1] = Level.EMPTY
        # interior walls
        for (c, r, w, h) in walls:
            for row in range(r, r + h):
                for col in range(c, c + w):
                    self[row + 1, col + 1] = Level.WALL
        # pit
        (pr, pc, pw, ph) = self.pit = (self.height // 2 - 3, self.width // 2 - 4, 8, 5)
        for row in range(pr, pr + ph):
            self[row, pc] = Level.WALL
            self[row, pc + pw - 1] = Level.WALL
        for col in range(pc, pc + pw):
            self[pr, col] = Level.WALL
            self[pr + ph - 1, col] = Level.WALL
        for row in range(pr + 1, pr + ph - 1):
            for col in range(pc + 1, pc + pw - 1):
                self[row, col] = Level.PIT
        # pills
        self.reset()

    def __getitem__(self, pos):
        return self.cell[pos[0]][pos[1]]

    def __setitem__(self, pos, cell):
        old_pill = self.is_pill(self[pos])
        new_pill = self.is_pill(cell)
        self.cell[pos[0]][pos[1]] = cell
        if old_pill and not new_pill: self.num_pills -= 1
        elif new_pill and not old_pill: self.num_pills += 1

    def reset(self):
        """Reset the pills"""
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self[row, col] == Level.EMPTY:
                    self[row, col] = Level.PILL
        (pr, pc, pw, ph) = self.pit
        self[pr + ph, pc + pw//2 - 1] = Level.EMPTY
        self[pr + ph, pc + pw//2] = Level.EMPTY

    def can_enter(self, cell):
        """Is it valid to enter the given cell?"""
        row, col = cell
        return self[row, col] not in {Level.WALL, Level.PIT}

    def neighbors(self, cell, exclude=None):
        """All the neighbors of the given cell, with the possible exception of the
        cell in the `exclude` parameter (if any)"""
        row, col = cell
        cands = [(row + self.height - 1, col), (row, col + 1), (row + 1, col), (row, col + self.width - 1)]
        ns = []
        for (r, c) in cands:
            r = r % self.height
            c = c % self.width
            if exclude is not None:
                if r == exclude[0] and c == exclude[1]: continue
            if self[r, c] in [Level.WALL, Level.PIT]: continue
            ns.append((r, c))
        return ns

    def render(self, window):
        """Draw the level in `window`"""
        cw = window.get_width() // (self.width + 2)
        ch = window.get_height() // (self.height + 2)
        # Pit
        (pr, pc, pw, ph) = self.pit
        pg.draw.rect(window, darkblue, ((pc + 1) * cw + cw//2, (pr + 1) * ch + ch//2,
                                        (pw - 1) * cw, (ph - 1) * ch))
        # Cells
        for row in range(self.height):
            for col in range(self.width):
                x = (col + 1) * cw
                y = (row + 1) * ch
                if self[row, col] == Level.EMPTY:
                    pass
                elif self[row, col] == Level.WALL:
                    a = [r in range(0, self.height) and c in range(self.width) \
                         and self[r, c] != Level.WALL \
                         for r in range(row - 1, row + 2) \
                         for c in range(col - 1, col + 2)]
                    if a[0] and not (a[1] or a[3]):
                        pg.draw.line(window, blue, (x, y+ch//2), (x+cw//2, y), 4)
                    if a[2] and not (a[1] or a[5]):
                        pg.draw.line(window, blue, (x+cw//2, y), (x+cw, y+ch//2), 4)
                    if a[6] and not (a[3] or a[7]):
                        pg.draw.line(window, blue, (x+cw//2, y+ch), (x, y+ch//2), 4)
                    if a[8] and not (a[5] or a[7]):
                        pg.draw.line(window, blue, (x+cw//2, y+ch), (x+cw, y+ch//2), 4)
                    if a[0] and a[1] and a[3]:
                        pg.draw.line(window, blue, (x+cw//2, y+ch), (x+cw, y+ch//2), 4)
                    if a[1] and a[2] and a[5]:
                        pg.draw.line(window, blue, (x, y+ch//2), (x+cw//2, y+ch), 4)
                    if a[3] and a[6] and a[7]:
                        pg.draw.line(window, blue, (x+cw//2, y), (x+cw, y+ch//2), 4)
                    if a[5] and a[7] and a[8]:
                        pg.draw.line(window, blue, (x, y+ch//2), (x+cw//2, y), 4)
                    if a[3] and not (a[1] or a[7]):
                        pg.draw.line(window, blue, (x+cw//2, y), (x + cw//2, y+ch), 4)
                    if a[1] and not (a[3] or a[5]):
                        pg.draw.line(window, blue, (x, y+ch//2), (x+cw, y+ch//2), 4)
                    if a[5] and not (a[1] or a[7]):
                        pg.draw.line(window, blue, (x+cw//2, y), (x+cw//2, y+ch), 4)
                    if a[7] and not (a[3] or a[5]):
                        pg.draw.line(window, blue, (x, y+ch//2), (x+cw, y+ch//2), 4)
                elif self[row, col] == Level.PILL:
                    pg.draw.circle(window, yellow,
                                   (x + cw // 2, y + ch // 2),
                                   cw * 1 // 9)
                elif self[row, col] == Level.POWERPILL:
                    pg.draw.circle(window, yellow,
                                   (x + cw // 2, y + ch // 2),
                                   cw * 2 // 7)
                elif self[row, col] == Level.PIT:
                    pass
                else:
                    raise Exception('cell[{}][{}] contained {}'
                                    .format(row, col, self[row, col]))


### This is the standard level 1 of Pac-Man
level_1 = Level(26, 29,
                [(1, 1, 4, 3), (6, 1, 5, 3), (12, 0, 2, 4),
                 (15, 1, 5, 3), (21, 1, 4, 3), (1, 5, 4, 2),
                 (6, 5, 2, 8), (9, 5, 8, 2), (18, 5, 2, 8),
                 (21, 5, 4, 2), (0, 8, 5, 5), (8, 8, 3, 2),
                 (12, 7, 2, 3), (15, 8, 3, 2), (21, 8, 5, 5),
                 (0, 14, 5, 5), (21, 14, 5, 5), (6, 14, 2, 5),
                 (18, 14, 2, 5), (9, 17, 8, 2), (1, 20, 4, 2),
                 (6, 20, 5, 2), (12, 19, 2, 3), (15, 20, 5, 2),
                 (21, 20, 4, 2), (3, 22, 2, 3), (21, 22, 2, 3),
                 (0, 23, 2, 2), (24, 23, 2, 2), (9, 23, 8, 2),
                 (12, 25, 2, 3), (6, 23, 2, 3), (18, 23, 2, 3),
                 (1, 26, 10, 2), (15, 26, 10, 2)])
levels = [level_1]

### just for debugging
if __name__ == '__main__':
    def show_level(level):
        pg.init()

        window = pg.display.set_mode((1000, 862))
        clock = pg.time.Clock()

        done = False
        while not done:
            for ev in pg.event.get():
                if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                    done = True

            window.fill(black)
            level.render(window)
            pg.display.flip()

        pg.quit()

    show_level(level_1)
