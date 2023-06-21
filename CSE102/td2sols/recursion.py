import math

def binom(n,k):
    if (k == 0):
        return 1
    if (k > n):
        return 0
    return binom(n-1,k) + binom(n-1,k-1)

# We can write the choose function so that it's recursive structure
# exactly mirrors the recursive structure of binom above...
def choose(S,k):
    if (k == 0):
        return [[]]
    if (k > len(S)):
        return []
    return [[S[0]] + R for R in choose(S[1:],k-1)] + choose(S[1:],k)
    # Here in the recursive case we used a list comprehension, resulting in
    # very concise code, but alternatively we could have used a for loop.

def permutations(xs):
    if not xs:
        return [xs]
    return [perm[0:i] + [xs[0]] + perm[i:]
            for perm in permutations(xs[1:])
            for i in range(len(xs))]

def multichoose(S,k):
    if (k == 0):
        return [[]]
    if k > len(S):
        return []
    return [[S[0]] + R for R in multichoose(S[1:],k-1)] + \
        [R for R in multichoose([y for y in S[1:] if y > S[0]],k)]

def not_angry(n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    return not_angry(n - 1) + not_angry(n - 2)

def not_so_angry(k, n):
    if n <= k:
        return 2**n
    return sum([not_so_angry(k, n - i - 1) for i in range(k + 1)])

def find_assignment(prices):
    n = len(prices)
    if n == 0:
        return (0, [])
    best_price = math.inf
    best_assignment = None
    for to_last in range(n):
        prices_but_last = [p[:to_last] + p[(to_last + 1):] for p in prices[:-1]]
        (price, assign) = find_assignment(prices_but_last)
        if best_price > price + prices[-1][to_last]:
            best_price = price + prices[-1][to_last]
            best_assignment = [a + int(a >= to_last) for a in assign]
            best_assignment.append(to_last)
    return (best_price, best_assignment)
