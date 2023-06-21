# --------------------------------------------------------------------
import random

# --------------------------------------------------------------------
def roll(D):
    ns, total = [], 0
    for x in D:
        ns.append(total); total += x
    i, x = len(D), random.random()
    while x < ns[i-1]:
        i -= 1
    return i

# --------------------------------------------------------------------
def rolls(D, N):
    aout = [0] * len(D)
    for _ in range(N):
        aout[roll(D)-1] += 1
    return aout
