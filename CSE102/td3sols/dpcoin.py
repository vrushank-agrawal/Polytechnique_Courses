import math as math

CURRENCY = [9,7,3,1]

# --------------------------------------------------------------------
def transacts_num(n):
    num_transacts = [math.inf] * (n + 1)
    num_transacts[0] = 0
    for i in range(1, n+1):
        for v in CURRENCY:
            if v <= i:
                num_transacts[i] = min(num_transacts[i], num_transacts[i - v] + 1)
    
    return num_transacts[-1]

# another bottom-up version, using hash tables and single for loop
# combined with a list comprehension
def transacts_num_v2(n):
    cache = {}
    cache[0] = 0
    for i in range(1, n+1):
        cache[i] = min ([1 + cache[i-v] for v in CURRENCY if i-v >= 0])
    return cache[n]

# --------------------------------------------------------------------
# similar algorithm to transacts_num, but now keeping track of (just) the last coin
# used in an optimal payment.  Note this has O(n) space complexity.
def transacts_list(n):
    num_coins = [math.inf] * (n + 1)
    num_coins[0] = 0
    last_coin = [0] * (n + 1)
    for i in range(1, n + 1):
        for v in CURRENCY:
            if v <= i and num_coins[i] > num_coins[i - v] + 1:
                num_coins[i] = num_coins[i - v] + 1
                last_coin[i] = v

    result = []
    to_pay = n
    while to_pay > 0:
        result.append(last_coin[to_pay])
        to_pay -= last_coin[to_pay]
    
    return result

# a more concise version of transacts_list, very similar to transacts_v2 but now
# storing lists of transacts in the hash table.  Note, though, that this
# version has O(n^2) space complexity.
def transacts_list_v2(n):
    cache = {}
    cache[0] = []
    for i in range(1,n+1):
        cache[i] = min ([[c] + cache[i-c] for c in CURRENCY if i-c >= 0],
                        key = len)
    return cache[n]

# --------------------------------------------------------------------
def collusion_number(A, B):
    m = len(A)
    n = len(B)
    c = [[0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(1,m+1):
        for j in range(1,n+1):
            if A[i-1] == B[j-1]:
                c[i][j] = c[i-1][j-1] + 1
            else:
                c[i][j] = max(c[i][j-1], c[i-1][j])
    return c[m][n]

# --------------------------------------------------------------------
def collusion_list(A, B):
    m = len(A)
    n = len(B)
    c = [[[] for _ in range(n+1)] for _ in range(m+1)]
    
    for i in range(1,m+1):
        for j in range(1,n+1):
            if A[i-1] == B[j-1]:
                c[i][j] = c[i-1][j-1] + [(i-1,j-1)]
            else:
                c[i][j] = max(c[i][j-1], c[i-1][j], key = lambda p : len(p))
    return c[m][n]


lorem = ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', \
         'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', \
         'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua']

def print_message(msg):
    print('\n'.join([' '.join(blk) for blk in msg]))

# --------------------------------------------------------------------
def block_tax(L, B):
    ell = sum ([len(w) + 1 for w in B]) - 1
    return (L - ell) ** 3 if ell <= L else math.inf
    
# --------------------------------------------------------------------
def text_charge(L, T):
    min_penalty = {}
    min_penalty[0] = 0
    for i in range(1,len(T)+1):
        min_penalty[i] = min ([min_penalty[j] + block_tax(L,T[j:i])
                               for j in range(i)])
    return min_penalty[len(T)]

# --------------------------------------------------------------------
def text_blocks(L, T):
    min_penalties = {}
    min_penalties[0] = []
    for i in range(1,len(T)+1):
        min_penalties[i] = min ([min_penalties[j] + [T[j:i]] for j in range(i)],
                                key = lambda msg:
                                      sum([block_tax(L,blk) for blk in msg]))
    return min_penalties[len(T)]
