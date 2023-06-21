"""TD 8: Conway's game of life."""

class Point:
    """Encodes a live point in the Game of Life.

    Data attributes:
    x -- the x-coordinate (an integer)
    y -- the y-coorinate (an integer)
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # No reason to not use the quick-and-dirty hash recipe here:
        return hash((self.x, self.y))
        # Alternatively, you could use a (reasonably random-looking)
        # linear combination of the x and y values

    def get_neighbors(self):
        """Return the set of neighbors of this Point."""
        return {Point(self.x-1, self.y-1),
                Point(self.x-1, self.y),
                Point(self.x-1, self.y+1),
                Point(self.x, self.y-1),
                Point(self.x, self.y+1),
                Point(self.x+1, self.y-1),
                Point(self.x+1, self.y),
                Point(self.x+1, self.y+1),
               }
        # Alternatively, you could use iterations
        # to do this a little more cleanly.  For example:
        # return {Point(self.x + i, self.y + j)
                # for i in range(-1, 2)
                # for j in range(-1, 2)
                # if (i, j) != (0, 0)}


class Board:
    """Store the current board and manipulate it.
    Data attributes:
    sizex -- the number of "columns" on the board
    sizey -- the number of "rows"
    points -- the set of "live" points
    """

    def __init__(self, sizex, sizey, points):
        self.points = points
        self.sizex = sizex
        self.sizey = sizey

    def is_legal(self, point):
        """Check if a given Point is on the board.
        """
        return 0 <= point.x < self.sizex and 0 <= point.y < self.sizey

    def number_live_neighbors(self, point):
        """Compute the number of neighbours of p on the Board that are alive.
        """
        return sum(1 for p in point.get_neighbors() if p in self.points)

    def next_step(self):
        """Compute the points alive in the next round,
        and update the points of the Board.
        """
        next_alive = {point for point in self.points
                      if self.number_live_neighbors(point) in {2, 3}}
        for point in self.points:
            for nbor in point.get_neighbors():
                if not self.is_legal(nbor) or nbor in self.points:
                    continue
                # now we know that n is legally dead
                if self.number_live_neighbors(nbor) == 3:
                    next_alive.add(nbor)
        self.points = next_alive

    def load_from_file(self, filename):
        """Load a board configuration from file. The file format is as follows:
        - The first two lines contain a number representing the size in x- and
            y-coordinates, respectively.
        - Each of the following lines gives the coordinates of a single point,
            with the two coordinate values separated by a comma.
            Those are the points that are alive in the board to be loaded.
        """
        self.points = set()
        with open(filename) as input_file:
            self.sizex = int(input_file.readline())
            self.sizey = int(input_file.readline())
            for line in input_file:
                parts = line.split(',')
                self.points.add(Point(int(parts[0].strip()),
                                      int(parts[1].strip())))

    def save_to_file(self, filename):
        """Save a board to a file. The format is that described for
        load_from_file()
        """
        with open(filename, 'w') as file:
            file.write('{}\n'.format(self.sizex))  # Line 0
            file.write('{}\n'.format(self.sizey))  # Line 1
            for pt in self.points:
                file.write('{},{}\n'.format(pt.x, pt.y))

    def toggle_point(self, x, y):
        """Add Point(x, y) if it is not in points, otherwise delete it from points.
        """
        point = Point(x, y)
        if point in self.points:
            self.points.remove(point)
        else:
            self.points.add(point)

class TextView():
    """A text visualization of Board instances.

    Data attributes:
    board -- the Board object to be displayed
    """

    def __init__(self, board):
        """Initialize the Board."""
        self.board = board

    def show(self):
        """Show the Board."""
        print('o' * (self.board.sizex+2))
        for y in range(self.board.sizey):
            print('o', end='')
            for x in range(self.board.sizex):
                if Point(x, y) in self.board.points:
                    print('X', end='')
                else:
                    print(' ', end='')
            print('o')
        print('o' * (self.board.sizex + 2))

    def tick(self):
        input('Press Enter for next step')


class LifeGame:
    """The game loop for the text based Game of Life.

    Data attributes:
    board -- a Board object for the current game of life
    view -- graphical viewing object for displaying the board
    """

    def __init__(self, board):
        """Initialize the board and creates a TextView for it."""
        self.board = board
        self.view = TextView(board)

    def run(self, steps):
        """Run the game of life for the given number of steps. At every step,
        show the board and prompt the user to continue by calling tick() on the
        TextView.
        """
        for _ in range(steps):
            self.view.show()
            self.view.tick()
            self.board.next_step()
