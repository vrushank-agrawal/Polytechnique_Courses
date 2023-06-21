# --------------------------------------------------------------------
def catalan(n):
    if n <= 0:
        return 1
    return sum(catalan(i) * catalan(n-1-i) for i in range(0, n))

# --------------------------------------------------------------------
def catalan_td(n, cache = None):
    cache = {} if cache is None else cache

    if n not in cache:
        if n <= 0:
            cache[n] = 1
        else:
            cache[n] = sum(
                catalan_td(i, cache) * catalan_td(n-1-i, cache)
                for i in range(0, n))

    return cache[n]

# --------------------------------------------------------------------
def next_catalan(cs):
    if cs == []:
        return 1
    return sum(cs[i] * cs[-i-1] for i in range(len(cs)))

def catalan_bu(n):
    cache = []
    for _ in range(n+1):
        cache.append(next_catalan(cache))
    return cache[-1]
