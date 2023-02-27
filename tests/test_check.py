import pytest
from numpy import array, log2, ndarray

from gutils import check


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

    check.expected_variables_types(
        [("counts", "int"), ("non_zero", "bool"), ("logged", "float")],
        locals(),
        array_types=True,
    )
    # dtype is wrong causes exception
    with pytest.raises(AssertionError):
        check.expected_variables_types(
            [("counts", "bool")],
            locals(),
            array_types=True,
        )

    # not array causes exception
    counts = counts.tolist()
    with pytest.raises(AssertionError):
        check.expected_variables_types(
            [("counts", "bool")],
            locals(),
            array_types=True,
        )


def test_expected_variables_attrib_values():
    counts = array(
        [
            [1323, 275, 2657, 2746, 0, 2746, 0, 2199, 566, 984, 749],
            [1039, 2165, 89, 0, 39, 0, 2746, 0, 1240, 1004, 929],
            [10, 0, 0, 0, 2707, 0, 0, 547, 0, 601, 386],
            [374, 306, 0, 0, 0, 0, 0, 0, 940, 157, 682],
        ],
        dtype=int,
    )
    check.expected_variables_attrib_values(
        [
            ("counts", (4, 11)),
        ],
        "shape",
        locals(),
    )

    with pytest.raises(AssertionError):
        check.expected_variables_attrib_values(
            [
                ("counts", (4, 10)),
            ],
            "shape",
            locals(),
        )


def test_function_does_not_fail_multi_args():
    def foo(a, b):
        return True

    a = ("a", "b")
    b = 42
    check.function_does_not_fail(foo, (a, b), multiple_args=True)
