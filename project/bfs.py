from typing import List, Tuple
from pygraphblas import Matrix, BOOL, Vector, INT64
from pygraphblas.descriptor import RC

__all__ = ["bfs", "ms_bfs"]


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


def ms_bfs(graph: Matrix, source: List[int]) -> List[Tuple[int, List[int]]]:
    """
    Multi-source BFS of a directed graph from given source vertices

    Parameters
    ----------
    graph: Matrix
        adjacency boolean matrix of graph
    source: List[int]
        list of source vertices

    Returns
    -------
    result: List[Tuple[int, List[int]]]
        list of pairs consisting of a source vertex and a list of parents on
        the shortest path from this vertex.
        parent of source vertex is -1, parent of unreachable vertex is -2
    """
    m, n = len(source), graph.ncols
    assert graph.square
    assert graph.type == BOOL
    assert all(v in range(n) for v in source)

    parents = Matrix.sparse(INT64, nrows=m, ncols=n)
    front = Matrix.sparse(INT64, nrows=m, ncols=n)

    for i, v in enumerate(source):
        parents[i, v] = -1
        front[i, v] = v

    while front:
        front.mxm(graph, INT64.MIN_FIRST, out=front, mask=parents.pattern(), desc=RC)
        parents.assign(front, mask=front.pattern())
        front.apply(INT64.POSITIONJ, out=front, mask=front.pattern())

    return [
        (v, [parents.get(i, j, default=-2) for j in range(n)])
        for i, v in enumerate(source)
    ]
