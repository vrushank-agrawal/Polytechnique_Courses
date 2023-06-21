# --------------------------------------------------------------------
def next_seq(alphas, us):
    return sum((x * y for x, y in zip(alphas, us)), 0)

# --------------------------------------------------------------------
def u(alphas, us, n):
    for _ in range(n):
        us = us[1:] + [next_seq(alphas, us)]
    return (us or [0])[0]

# --------------------------------------------------------------------
def fibo(n):
    return u([1, 1], [0, 1], n)
