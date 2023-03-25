from typing import List

from pygraphblas import Matrix, BOOL, INT64
from pygraphblas.descriptor import T0

__all__ = [
    "vertex_to_triangle_count",
    "cohen_triangles",
    "sandia_triangles",
]


def vertex_to_triangle_count(graph: Matrix) -> List[int]:
    """
    For each vertex of undirected graph calculates number of triangles that contain given vertex

    Parameters
    ----------
    graph: Matrix
        adjacency boolean matrix of undirected graph

    Returns
    -------
    result: List[int]
        list where i-th value is count of triangles that contain vertex i
    """
    _assert_is_adjacency_matrix_of_undirected_graph(graph)
    ans_v = graph.mxm(graph, cast=INT64, mask=graph).reduce_vector(desc=T0)
    ans_v = ans_v.dense(INT64, size=ans_v.size, fill=ans_v if ans_v.nvals else 0)
    return [count // 2 for count in ans_v.vals]


def cohen_triangles(graph: Matrix) -> int:
    """
    Calculates number of triangles in undirected graph using Cohen's algo

    Parameters
    ----------
    graph: Matrix
        adjacency boolean matrix of undirected graph

    Returns
    -------
    result: int
        number of triangles
    """
    _assert_is_adjacency_matrix_of_undirected_graph(graph)
    l, u = graph.tril(), graph.triu()
    return sum(l.mxm(u, cast=INT64, mask=graph).nvals) // 2


def sandia_triangles(graph: Matrix) -> int:
    """
    Calculates number of triangles in undirected graph using Sandia algo

    Parameters
    ----------
    graph: Matrix
        adjacency boolean matrix of undirected graph

    Returns
    -------
    result: int
        number of triangles
    """
    u = graph.triu()
    return sum(u.mxm(u, cast=INT64, mask=u).nvals)


def _assert_is_adjacency_matrix_of_undirected_graph(m: Matrix):
    assert m.square
    assert m.type == BOOL
    assert m.iseq(m.transpose())
