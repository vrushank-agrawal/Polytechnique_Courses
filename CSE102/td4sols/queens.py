def comb_print(n, comb):
    def occupied(i,j):
        return i<len(comb) and comb[i] == j
    
    print(' '*3*n + '__')
    for line in range(n):
        print(' '*(n-line-1)*3 + '__/', end='')
        for cell in range(line+1):
            i = n-1-line+cell
            j = cell
            s = '@@' if occupied(i,j) else '  '
            print(s + '\\__' + ('/' if cell<line else ''), end='')
        print()
    for line in range(n,2*n):
        print(' '*(line-n)*3 + '  \\__/', end='')
        for cell in range(2*n-1-line):
            i = cell
            j = cell+line-n+1
            s = '@@' if occupied(i,j) else '  '
            print(s + '\\__/', end='')
        print()
    print()
    
# --------------------------------------------------------------------
def invalid_offset(k, comb, j):
    return any(j == comb[i]       # j in same negative diagonal row as ith bee
               or                 # or
               k+j == comb[i]+i   # j in same column as ith bee
               for i in range(k)) # for some 0 <= i < k

# --------------------------------------------------------------------
def queen_bees(n, k, comb):
    # if k == n, then the partial solution is a full solution and we yield it
    if k == n:
        yield comb
    # otherwise, we look for a valid offset j to place the (k+1)th bee
    for j in range(n):
        if invalid_offset(k, comb, j):
            continue
        yield from queen_bees(n, k+1, comb + [j])

# --------------------------------------------------------------------
def count_combs(n):
    # we can efficiently and concisely count the number of solutions
    # by creating a generator that yields 1 for every solution, and
    # summing over it
    return sum(1 for _ in queen_bees(n, 0, []))
    # alternatively, we could create the list of all solutions and return its length:
    #   return len([s for s in queen_bees(n, 0, [])])
    # but this needlessly consumes a lot of memory, since we don't actually need to
    # store all the solutions to count how many there are.

# Now let's try computing some timing statistics...

import time 

# For convenience, we introduce a higher-order helper function time_fn, which
# takes as argument a function f and a generator dom, and prints the output
# f(x) = y for each input value x in dom, together with the time it took to
# compute y.

def time_fn(f, dom):
    base = time.time()
    for x in dom:
        print (f.__name__ + '(' + str(x) + ') =', f(x), 'in',
               f'{time.time() - base:.5f}', 'seconds')
        base = time.time()

# Some timing statistics for count_combs on my laptop (plugged into power):

# >>> time_fn(count_combs, range(1,11))
# count_combs(1) = 1 in 0.00007 seconds
# count_combs(2) = 1 in 0.00006 seconds
# count_combs(3) = 3 in 0.00015 seconds
# count_combs(4) = 7 in 0.00055 seconds
# count_combs(5) = 23 in 0.00253 seconds
# count_combs(6) = 83 in 0.01638 seconds
# count_combs(7) = 405 in 0.04339 seconds
# count_combs(8) = 2113 in 0.10754 seconds
# count_combs(9) = 12657 in 0.73461 seconds
# count_combs(10) = 82297 in 5.74676 seconds

# In many kinds of constraint problems, it is possible to use symmetry to
# reduce the size of the search space and potentially make backtracking
# search more efficient.  In the queen bees problem, the space of solutions has
# "vertical symmetry" in the sense that to every solution there is another
# solution obtained by reflecting across the vertical axis:

#             __                              __
#          __/  \__                        __/  \__
#       __/  \__/  \__                  __/  \__/  \__
#    __/  \__/@@\__/@@\__            __/@@\__/@@\__/  \__
# __/@@\__/  \__/  \__/  \__      __/  \__/  \__/  \__/@@\__
#   \__/  \__/  \__/  \__/          \__/  \__/  \__/  \__/
#      \__/  \__/@@\__/                \__/@@\__/  \__/
#         \__/  \__/                      \__/  \__/
#            \__/                            \__/
#

# Similarly, the space of solutions has "horizontal symmetry" in the sense that
# to every solution there is another solution obtained by reflecting across the
# horizontal axis:

#             __                              __
#          __/  \__                        __/  \__
#       __/  \__/  \__                  __/  \__/@@\__
#    __/  \__/@@\__/@@\__            __/  \__/  \__/  \__
# __/@@\__/  \__/  \__/  \__      __/@@\__/  \__/  \__/  \__
#   \__/  \__/  \__/  \__/          \__/  \__/@@\__/@@\__/
#      \__/  \__/@@\__/                \__/  \__/  \__/
#         \__/  \__/                      \__/  \__/
#            \__/                            \__/

# The reason why symmetry is *potentially* helpful for making backtracking
# search more efficient is that we only need to find one solution from each
# equivalence class of solutions up to symmetry.  On the other hand, there is
# a tradeoff involved because we may need to do a bit of extra bookkeeping in
# order to avoid counting the same solution twice.

# The following version of queen_bees uses horizontal symmetry to generate valid
# honeycombs a bit more efficiently.  It takes two extra parameters upper and
# lower, which count the number of bees above and below the horizontal axis.
# The idea is that we only ever try to build solutions with upper >= lower, and
# if upper > lower, then we can use horizontal symmetry to generate another solution
# with lower < upper.  (For instance, in the example above, the comb on the left
# has upper=2 and lower=1, while the one on the right has upper=1 and lower=2.)

def faster_queen_bees(n, k, upper, lower, comb):
    if lower + (n-k) < upper:
        # since lower + (n-k) < upper, this partial solution cannot possibly lead
        # to a solution with upper <= lower, so we backtrack.
        return
    if k == n:
        yield comb          # output the solution
        if lower > upper:   # if lower > upper, output the symmetric solution
            yield [comb.index(i) for i in range(n)]
    for j in range(n):
        if invalid_offset(k, comb, j):
            continue
        # determine whether the current bee is above or below the axis (or neither)
        du = 1 if k < j else 0
        dl = 1 if j < k else 0
        yield from faster_queen_bees(n, k+1, upper+du, lower+dl, comb + [j])

def count_faster_combs(n):
    return sum(1 for _ in faster_queen_bees(n, 0, 0, 0, []))

# This version is indeed a little faster, although not by that much:

# >>> time_fn(count_faster_combs, range(1,11))
# count_faster_combs(1) = 1 in 0.00005 seconds
# count_faster_combs(2) = 1 in 0.00004 seconds
# count_faster_combs(3) = 3 in 0.00010 seconds
# count_faster_combs(4) = 7 in 0.00035 seconds
# count_faster_combs(5) = 23 in 0.00152 seconds
# count_faster_combs(6) = 83 in 0.00620 seconds
# count_faster_combs(7) = 405 in 0.01946 seconds
# count_faster_combs(8) = 2113 in 0.08972 seconds
# count_faster_combs(9) = 12657 in 0.61744 seconds
# count_faster_combs(10) = 82297 in 4.13891 seconds

# Surely we can do better?  If you beat these numbers, please let us know!
# You might have a look at the references in https://oeis.org/A099152.

# --------------------------------------------------------------------

def board_print(n, black, white):
    def square(i,j):
        if (i,j) in black:
            return 'B'
        elif (i,j) in white:
            return 'W'
        return '.'
    
    print('+' + '-' * (2*n+1) + '+')
    for i in range(n):
        print('|', end = '')
        for j in range(n):
            print(' ' + square(i,j), end = '')
        print(' |')
    print('+' + '-' * (2*n+1) + '+')

# --------------------------------------------------------------------

# for the peaceable queens problem, we write a generic solver `solve` that is
# parameterized by an "attack function" attackfn (which determines whether two
# coordinates are attacking each other), together with four extra arguments:
#   black:  list of black pieces on the board
#   white:  list of white pieces on the board
#   bmoves: list of legal positions for the next black piece
#   wmoves: list of legal positions for the next white piece
#   m:      number of additional pairs of black/white pieces to place on the board
 
def solve(attackfn, black, white, bmoves, wmoves, m):
    if m == 0:                           # if m == 0 we are done, we yield the solution
        yield (black, white)
    else:
        for i in range(len(bmoves)):     # otherwise we try one of black's moves
            b = bmoves[i]
            for j in range(len(wmoves)): # and one of white's moves
                w = wmoves[j]
                if attackfn(w,b):        # so long as they are not in conflict
                    continue
                # Then we prune the list of available moves for black and white.
                # For example, for the case of black, first we remove all of the
                # black moves we already considered (index <= i), then we remove
                # all of the moves which are in conflict with the white piece
                # that was just placed.                
                new_bmoves = [bm for bm in bmoves[i+1:] if not attackfn(w,bm)]
                new_wmoves = [wm for wm in wmoves[j+1:] if not attackfn(wm,b)]
                yield from solve(attackfn, black + [b], white + [w], new_bmoves, new_wmoves, m-1)

# two queens are attacking if they are in the same row, column, or diagonal
def queenattack (p1, p2):
    (i1,j1) = p1
    (i2,j2) = p2
    return (i1 == i2) or (j1 == j2) or (i1-j1) == (i2-j2) or (i1+j1) == (i2+j2)

# we implement peaceable_queens by calling solve with queenattack
def peaceable_queens(n, m):
    empty = [(i,j) for i in range(n) for j in range(n)]
    return solve(queenattack, [], [], empty, empty, m)

# we can easily implement "peaceable kings", "peaceable rooks", etc., by plugging
# the solver with different attack functions.
def kingattack (p1, p2):
    (i1,j1) = p1
    (i2,j2) = p2
    return abs (i1 - i2) <= 1 and abs (j1 - j2) <= 1

def rookattack (p1, p2):
    (i1,j1) = p1
    (i2,j2) = p2
    return (i1 == i2) or (j1 == j2)

def peaceable_rooks(n, m):
    empty = [(i,j) for i in range(n) for j in range(n)]
    yield from solve(rookattack, [], [], empty, empty, m)

def peaceable_kings(n, m):
    empty = [(i,j) for i in range(n) for j in range(n)]
    yield from solve(kingattack, [], [], empty, empty, m)

# we write a generic "pax number" routine parameterized by an attack function
def pax_number(attackfn, n):
    empty = [(i,j) for i in range(n) for j in range(n)]
    m = 1
    while True:
        g = solve(attackfn, [], [], empty, empty, m)
        s = next(g, None)
        if not s:
            return (m-1)
        m += 1

def pax_regina_number(n):
    return pax_number(queenattack, n)

# Some timing statistics:

# >>> time_fn(pax_regina_number, range(1,8))
# pax_regina_number(1) = 0 in 0.00007 seconds
# pax_regina_number(2) = 0 in 0.00007 seconds
# pax_regina_number(3) = 1 in 0.00066 seconds
# pax_regina_number(4) = 2 in 0.00585 seconds
# pax_regina_number(5) = 4 in 0.03839 seconds
# pax_regina_number(6) = 5 in 0.45000 seconds
# pax_regina_number(7) = 7 in 23.34762 seconds

# Here are some example peaceful configurations:

# >>> board_print(6, *next(peaceable_queens(6,5)))
# +-------------+
# | B . . . . . |
# | . . W . . W |
# | . . . . W W |
# | . . . . W . |
# | B B . . . . |
# | B . . B . . |
# +-------------+
# >>> board_print(6, *next(peaceable_rooks(6,9)))
# +-------------+
# | B . B . B . |
# | . W . W . W |
# | B . B . B . |
# | . W . W . W |
# | B . B . B . |
# | . W . W . W |
# +-------------+
# >>> board_print(8, *next(peaceable_kings(8,22)))
# +-----------------+
# | B . W . B . W W |
# | B . W . B . W W |
# | B . W . B . W W |
# | B . . . B . W W |
# | B B B B B . W W |
# | B B B . . . W W |
# | B B B . W W W W |
# | B B B . W W W . |
# +-----------------+
