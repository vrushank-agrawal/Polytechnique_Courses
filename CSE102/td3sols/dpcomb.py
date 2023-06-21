import sys; sys.setrecursionlimit (10 ** 6)

# --------------------------------------------------------------------
def binom(n,k):
    if (k == 0):
        return 1
    if (k > n):
        return 0
    return binom(n-1,k) + binom(n-1,k-1)

# The number of calls to binom doubles with each recursive step until
# reaching the boundary conditions, and so a rough upper bound on the
# total number of recursive calls made by binom(n,k) is O(2^n)
# (although it will be less when k is close to 0 or n).

# Some timing statistics on my laptop:
# >>> timeit.timeit('binom(20,10)', setup='from dpcomb import binom', number=1)
# 0.09326671998132952
# >>> timeit.timeit('binom(30,15)', setup='from dpcomb import binom', number=1)
# 67.54809480899712s

# --------------------------------------------------------------------
def binom_td(n, k, cache = None):
    cache = {} if cache is None else cache
    if (n,k) in cache:
        return cache[n,k]
    if k == 0:
        return 1
    if k > n:
        return 0
    aout = binom_td(n-1,k,cache) + binom_td(n-1,k-1,cache)
    cache[n,k] = aout
    return aout

# Since binom_td saves the result of previous calls in the cache, the
# number of calls to binom_td only grows linearly with each recursive
# step, and so a rough upper bound on the total number of recursive
# calls made by binom_td(n,k) is O(n^2).

# Some timing statistics on my laptop:
# >>> timeit.timeit('binom_td(20,10)', setup='from dpcomb import binom_td', number=1)
# 0.0004961829981766641
# >>> timeit.timeit('binom_td(200,100)', setup='from dpcomb import binom_td', number=1)
# 0.009315028990386054

# --------------------------------------------------------------------
def parts_td(n, k = None, cache = None):
    cache = {} if cache is None else cache
    if k is None:
        return sum(parts_td(n,k,cache) for k in range(1,n+1))
    if (n,k) in cache:
        return cache[n,k]
    if k == 1:          # one partition into one part
        return 1
    if k > n:           # no partitions into > n parts
        return 0
    # apply recurrence relation for partitions into 1 < k <= n parts
    aout = parts_td(n-1,k-1,cache) + parts_td(n-k,k,cache)
    cache[n,k] = aout
    return aout

# --------------------------------------------------------------------
def parts_bu(n):
    cache = [[0 for _ in range(n+1)] for _ in range(n+1)]
    for m in range(1,n+1):
        cache[m][1] = 1
        for k in range(2,m+1):
            cache[m][k] = cache[m-1][k-1] + cache[m-k][k]
    return sum(cache[n][k] for k in range(1,n+1))

# Let's compare the running times of parts_td and parts_bu:
# >>> timeit.timeit('parts_td(100)', setup='from dpcomb import parts_td', number=1)
# 0.005361994000850245
# >>> timeit.timeit('parts_td(1000)', setup='from dpcomb import parts_td', number=1)
# 0.5516019070055336
# >>> timeit.timeit('parts_td(2000)', setup='from dpcomb import parts_td', number=1)
# 2.9291434490005486
# >>> timeit.timeit('parts_td(5000)', setup='from dpcomb import parts_td', number=1)
# 60.943428593018325
# >>> timeit.timeit('parts_bu(100)', setup='from dpcomb import parts_bu', number=1)
# 0.0014927639858797193
# >>> timeit.timeit('parts_bu(1000)', setup='from dpcomb import parts_bu', number=1)
# 0.1546913300117012
# >>> timeit.timeit('parts_bu(2000)', setup='from dpcomb import parts_bu', number=1)
# 0.5760251049941871
# >>> timeit.timeit('parts_bu(5000)', setup='from dpcomb import parts_bu', number =1)
# 4.662502398015931

# We see that parts_bu is significantly faster than parts_td, but they
# both exhibit roughly the same computational complexity, namely
# O(n^2).  The constant factor difference is likely explained by the
# overhead of checking whether something is in the cache and of
# maintaining the call stack in the top-down solution.


# --------------------------------------------------------------------
def iparts(n):
    cache = [[[] for _ in range(n+1)] for _ in range(n+1)]
    for m in range(1,n+1):
        cache[m][1] = [[m]]     # one partition into one part
        for k in range(2,m+1):  # partitions into two or more parts
            cache[m][k] = [p + [1] for p in cache[m-1][k-1]] + \
                          [list(map(lambda x:x+1, p)) for p in cache[m-k][k]] # shift all the parts by 1
    return [p for k in range(1,n+1) for p in cache[n][k]]

# --------------------------------------------------------------------
def dparts(n):
    # we maintain two tables, one for partitions whose smallest part is 1
    cache1 = [[[] for _ in range(n+1)] for _ in range(n+1)]
    # ...and one for partitions whose smallest part is >= 2
    cache2 = [[[] for _ in range(n+1)] for _ in range(n+1)]
    for m in range(1,n+1):
        if m > 1:
            cache2[m][1] = [[m]]
        else:
            cache1[m][1] = [[m]]
        for k in range(2,m+1):
            cache1[m][k] = [p + [1] for p in cache2[m-1][k-1]]
            cache2[m][k] = [list(map(lambda x:x+1, p)) for p in cache1[m-k][k] + cache2[m-k][k]]
    return [p for k in range(1,n+1) for p in cache1[n][k] + cache2[n][k]]
