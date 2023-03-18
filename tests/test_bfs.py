import pytest
from project.bfs import bfs
from tests.utils import adj_matrix_from_edge_list


@pytest.mark.parametrize(
    "edge_list, source, ans",
    [
        (
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
            0,
            [0, 1, 2, 3, 4, 5],
        ),
        (
            [(0, 1), (0, 2), (0, 3), (0, 4)],
            0,
            [0, 1, 1, 1, 1],
        ),
        (
            [(0, 1), (1, 2), (2, 3), (3, 0)],
            2,
            [2, 3, 0, 1],
        ),
    ],
)
def test_bfs(edge_list, source, ans):
    graph = adj_matrix_from_edge_list(edge_list)
    assert bfs(graph, source) == ans
