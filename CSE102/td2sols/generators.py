def fibs():
    a = 0
    b = 1

    while True:
        yield a
        a , b = b , a+b

def prefix_sums(k):
    sum = k
    while True:
        yield sum
        k += 1
        sum += k

def interleave(g1,g2):
    while True:
        yield next(g1)
        g1 , g2 = g2 , g1

def choose_gen(S,k):
    if (k == 0):
        yield []
        return
    if (k > len(S)):
        return
    x = S[0]
    for R in choose_gen(S[1:],k-1):
        yield [x] + R
    yield from choose_gen(S[1:],k)
    #### note: instead of "yield from" we could equivalently write...
    # for R in choose_gen(S[1:],k):
    #    yield R
    
def subsets_gen(S):
    for k in range(len(S)+1):
        yield from choose_gen(S,k)

def permutations_gen(elems):
    if not elems:
        yield []
        return
    for p in permutations_gen(elems[1:]):
        for i in range(len(elems)):
            yield p[0:i] + [elems[0]] + p[i:]

# below is a non-recursive solution, which generates permutations using "Algorithm L"
# from Knuth's The Art of Computer Programming (Volume 4a, section 7.2.1.2)
def permutations_gen_NR(elems):
    if elems == []:
        yield []
        return
    
    n = len(elems)
    perm = [i for i in range(n+1)]

    while True:
        yield [elems[i-1] for i in perm[1:]]
        
        j = n-1
        while perm[j] >= perm[j+1]:
            j -= 1

        if j == 0:
            return
        
        l = n
        while perm[j] >= perm[l]:
            l -= 1
        perm[j] , perm[l] = perm[l] , perm[j]
        
        k = j + 1
        l = n
        while k < l:
            perm[k] , perm[l] = perm[l] , perm[k]
            k += 1
            l -= 1

def repeat(x):
    while True:
        yield x

def cross(n, g):
    while True:
        for i in range(n-1):
            yield next(g)
        next(g)
        yield False
        
def sieve():
    yield False
    yield False
    n = 2
    g = repeat(True)
    while True:
        if next(g):
            yield True
            g = cross(n,g)
        else:
            yield False
        n = n+1

def prime_pi(n):
    g = sieve()
    k = 0
    for i in range(n+1):
        if next(g):
            k = k+1
    return k
    
