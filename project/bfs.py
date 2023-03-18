from typing import List
from pygraphblas import Matrix, BOOL, Vector, INT64
from pygraphblas.descriptor import RC

__all__ = [
    "bfs",
]


def bfs(graph: Matrix, source: int) -> List[int]:
    """
    BFS of a directed graph from a given source vertex

    Parameters
    ----------
    graph: Matrix
        adjacency boolean matrix of graph
    source: int
        source vertex

    Returns
    -------
    result: List[int]
        list where i-th value is distance of the shortest path from source to vertex i,
        if there is no path value is -1
    """
    n = graph.ncols
    assert graph.square
    assert graph.type == BOOL
    assert source in range(n)

    level = Vector.sparse(BOOL, n)
    level[source] = True
    ans = Vector.sparse(INT64, n)

    dist = 0
    while level:
        ans.assign_scalar(dist, mask=level)
        level.vxm(graph, out=level, mask=ans.pattern(), desc=RC)
        dist += 1

    return list(ans.vals)
