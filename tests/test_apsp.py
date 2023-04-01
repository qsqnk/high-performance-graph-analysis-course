import math

import pytest

from project.shortest_paths import apsp
from tests.utils import float_adj_matrix_from_edge_list


@pytest.mark.parametrize(
    "edge_list, ans",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2)],
            [
                (0, [0.0, 1.0, 2.0]),
                (1, [math.inf, 0.0, 1.0]),
                (2, [math.inf, math.inf, 0.0]),
            ],
        ),
        (
            [(0, 1.0, 1), (1, 2.0, 2), (2, 3.0, 0)],
            [(0, [0.0, 1.0, 3.0]), (1, [5.0, 0.0, 2.0]), (2, [3.0, 4.0, 0.0])],
        ),
        (
            [(0, 1.0, 1), (0, 2.0, 2), (1, 1.0, 3), (2, 1.0, 3)],
            [
                (0, [0.0, 1.0, 2.0, 2.0]),
                (1, [math.inf, 0.0, math.inf, 1.0]),
                (2, [math.inf, math.inf, 0.0, 1.0]),
                (3, [math.inf, math.inf, math.inf, 0.0]),
            ],
        ),
    ],
)
def test_apsp(edge_list, ans):
    graph = float_adj_matrix_from_edge_list(edge_list)
    assert apsp(graph) == ans
