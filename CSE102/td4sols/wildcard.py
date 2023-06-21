def wildcard(s, p):
    if (p == ""):
       return (s == "")
 
    lk = [
        [False for i in range(len(p) + 1)]
        for j in range(len(s) + 1)
    ]
 
    lk[0][0] = True
 
    for j in range(1, len(p) + 1):
        if (p[j - 1] == '*'):
            lk[0][j] = lk[0][j - 1]
 
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if (p[j - 1] == '*'):
                lk[i][j] = lk[i][j - 1] or lk[i - 1][j]
 
            elif (p[j - 1] == '?' or s[i - 1] == p[j - 1]):
                lk[i][j] = lk[i - 1][j - 1]
 
            else:
                lk[i][j] = False
 
    return lk[len(s)][len(p)]
