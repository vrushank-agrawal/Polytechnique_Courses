# ---------------------------------------------------------------------
import random, math

# --------------------------------------------------------------------
def area3(p1, p2, p3):
    return abs(
        p1[0] * (p2[1] - p3[1]) + \
        p2[0] * (p3[1] - p1[1]) + \
        p3[0] * (p1[1] - p2[1])) / 2

# --------------------------------------------------------------------
def bounding_rect(p1, p2, p3):
    xs  = [p1[0], p2[0], p3[0]]
    ys  = [p1[1], p2[1], p3[1]]
    bb1 = (min(xs), min(ys))
    bb2 = (max(xs), max(ys))
    return (bb1, bb2)

# --------------------------------------------------------------------
def pt_in_triangle(p, p1, p2, p3):
    value = area3(p, p1, p2) + area3(p, p2, p3) + area3(p, p1, p3)
    return math.isclose(value, area3(p1, p2, p3))

# --------------------------------------------------------------------
def rejection_sample3(p1, p2, p3):
    bb1, bb2 = bounding_rect(p1, p2, p3)
    while True:
        x = random.uniform(bb1[0], bb2[0])
        y = random.uniform(bb1[1], bb2[1])
        if pt_in_triangle((x, y), p1, p2, p3):
            return (x, y)

# --------------------------------------------------------------------
def quick_sample3(p1, p2, p3):
    u = (p2[0] - p1[0], p2[1] - p1[1])
    v = (p3[0] - p1[0], p3[1] - p1[1])
    a = random.random()
    b = random.random()

    if a + b > 1:
        (a, b) = (1 - b, 1 - a)

    return (a * u[0] + b * v[0] + p1[0], a * u[1] + b * v[1] + p1[1])
