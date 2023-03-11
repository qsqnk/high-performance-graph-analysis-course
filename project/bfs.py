from typing import List
from pygraphblas import Matrix, BOOL, Vector, INT64

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
        list where i-th value is dist_from_source of the shortest path from source to vertex i,
        if there is no path value is -1
    """
    n = graph.ncols
    assert graph.square
    assert graph.type == BOOL
    assert source in range(n)

    level = Vector.sparse(BOOL, n)
    used = Vector.sparse(BOOL, n)
    ans = Vector.dense(INT64, n, fill=-1)

    level[source] = True
    dist_from_source = 0
    prev_used = None

    while prev_used != used.nvals:
        prev_used = used.nvals
        ans.assign_scalar(dist_from_source, mask=level)
        used |= level
        level @= graph
        level.assign_scalar(False, mask=used)
        dist_from_source += 1

    return list(ans.vals)
