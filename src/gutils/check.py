"""functions for validating student nbgrader assignments"""


def expected_variables_exist(var_names, scope):
    """raises an AssertionError if scope does not contain expected var_names"""
    absent = [var_name for var_name in var_names if var_name not in scope]
    if absent:
        msg = ", ".join(f"{n}" for n in absent)
        raise AssertionError(f"The following expected variables are missing: {msg}")


def expected_variables_types(names_types, scope):
    """raises an AssertionError if type of name in scope not in expected"""
    wrong = []
    names_types = dict(names_types)
    for name, type_ in names_types.items():
        if name not in scope:
            wrong.append(f"'{name}' not present")
            continue

        expect = {type_} if isinstance(type_, type) else set(type_)
        got = type(scope[name])
        if got not in expect:
            wrong.append((f"type of '{name}'='{got}' not in {expect}"))

    if wrong:
        msg = "\n".join(wrong)
        raise AssertionError(f"The following variables had an incorrect type: {msg}")


def expected_variables_values(names_values, scope):
    """raises an AssertionError if type of name in scope not in expected"""
    wrong = []
    names_values = dict(names_values)
    for name, expect in names_values.items():
        if name not in scope:
            wrong.append(f"'{name}' not present")
            continue

        got = scope[name]
        if got != expect:
            expect = repr(expect) if isinstance(expect, str) else expect
            got = repr(got) if isinstance(got, str) else got
            wrong.append((f"value of {name}={got} does not equal {expect}"))

    if wrong:
        msg = "\n".join(wrong)
        raise AssertionError(f"The following variables had incorrect values: {msg}")


def function_does_not_fail(func, *inputs):
    """function does not fail on the provided inputs"""
    errors = []
    for input in inputs:
        try:
            _ = func(input)
        except Exception as err:
            msg = f"failed on {input}: {err}"
            errors.append(msg)
    if errors:
        raise AssertionError("\n".join(errors))


def _get_types(result, single):
    if single:
        result = [result]

    return [type(item) for item in result]


def function_returned_correct_types(func, expected_types, *inputs):
    """function returns types matching expected_types"""
    if isinstance(expected_types, type):
        expected_types = [expected_types]
        single = True
    else:
        single = False
    errors = []
    for input in inputs:
        try:
            got = func(input)
            got_types = _get_types(got, single)
        except Exception as err:
            msg = f"failed on {input}: {err}"
            errors.append(msg)

        if got_types != expected_types:
            msg = (
                f"{got_types[0]} != {expected_types[0]}"
                if single
                else f"{got_types} != {expected_types}"
            )
            errors.append(msg)

    if errors:
        raise AssertionError("\n".join(errors))
