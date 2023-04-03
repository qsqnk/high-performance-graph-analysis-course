from typing import List, Tuple

from pygraphblas import Matrix


def adj_matrix_from_edge_list(
    edge_list: List[Tuple[int, int]], directed=True
) -> Matrix:
    if not directed:
        edge_list += [(j, i) for i, j in edge_list]
    u, v = zip(*edge_list)
    n = max(u + v) + 1
    return Matrix.from_lists(u, v, [True] * len(u), nrows=n, ncols=n)


def float_adj_matrix_from_edge_list(
    edge_list: List[Tuple[int, float, int]], directed=True
) -> Matrix:
    if not directed:
        edge_list += [(j, w, i) for i, w, j in edge_list]
    u, w, v = zip(*edge_list)
    n = max(u + v) + 1
    return Matrix.from_lists(u, v, w, nrows=n, ncols=n)
