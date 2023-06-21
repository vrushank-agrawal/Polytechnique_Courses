#! /usr/bin/env python3

# --------------------------------------------------------------------
import collections, math

# --------------------------------------------------------------------
def shortest_route_len(G, s, t):
    # We simply do a BFS from `s` and stops when we hit `t` By the
    # properties of BFS, we know that the first time we hit a node, we
    # followed a path of shortest length.
    #
    # To know this path length, each time we reach a node for the
    # first time, we store its minimal distance from `s` in a
    # dedicated table `distance`.

    # With start at node `s`, which is of minimum distance `0` from
    # `s`.  All other nodes, currently, are marked as being at an
    # infinite distance from `s`.
    queue    = collections.deque([s])
    distance = [0 if i == s else math.inf for i in range(len(G))]

    while queue:
        # Pop next node to process.
        current = queue.popleft()

        if current == t:
            # We reached `t` & `distance[t]` is the minimum distance
            # between `s` and `t`.
            return distance[t]

        # Otherwise, we continue the BFS walk by appending all
        # (non-visited) `current`'s children to the queue.
        #
        # Note that, again by the BFS properties, these children are
        # at minimum distance `distance[current]+1` from `s`.
        for child in G[current]:
            if distance[child] != math.inf:
                # The node `child` has already been visited. This
                # means that `child` is on a cycle that we fully
                # visited: we ignore it.
                continue
            distance[child] = distance[current]+1
            queue.append(child)

    # We never reached `t`, i.e. there are no paths from `s` to `t`
    return math.inf

# --------------------------------------------------------------------
def shortest_route(G, s, t):
    # We do as for `shortest_route_len`. The only difference is that
    # for each node, we store it predecessor in the BFS iteration.
    #
    # When we reach `t`, to reconstruct the shortest path, we simply
    # walk back that path using the predecessors table.

    # In that version, `s` and `t` can be list of nodes. To handle
    # this, we simply add dummy nodes `s0` & `t0`, edges from `s0` to
    # the nodes of `s`, and edges from the nodes of `t` to `t0`.
    s = [s] if isinstance(s, int) else s
    t = [t] if isinstance(t, int) else t
    G = [adj[:] for adj in G] + [[], []]

    s0, t0 = len(G)-2, len(G)-1

    G[s0] = s[:]
    for u in t:
        G[u].append(t0)

    # With start at node `s0`, which is of minimum distance `0` from
    # `s0` and has no predecessor.  All other nodes, currently, are
    # marked as being at an infinite distance from `s` and have no
    # predecessor (yet).
    queue    = collections.deque([s0])
    distance = [0 if i == s0 else math.inf for i in range(len(G))]
    previous = [None] * len(G)

    while queue:
        # Pop next node to process.
        current = queue.popleft()

        if current == t0:
            # We reached `t`. We reconstruct the path by walking it
            # back using the `previous` table.
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            # We reverse that path and remove the dummy nodes
            return path[::-1][1:-1]

        # Otherwise, we continue the BFS walk by appending all
        # (non-visited) `current`'s children to the queue.
        #
        # Note that, again by the BFS properties, these children are
        # at minimum distance `distance[current]+1` from `s`. We also
        # update the `previous` table.
        for child in G[current]:
            if distance[child] != math.inf:
                # The node `child` has already been visited. This
                # means that `child` is on a cycle that we fully
                # visited: we ignore it.
                continue
            distance[child] = distance[current]+1
            previous[child] = current
            queue.append(child)

    # We never reached `t`, i.e. there are no paths from `s` to `t`
    return None

# --------------------------------------------------------------------
def shortest_duration(G, s, t):
    # We are going to convert the graph G to a new graph H:
    #
    #  - initially, H has the same nodes of G and no edges
    #
    #  - then, we iterate the following process: for any edge `i -> j`
    #    with positive weight `w`:
    #
    #    * we add `w-1` fresh nodes `n_1`, ..., `n_{w-1}` in H
    #    * we add, in H, edges from
    #      + i       -> w_1
    #      + n_k     -> n_{k+1} for k \in [1..w-2]
    #      + n_{w-1} -> j
    #
    #    That is, we create a path from `i` to `j` of length `w`, hence
    #    simulating the weight.
    #
    # In consequence, the weight of a path in G is equal to the length
    # of it counterpart in H. So finding the weight of a path with
    # minimum weight in G amounts to finding a path of minimal length
    # in H, a problem we already solved.

    # Initially, H has the same nodes of G and no edges
    H = [[] for _ in range(len(G))]

    # With now iterate over all the edges of G
    for i, adj in enumerate(G):
         for j, w in adj:
             # We have an edge from `i` to `j` in `G` with weight `w`
             assert w > 0

             # If the weight is 1, we simply add back the original
             # edge from `i` to `j` in `H`.
             if w == 1:
                 H[i].append(j)
             else:
                 # We start by adding `w-1` nodes to H. These nodes
                 # are numbered `b+0`, `b+1`, ..., `b+w-2` where `b`
                 # in the number of nodes in `H` when we started the
                 # processing of the edge `i` -> `j`.
    
                 b = len(H)                         # base index for new nodes
                 H.extend([[] for _ in range(w-1)]) # We create `w-1` nodes in H
    
                 # We now create the following path in H:
                 #   i -> b+0 -> b+1 -> ... -> b+w-2 -> j
                 H[i].append(b); H[b+w-2].append(j)
                 for k in range(w-2):
                     H[b+k].append(b+k+1)

    # We can now solve the initial problem using `shortest_route_len`
    return shortest_route_len(H, s, t)

# --------------------------------------------------------------------
def shortest_duration2(G, s, t):
    # We are going to use `shortest_duration` to solve that problem.

    # First, we create a new weighted graph H that is identical to G
    # with the exception that all weights have been increased by 1. We
    # do so to simulate that every change takes exactly one hour.

    H = [[(j, w+1) for j, w in row] for row in G]

    # Using `shortest_duration`, we can now compute the weight of the
    # shortest path from `s` to `t` in `H`:

    w = shortest_duration(H, s, t)

    # However, along a path made of `n+2` nodes (i.e. of `n+1` edges),
    # there are only `n` node changes. However, since we increased the
    # edges weight by `1` to take the node change cost into account,
    # our current `w` is shifted by 1. We need to correct that by
    # substracting `1`, i.e. to return `w-1`.
    #
    # There are however 2 corner cases:
    #
    #  - When there are no paths from `s` to `t`. In that case, `w` is
    #    equal to `math.inf` and so is `w-1`.
    #
    #  - When `s` is equal to `t`. In that case, `w` is equal to `0`
    #    and we should return `0`, note `-1`.

    return max(0, shortest_duration(H, s, t) - 1)

# ====================================================================
# This class eases the building of graphs (in adjacency list
# representation) where nodes are referenced using arbitrary labels
class GraphBuilder:
    def __init__(self):
        self.nodei = 0          # Next node index
        self.keys  = {}         # Mapping from node label to node index
        self.graph = []         # The actual graph

    def node(self, label):
        # Check if a node has been assigned to `label`. If not, create
        # such a node, using the next available index.
        #
        # The method returns the node index.
        if label not in self.keys:
            self.keys[label] = self.nodei
            self.nodei += 1; self.graph.append([])
        return self.keys[label]

    def add_edge(self, i, j):
        # Add a edge from `i` to `j`, where the values `i` and `j` are
        # node labels.
        i, j = self.node(i), self.node(j)
        self.graph[i].append(j)

# --------------------------------------------------------------------
# Yet another implementation of DFS
def dfs(G, u, visited):
    if u not in visited:
        visited.add(u)
        for v in G[u]:
            dfs(G, v, visited)

# --------------------------------------------------------------------
def fastest_route(F, s0, t0):
    def parse_time(s):
        # Convert a 'hh:mm' formatted time `s` into an integer
        # representing the number of seconds between midnight and
        # `s`.
        hh, mm = s.split(':', 1)
        return 60 * int(hh) + int(mm)

    builder = GraphBuilder();

    # Mapping between airport names and departure/arrival times for that airport
    aps = {}

    # Parse all the departure and arrival timnes in F
    F = [(s, t, parse_time(d), parse_time(a)) for s, t, d, a in F]

    # If there exists a flight from `(s, dept)` to `(t, arrt)`, add an
    # edge from `(s, dept)` to `(t, arrt)` in `builder`.
    for s, t, dept, arrt in F:
        builder.add_edge((s, dept), (t, arrt))
        aps.setdefault(s, (set(), set()))[0].add(dept)
        aps.setdefault(t, (set(), set()))[1].add(arrt)

    # Sort the departure/arrival times in aps.
    aps = { a: (list(sorted(t0)), list(sorted(t1)))
                 for a, (t0, t1) in aps.items() }

    # Add an edge from `(s, t1)` to `(s, t2)` if `t1` is an arrival
    # date and `t2` is a departure date strictly greater than `t1`.
    for a, ts in aps.items():
        for t1 in ts[1]:
            for t2 in ts[0]:
                if t2 > t1:
                    builder.add_edge((a, t1), (a, t2))

    # Then, we find all the paths between all nodes of the form `(s,
    # dept)` and `(t, arrt)` where `dept` is a departure time and
    # `arrt` is an arrival time. Note that by iterating the departure
    # time in decreasing order and arrival time by increasing order,
    # we can share the 'visited' set between the calls to `dfs` and we
    # can break the inner loop as soon as we detected a path.

    visited, best = set(), math.inf

    for dept in aps.get(s0, ([], []))[0][::-1]:
        dfs(builder.graph, builder.node((s0, dept)), visited)
        for arrt in aps.get(t0, ([], []))[1]:
            if builder.node((t0, arrt)) in visited:
                best = min(best, arrt - dept)
                break

    return best

# ====================================================================
def getd(xs, i, dfl):
    return xs[i] if 0 <= i < len(xs) else dfl

def maze__get(maze, i, j):
    # Return the `maze cell's content at row `i` and column `j`.
    #
    # Note that the maze is virtually infinite: all out of bounds
    # cells contain a well - see the `getd` function above.x

    return getd(getd(maze, i, []), j, 1)

def maze__nbh(maze, i, j):
    # Iterate over the cells of `maze` that are reachable from `i` and
    # `j`.  We assume that the cell `(i, j)` does not contain a wall.

    for i0, j0 in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if maze__get(maze, i0, j0) == 0:
            yield (i0, j0)

# --------------------------------------------------------------------
def shortest_escape(maze, start, finish):
    # We directly give a solution to `shortest_escape`.
    #
    # Yet again, we are going to do a BFS on the graph **induced**
    # by the maze. We won't create this graph directly on memory, but
    # instead, we write a BFS that works directly on a maze.
    #
    # The induced graph is constructed as follow:
    #
    #  - The nodes are denoted by pairs of integers (i, j) and
    #    represent the cell `(i, j)` in the maze.
    #
    #  - There is an edge from node `(i1, j1)` to node `(i2, j2)` if
    #    one can walk from `(i1, j1)` to `(i2, j2)` in the maze.
    #
    # Our BFS implementation will be a bit different from the one of
    # `shortest_route_len`: instead of constructing a table `previous`
    # to retain the path we are walking along, we use the stack to
    # store it.

    queue, visited = collections.deque(), set()

    # We start at `start`. The shortest path from `start` to `start`
    # is the empty path (hence the value `[]` as the second pair
    # component).
    queue.append((start, []))

    while queue:
        # The next cell to process is at location (i, j)
        # The shortest path to reach it is `path`
        (i, j), path = queue.popleft()


        if (i, j) in visited:
            # If (i, j) has already been visited, we ignore it
            # Otherwise, we are going to walk along a cycle
            continue

        # We store that (i, j) has now been processed
        visited.add((i, j))


        if (i, j) == finish:
            # If (i, j) == finish, we are done.
            return path + [(i, j)]

        # Otherwise, we iterate over the reachable neighbors of (i, j)
        # and push them in the stack, s.t. we eventually process
        # them.
        #
        # Note that we update the register paths by appending (i, j).
        for i0, j0 in maze__nbh(maze, i, j):
            queue.append(((i0, j0), path + [(i, j)]))
    return None

# --------------------------------------------------------------------
def shortest_escape_len(maze, start, finish):
    # We can solve `shortest_escape_len` by just returning the length
    # of shortest path from `start` to `finish` in `maze`.
    path = shortest_escape(maze, start, finish)
    return math.inf if path is None else len(path)-1
