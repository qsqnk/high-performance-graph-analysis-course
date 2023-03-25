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
