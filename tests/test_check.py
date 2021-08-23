import pytest

from numpy import array, ndarray
from numpy import log2


def test_array_types():
    counts = array(
        [
            [1323, 275, 2657, 2746, 0, 2746, 0, 2199, 566, 984, 749],
            [1039, 2165, 89, 0, 39, 0, 2746, 0, 1240, 1004, 929],
            [10, 0, 0, 0, 2707, 0, 0, 547, 0, 601, 386],
            [374, 306, 0, 0, 0, 0, 0, 0, 940, 157, 682],
        ],
        dtype=int,
    )
    non_zero = counts != 0
    logged = counts.astype(float)
    logged[non_zero] = log2(logged[non_zero])

    from gutils import check

    check.expected_variables_types(
        [("counts", "int"), ("non_zero", "bool"), ("logged", "float")],
        locals(),
        array_types=True,
    )
