# --------------------------------------------------------------------
import math, random

# --------------------------------------------------------------------
def torus_volume_cuboid(R, r, N = 100_000):
    Rr = R + r

    def sample():
        x = random.uniform(-Rr, Rr)
        y = random.uniform(-Rr, Rr)
        z = random.uniform(-r, r)
        return (math.sqrt(x ** 2 + y ** 2) - R) ** 2 + z ** 2 < r ** 2

    return sum(int(sample()) for _ in range(N)) / N * (8 * (Rr ** 2) * r)

# --------------------------------------------------------------------
def torus_volume_cylinder(R, r, N = 100_000):
    Rr = R + r

    def sample():
        th = random.uniform(0, 2 * math.pi)
        u  = Rr * math.sqrt(random.random())
        x  = u * math.cos(th)
        y  = u * math.sin(th)
        z  = random.uniform(-r, r)
        return (math.sqrt(x ** 2 + y ** 2) - R) ** 2 + z ** 2 < r ** 2

    return sum(int(sample()) for _ in range(N)) / N * (2 * math.pi * (Rr ** 2) * r)

# --------------------------------------------------------------------
def torus_volume_pipe(R, r, N=100_000):
    def sample():
        th = random.uniform(0, 2 * math.pi)
        u  = math.sqrt(random.uniform((R - r) ** 2, (R + r) ** 2))
        x  = u * math.cos(th)
        y  = u * math.sin(th)
        z  = random.uniform(-r, r)
        return (math.sqrt(x ** 2 + y ** 2) - R) ** 2 + z ** 2 < r ** 2

    return sum(int(sample()) for _ in range(N)) \
               / N * (2 * math.pi * ((R + r) ** 2 - (R - r) ** 2) * r)
