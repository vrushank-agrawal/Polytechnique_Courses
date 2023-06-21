# --------------------------------------------------------------------
import random

# --------------------------------------------------------------------
def streak(N, k):
    count = 0
    for _ in range(N):
        if random.choice([True, False]):
            count += 1
            if count >= k:
                return True
        else:
            count = 0
    return False

# --------------------------------------------------------------------
def experiment(N, k, C = 100_000):
    return sum(int(streak(N, k)) for _ in range(C)) / C
