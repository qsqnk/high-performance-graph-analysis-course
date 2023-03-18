import pytest
from project.bfs import ms_bfs
from tests.utils import adj_matrix_from_edge_list


@pytest.mark.parametrize(
    "edge_list, source, ans",
    [
        (
            [(0, 1), (1, 2), (2, 0)],
            [0],
            [(0, [-1, 0, 1])],
        ),
        (
            [(0, 1), (0, 2), (0, 3)],
            [0, 3],
            [(0, [-1, 0, 0, 0]), (3, [-2, -2, -2, -1])],
        ),
        (
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
            [0, 1, 2],
            [
                (0, [-1, 0, 1, 2, 3, 4]),
                (1, [-2, -1, 1, 2, 3, 4]),
                (2, [-2, -2, -1, 2, 3, 4]),
            ],
        ),
    ],
)
def test_ms_bfs(edge_list, source, ans):
    graph = adj_matrix_from_edge_list(edge_list)
    assert ms_bfs(graph, source) == ans
