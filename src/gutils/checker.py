"""functions for validating student nbgrader assignments"""


def variables_exist(var_names, scope):
    """raises an AssertionError if scope does not contain var_names"""
    absent = [var_name for var_name in var_names if var_name not in scope]
    if absent:
        msg = ", ".join(f"{n}" for n in absent)
        raise AssertionError(f"The following expected variables are missing: {msg}")

def variables_types(names_types, scope):
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

def variables_values(names_values, scope):
    """raises an AssertionError if type of name in scope not in expected"""
    wrong = []
    names_values = dict(names_values)
    for name, expect in names_values.items():
        if name not in scope:
            wrong.append(f"'{name}' not present")
            continue

        got = scope[name]
        if got != expect:
            wrong.append((f"value of '{name}'='{got}' does not equal {expect}"))


    if wrong:
        msg = "\n".join(wrong)
        raise AssertionError(f"The following variables had incorrect values: {msg}")

