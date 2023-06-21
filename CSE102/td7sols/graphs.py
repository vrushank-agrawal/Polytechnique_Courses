#! /usr/bin/env python3

# --------------------------------------------------------------------
def edges(G):
    # This function enumerates over all the edges of `G`
    #
    # `G` must be in adjacency list form
    for i, s in enumerate(G):
        yield from [(i, j) for j in s]

# --------------------------------------------------------------------
def matrix_to_adjlist(G):
    return [[j for j, b in enumerate(G[i]) if b] for i in range(len(G))]

# --------------------------------------------------------------------
def is_symmetric(G):
    # A graph is symmetric iff `u -> v` is an edge of `G` implies that
    # `v -> u` is also an edge of G.
    #
    # Note that, in adjacency list form, we can check that `u -> v` is
    # an edge of `G` by checking that `v` is in the adjacency list of
    # `u` i.e. if `v in G[u]`.

    # We iterate over all the edges `u -> v` of `G`. If `v -> u` is
    # not in `G`, then `G` is not symmetric.
    for u, v in edges(G):
        if not u in G[v]:
            return False
    return True

# --------------------------------------------------------------------
def revert_edges(G):
    # We first create a graph with the same number of nodes but with
    # no edges.
    rG = [[] for _ in range(len(G))]

    for u, v in edges(G):
        # Then, we iterate over the edges `u -> v` of `G` and, for
        # each of them, add the edge `v -> u` in `rG`.
        rG[v].append(u)

    return rG
