import math

import pytest

from project.shortest_paths import sssp
from tests.utils import float_adj_matrix_from_edge_list


@pytest.mark.parametrize(
    "edge_list, source, ans",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2)],
            1,
            [math.inf, 0.0, 1.0],
        ),
        (
            [(0, 1.0, 1), (1, 2.0, 2), (2, 3.0, 0)],
            0,
            [0.0, 1.0, 3.0],
        ),
        ([(0, 1.0, 1), (0, 2.0, 2), (1, 1.0, 3), (2, 1.0, 3)], 0, [0.0, 1.0, 2.0, 2.0]),
    ],
)
def test_sssp(edge_list, source, ans):
    graph = float_adj_matrix_from_edge_list(edge_list)
    assert sssp(graph, source) == ans
