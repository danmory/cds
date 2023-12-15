# На основе алгоритма изложенного в статье:
# Solving Connected Dominating Set Faster than 2n
# https://people.idsia.ch/~grandoni/Pubblicazioni/FGK08alg.pdf

# Доказательства сложности O(1.94^n) и корректности работы алгоритма приведены в статье.

from itertools import permutations, combinations


class Graph:
    def __init__(self, vertices: int):
        self.V = set(range(vertices))
        self.adj: dict[int, set[int]] = {v: set() for v in range(vertices)}

    def add_edge(self, u: int, v: int):
        self.adj[u].add(v)
        self.adj[v].add(u)


def connected_dominating_set(G: Graph, S: set[int], D: set[int]) -> set[int] | None:
    # Проверка невыполнимости
    def infeasible(S: set[int], D: set[int]):
        if len(S.intersection(D)) > 0:
            return True
        if not is_dominating_set(G.V - D):
            return True

    # V \ (S v D)
    def available_nodes(S: set[int], D: set[int]):
        return G.V - S - D

    # Проверка, что S - доминирующее множество
    def is_dominating_set(S: set[int]):
        uncovered = G.V - S
        for u in uncovered:
            if not any(v in S for v in G.adj[u]):
                return False
        return True

    # Candidate vertices
    def candidates(S: set[int], D: set[int]):
        available = available_nodes(S, D)
        c: set[int] = set()
        for a in available:
            if any(v in S for v in G.adj[a]):
                c.add(a)
        return c

    # Promise vertices
    def promises(S: set[int], D: set[int]):
        available = available_nodes(S, D)
        p: set[int] = set()
        for a in available:
            if not is_dominating_set(G.V - D - {a}):
                p.add(a)
        return p

    # Free vertices
    def free(S: set[int]):
        return G.V - set().union(*(G.adj[v] for v in S))

    S = S.copy()
    D = D.copy()

    if infeasible(S, D):
        return None
    if is_dominating_set(S):
        return S

    c = candidates(S, D)
    p = promises(S, D)

    # Reduction (a)
    S = S.union(c.intersection(p))

    # Reduction (b)
    for pair in permutations(c - p, 2):
        f = free(S)
        if G.adj[pair[0]].intersection(f).issubset(G.adj[pair[1]].intersection(f)):
            D.add(pair[0])

    # Reduction (c)
    for v in available_nodes(S, D):
        f = free(S)
        if not any(w in G.adj[v] for w in f):
            D.add(v)

    # Branch (A)
    for v in candidates(S, D):
        if len(available_nodes(S, D).intersection(G.adj[v])) >= 3:
            return connected_dominating_set(G, S.union({v}), D) or connected_dominating_set(G, S, D.union({v}))
        for w in available_nodes(S, D):
            if w != v and not any(u in available_nodes(S, D) for u in G.adj[w]):
                return connected_dominating_set(G, S.union({v}), D) or connected_dominating_set(G, S, D.union({v}))

    # Branch (B)
    for v in available_nodes(S, D):
        for w in available_nodes(S, D):
            if w != v and v in G.adj[w]:
                U = available_nodes(S, D).intersection(
                    G.adj[w]) - G.adj[v] - {v}
                return connected_dominating_set(G, S, D.union({v})) or connected_dominating_set(G, S.union({v, w}), D) or connected_dominating_set(G, S.union({v}), D.union({w}).union(U))

    # Branch (C)
    for v in available_nodes(S, D):
        for w1 in free(S):
            for w2 in free(S):
                if w1 != w2 and w1 != v and w2 != v and w1 in G.adj[v] and w2 in G.adj[v]:
                    U1 = available_nodes(S, D).intersection(
                        G.adj[w1]) - G.adj[v] - {v}
                    U2 = available_nodes(S, D).intersection(
                        G.adj[w2]) - G.adj[v] - {v}
                    if w1 in G.adj[w2] and w1 in available_nodes(S, D) and w2 in D:
                        return connected_dominating_set(G, S, D.union({v})) or connected_dominating_set(G, S.union({v, w1}), D) or connected_dominating_set(G, S.union({v}), D.union({w1}).union(U1))
                    if w1 in G.adj[w2] and w1 in available_nodes(S, D) and w2 in available_nodes(S, D):
                        return connected_dominating_set(G, S, D.union({v})) or connected_dominating_set(G, S.union({v, w1}), D) or connected_dominating_set(G, S.union({v, w2}), D.union({w1})) or connected_dominating_set(G, S.union({v}), D.union({w1, w2}).union(U1, U2))
                    return connected_dominating_set(G, S, D.union({v})) or connected_dominating_set(G, S.union({v, w1}), D) or connected_dominating_set(G, S.union({v, w2}), D.union({w1})) or connected_dominating_set(G, S.union({v}), D.union({w1, w2}).union(U1)) or connected_dominating_set(G, S.union({v}), D.union({w1, w2}).union(U2))


if __name__ == "__main__":
    vertices = 9
    graph = Graph(vertices)
    graph.add_edge(0, 5)
    graph.add_edge(1, 5)
    graph.add_edge(1, 6)
    graph.add_edge(2, 6)
    graph.add_edge(2, 7)
    graph.add_edge(3, 7)
    graph.add_edge(4, 5)
    graph.add_edge(4, 6)
    graph.add_edge(4, 7)
    graph.add_edge(4, 8)

    result: set[int] | None = None
    for pair in combinations(list(graph.V), 2):
        cds = connected_dominating_set(graph, set({4, 5}), set())
        if cds is not None:
            if result is None or len(cds) < len(result):
                result = cds

    print("Min-CDS:", result)
