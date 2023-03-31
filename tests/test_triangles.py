import pytest

from project.triangles import (
    vertex_to_triangle_count,
    cohen_triangles,
    sandia_triangles,
)
from tests.utils import adj_matrix_from_edge_list


@pytest.mark.parametrize(
    "edge_list, ans",
    [
        (
            [(0, 1)],
            [0, 0],
        ),
        (
            [(0, 1), (1, 2), (2, 0)],
            [1, 1, 1],
        ),
        (
            [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)],
            [1, 1, 2, 1, 1],
        ),
    ],
)
def test_vertex_to_triangles_count(edge_list, ans):
    graph = adj_matrix_from_edge_list(edge_list, directed=False)
    assert vertex_to_triangle_count(graph) == ans


@pytest.mark.parametrize(
    "edge_list, ans",
    [
        (
            [(0, 1)],
            0,
        ),
        (
            [(0, 1), (1, 2), (2, 0)],
            1,
        ),
        (
            [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)],
            2,
        ),
    ],
)
def test_triangles(edge_list, ans):
    graph = adj_matrix_from_edge_list(edge_list, directed=False)
    calculators = [cohen_triangles, sandia_triangles]
    assert all(triangle_calculator(graph) == ans for triangle_calculator in calculators)
