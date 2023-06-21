# --------------------------------------------------------------------
import random

# --------------------------------------------------------------------
def penney():
    s = []
    while True:
        s.append(random.choice([True, False]))
        if len(s) > 3:
            s.pop(0)
        if s == [True, True, False]:
            return True
        if s == [False, True, True]:
            return False

# --------------------------------------------------------------------
def experiment(N = 100_000):
    return sum(penney() for _ in range(N)) / N
