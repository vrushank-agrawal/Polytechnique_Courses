# --------------------------------------------------------------------
def maze(m, n, i, j):
    if i == n-1 and j == n-1:
        return [(n-1, n-1)]

    positions = [(i+1, j), (i, j+1)]

    for i1, j1 in positions:
        if not (i1 < n and j1 < n):
            continue
        if not m[i1][j1]:
            continue
        path = maze(m, n, i1, j1)
        if path is not None:
            return [(i, j)] + path

# --------------------------------------------------------------------
def maze_4d_r(m, n, i, j, visited):
    if (i, j) in visited:
        return None

    if i == n-1 and j == n-1:
        return [(n-1, n-1)]

    positions = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

    while positions:
        i1, j1 = positions.pop()
        if 0 <= i1 < n and 0 <= j1 < n:
            if not m[i1][j1]:
                continue
            path = maze_4d_r(m, n, i1, j1, visited.union([(i, j)]))
            if path is not None:
                return [(i, j)] + path
    
def maze_4d(m, n, i, j):
    return maze_4d_r(m, n, i, j, set())
