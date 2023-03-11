import pytest
from pygraphblas import Matrix, BOOL
from project.bfs import bfs


@pytest.mark.parametrize(
    "U, V, source, ans",
    [
        ([0, 1, 2, 3, 4], [1, 2, 3, 4, 5], 0, [0, 1, 2, 3, 4, 5]),
        (
            [0, 0, 0, 0],
            [1, 2, 3, 4],
            0,
            [0, 1, 1, 1, 1],
        ),
        (
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            2,
            [2, 3, 0, 1],
        ),
    ],
)
def test_bfs(U, V, source, ans):
    nrows = ncols = max(U + V) + 1
    graph = Matrix.from_lists(U, V, [True] * len(U), nrows=nrows, ncols=ncols)
    assert bfs(graph, source) == ans
