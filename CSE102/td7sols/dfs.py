#! /usr/bin/env python3

# --------------------------------------------------------------------
import graphs

# --------------------------------------------------------------------
def dfs(G, u, visited = None):
    # Before continuing, we implement a recursive version of DFS.
    # See the course Jupyter notebook for more details.

    # By default, we start with a fresh `visited` set...
    visited = set() if visited is None else visited

    # ...then, we our DFS...
    if u not in visited:
        visited.add(u)
        for v in G[u]:
            dfs(G, v, visited)

    # ...and return the visited set.
    return visited

# --------------------------------------------------------------------
def required(G, c):
    # For finding the number of courses that have to be passed in
    # order to pass `c`, we simply to a graph traversal from `c` and
    # count the number of visited nodes.
    return len(dfs(G, c))

# --------------------------------------------------------------------
def required_list(G, cs):
    # For finding the number of courses that have to be passed in
    # order to pass all the courses in `cs`, we simply to a graph
    # traversal for each `c` in `cs` and return the set visited nodes.
    #
    # Note that the set of visited nodes must be shared among the
    # different calls of `dfs`.
    #
    # Note that `cs` might also be a single course. In that case, we
    # put it in a singleton list.

    cs = [cs] if isinstance(cs, int) else cs
    vs = set()

    for c in cs:
        dfs(G, c, vs)

    return list(vs)

# --------------------------------------------------------------------
def needed_for(G, c):
    # `needed_for` is the dual of `required` (`u` requires `v` iff `v`
    # is needed for `u`). So we simply call `required` of the
    # symmetric of `G`.
    return required(graphs.revert_edges(G), c)

# --------------------------------------------------------------------
def cyclic_dependence(G):
    # This is the set of nodes we already visited
    visited = set()

    # This function check wether there exists a cycle that goes
    # through `i`. The variable `path` contains the path we followed
    # so far. The variables `actives` contains the nodes of `path`
    # (but this will be faster to check that a node is in `actives`
    # than in `path`)
    def check_cycle(i, path, actives):
        # If `i` is in active, then `i` is already part of
        # `path`. This means that we found a path. However, we might
        # after walked some nodes before reaching this cycle and we
        # have to prune them from `path`. To achieve this, we simply
        # remove all the nodes in path before the first (and only)
        # occurence of `i` in `path`.
        if i in actives:
            return path[path.index(i):] + [i]
        # If `i` is in `visited`, then we already check wether there
        # exists a cycke that is reachable from `i`.
        if i in visited:
            return
        # Otherwise, we add `i` to the set of visited nodes...
        visited.add(i)
        # ...and we check wether there exists a cycle reachable from
        # any of `i`'s children.
        for j in G[i]:
            aout = check_cycle(j, path + [i], actives.union({i}))
            if aout is not None:
                # We exit the function as soon as we detect a cycle
                return aout

    # Now, it suffices to check wether there exists a cycle reachable
    # from any node of G.
    for i in range(len(G)):
        aout = check_cycle(i, [], set())
        if aout is not None:
            return aout

    # No cycle detected
    return []
