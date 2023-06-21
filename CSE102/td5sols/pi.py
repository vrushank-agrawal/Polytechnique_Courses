# --------------------------------------------------------------------
import sys, math, random

def gcd(x, y):
    while (y):
        x, y = y, x % y
    return x

# --------------------------------------------------------------------
def pi_coprimality(N = 100_000):
    def sample():
        n1 = random.randint(0, sys.maxsize)
        n2 = random.randint(0, sys.maxsize)
        return math.gcd(n1, n2) == 1

    return math.sqrt(6 * N / sum(int(sample()) for _ in range(N)))

# --------------------------------------------------------------------
def pi_evenness(N = 100_000):
    fails = [round(random.random() / random.random()) & 0b1 for _ in range(N)]
    return 5 - 4 * (1 - sum(fails) / N)

# --------------------------------------------------------------------
def pi_chords(N = 100_000):
    def sample():
        while True:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x ** 2 + y ** 2 <= 1:
                norm = math.sqrt(x ** 2 + y ** 2)
                if norm != 0:
                    return (x, y, norm)

    return 4 * N / sum(
        math.sqrt((x / norm - 1) ** 2 + (y / norm) ** 2)
        for x, y, norm in [sample() for _ in range(N)])

# --------------------------------------------------------------------
def pi_circle_segments(N = 100_000):
    def sample_circle():
        # we are going to cheat and use polar coordinates
        theta  = random.uniform(0, 2 * math.pi)
        radius = math.sqrt(random.random())
        return (theta, radius)

    def sample():
        th1, r1 = sample_circle()
        th2, r2 = sample_circle()
        return math.sqrt(
            (r1 * math.cos(th1) - r2 * math.cos(th2)) ** 2 +
            (r1 * math.sin(th1) - r2 * math.sin(th2)) ** 2)

    return 128 * N / 45 / sum(sample() for _ in range(N))
