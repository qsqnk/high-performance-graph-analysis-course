import math
from typing import List, Tuple

from pygraphblas import Matrix, FP64

__all__ = [
    "sssp",
    "mssp",
    "apsp",
]


def sssp(graph: Matrix, source: int) -> List[int]:
    """
    Finds single-source shortest paths

    Parameters
    ----------
    graph: Matrix
        float adjacency matrix
    source: int
        source vertex

    Returns
    -------
    result: List[int]
        list where i-th value is distance from source to vertex i
    """
    return mssp(graph, [source])[0][1]


def mssp(graph: Matrix, source: List[int]) -> List[Tuple[int, List[int]]]:
    """
    Finds multiple-source shortest paths

    Parameters
    ----------
    graph: Matrix
        float adjacency matrix
    source: List[int]
        list of source vertices

    Returns
    -------
    result: List[Tuple[int, List[int]]]
        list containing of tuples (source, distances_from_source)
    """
    graph = _copy_with_zeroes_on_main_diag(graph)
    m, n = len(source), graph.ncols
    assert graph.type == FP64
    assert graph.square
    assert all(v in range(n) for v in source)

    dists = Matrix.sparse(FP64, nrows=m, ncols=n)
    for i, start in enumerate(source):
        dists[i, start] = 0

    for _ in range(n - 1):
        dists.mxm(graph, FP64.MIN_PLUS, out=dists)

    if dists.isne(dists.mxm(graph, FP64.MIN_PLUS)):
        raise ValueError("Negative cycle detected")

    return [
        (start, [dists.get(i, j, default=math.inf) for j in range(n)])
        for i, start in enumerate(source)
    ]


def apsp(graph: Matrix) -> List[Tuple[int, List[int]]]:
    """
    Finds all-pairs shortest paths

    Parameters
    ----------
    graph: Matrix
        float adjacency matrix

    Returns
    -------
    result: List[Tuple[int, List[int]]]
        list containing of tuples (source, distances_from_source)
    """
    graph = _copy_with_zeroes_on_main_diag(graph)
    n = graph.ncols
    assert graph.type == FP64
    assert graph.square

    dists = graph

    for k in range(n):
        col, row = dists.extract_matrix(col_index=k), dists.extract_matrix(row_index=k)
        dists.eadd(
            col.mxm(row, FP64.MIN_PLUS),
            FP64.MIN,
            out=dists,
        )

    for k in range(n):
        col, row = dists.extract_matrix(col_index=k), dists.extract_matrix(row_index=k)
        if dists.isne(
            dists.eadd(
                col.mxm(row, FP64.MIN_PLUS),
                FP64.MIN,
            )
        ):
            raise ValueError("Negative cycle detected")

    return [
        (i, [dists.get(i, j, default=math.inf) for j in range(n)]) for i in range(n)
    ]


def _copy_with_zeroes_on_main_diag(matrix: Matrix) -> Matrix:
    copy = matrix.dup()
    for i in range(matrix.ncols):
        copy[i, i] = 0.0
    return copy
