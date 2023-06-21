"""Non-transitive dice."""


def slice_dice(n, s, dice):
    """Split a single list represinting dice into one list per die."""
    return [dice[i * s : i * s + s] for i in range(n)]


def win_probability(die1, die2):
    """Compute the winning probability of die1 over die2."""
    n = len(die1)
    return sum((1 if d1 > d2 else 0 for d1 in die1 for d2 in die2)) / (n * n)


def beats(die1, die2, p=0.5):
    """Check if die1 beats die2 with probability greater than p."""
    return win_probability(die1, die2) > p


def score(n, s, dice):
    """Return the score, i.e., minimal cyclic win probability, of a dice list."""
    solution = slice_dice(n, s, dice)
    return min(
        win_probability(d1, solution[(i + 1) % n]) for i, d1 in enumerate(solution)
    )


def get_dice(n, s, dice):
    """Find by backtracking search n cyclic dice with s sides.

    a partial solution of size k is already given in dice
    """
    k = len(dice)
    if k == n * s:
        if beats(dice[-s:], dice[:s]):
            yield dice
        else:
            return
    else:
        for i in range(n * s):
            # already used
            if i in dice:
                continue
            # not the first element of a die, but not increasing
            if k % s != 0 and i <= dice[-1]:
                continue
            newd = dice + [i]
            # finished a die, and already more than two dice but not A>B
            if (
                k % s == s - 1
                and k + 1 >= 2 * s
                and not beats(newd[-2 * s : -s], newd[-s:])
            ):
                continue
            yield from get_dice(n, s, newd)

def find_dice(n, s):
    """Find by backtracking search n cyclic dice with s sides."""
    # we impose the very first element to be equal to 0
    yield from get_dice(n, s, [0])


def get_better_dice(n, s, dice, minscore=0.5, ref=None):
    """Find by backtracking search n cyclic dice with s sides

    a partial solution of size k is already given in dice
    each die beats the next with at least probability minscore
    the solution must be lexicographically greater than ref
    """
    k = len(dice)
    if k == n * s:
        if beats(dice[-s:], dice[:s], minscore):
            yield dice
        else:
            return
    else:
        for i in range(n * s):
            # already used
            if i in dice:
                continue
            if k % s != 0 and i <= dice[-1]:
                continue
            newd = dice + [i]
            if ref is not None:
                if i < ref[k]:
                    continue
                if i > ref[k]:
                    ref = None
            if (
                k % s == s - 1
                and k + 1 >= 2 * s
                and not beats(newd[-2 * s : -s], newd[-s:], minscore)
            ):
                continue
            yield from get_better_dice(n, s, newd, minscore, ref)


def optimal_dice(n, s):
    """Return a set of n s-sided dice with optimal score."""
    current_score = 0.5
    solution = None
    try:
        while True:
            solution = next(get_better_dice(n, s, [0], current_score, solution))
            current_score = score(n, s, solution)
            print(solution, current_score)
    except StopIteration:
        return solution
