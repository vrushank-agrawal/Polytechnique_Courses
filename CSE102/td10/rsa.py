# -*- coding: utf-8 -*-
"""
Created on Tue May 04 01:38:21 2021

@author: Vrushank Agrawal
"""

import random

# --------------------------------------------------------------------
#EXERCISE 1

def is_prime(n, k = 32):
    if n <= 3:
        return True
    if n%2 == 0:
        return False
    
    r = 0
    d = n-1
    while d%2 == 0:
        r += 1
        d //= 2
    
    for i in range(k):  
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if (x == 1 or x == n-1):
            continue
        for j in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True
    
    
# --------------------------------------------------------------------
#EXERCISE 2

def genprime(l):
    
    no = random.getrandbits(l)
    no = no | 1 << 0
    no = no | 1 << l
    i = 0
    while True:
        if (is_prime(no + 2*i)):
            return no + 2*i
        i+=1

    
# --------------------------------------------------------------------
#EXERCISE 3

def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

def genmod(p, q) :  
    phi = (p-1) * (q-1)
    while True:
        e = random.randint(2, phi - 1)
        gcd, u, v = egcd(e, phi)
        if gcd == 1:
            break
    print(u)
    if u < 0:
        k = (3 - u)/phi
        u += k * phi
    print(k)
    print(u)
    # return ((p*q, e), 3)


# --------------------------------------------------------------------
#EXERCISE 4

def kengen(l):
    
    
    pass
