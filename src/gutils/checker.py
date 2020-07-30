"""functions for validating student nbgrader assignments"""


def variables_exist(var_names, scope):
    """raises an AssertionError if scope does not contain var_names"""
    absent = []
    for var_name in var_names:
        if var_name not in scope:
            absent.append(var_name)

    if absent:
        msg = ", ".join(f"{n}" for n in absent)
        raise AssertionError(f"The following expected variables are missing: {msg}")
