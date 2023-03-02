"""functions for validating student nbgrader assignments"""
import copy
import traceback

from numpy import ndarray


def expected_variables_exist(var_names, scope, callables=None):
    """raises an AssertionError if scope does not contain expected var_names"""
    callables = callables or []
    absent = [var_name for var_name in var_names if var_name not in scope]
    not_callable = [
        func
        for func in callables
        if not callable(scope.get(func)) and func not in absent
    ]
    msgs = []
    if absent:
        msg = ", ".join(f"{n}" for n in absent)
        msg = f"The following expected variables are missing: {msg}"
        msgs.append(msg)

    if not_callable:
        msg = ", ".join(f"{n}" for n in not_callable)
        msgs.append(f"The following are not callable: {msg}")

    if msgs:
        raise AssertionError("\n".join(msgs))


def expected_variables_types(names_types, scope, array_types=False):
    """raises an AssertionError if type of name in scope not in expected

    if array_types, checks `dtype` attribute"""
    wrong = []
    names_types = dict(names_types)
    for name, type_ in names_types.items():
        if name not in scope:
            wrong.append(f"'{name}' not present")
            continue

        value = scope[name]
        if array_types and not isinstance(value, ndarray):
            wrong.append(f"{name} type pf {type(value)}!=ndarray")
            continue

        if array_types and type_ not in str(value.dtype):
            wrong.append(f"dtype prefix {type_} not in '{value.dtype}' for '{name}'")
        elif not array_types:
            expect = {type_} if isinstance(type_, type) else set(type_)
            if type(value) not in expect:
                wrong.append((f"type of '{name}'='{type(value)}' not in {expect}"))

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
            wrong.append(f"value of {name}={got} does not equal {expect}")

    if wrong:
        msg = "\n".join(wrong)
        raise AssertionError(f"The following variables had incorrect values: {msg}")


def expected_variables_attrib_values(names_values, attrib_name, scope):
    """
    Parameters
    ----------
    names_values
        variable name, expected attribute value
    attrib_name
        name of attribute expected to exist on variables
    scope

    Raises AssertionError if attribute does not exist or value of attribute
    incorrect.
    """
    wrong = []
    names_values = dict(names_values)
    for name, expect in names_values.items():
        if name not in scope:
            wrong.append(f"'{name}' not present")
            continue

        attrib_value = getattr(scope[name], attrib_name, None)
        if attrib_value is None:
            wrong.append(f"'{name}' does not have attribute {attrib_name}")
            continue

        if attrib_value != expect:
            expect = repr(expect) if isinstance(expect, str) else expect
            got = repr(attrib_value) if isinstance(attrib_value, str) else attrib_value
            wrong.append(
                (f"value of {name}.{attrib_name}={got} does not equal {expect}")
            )

    if wrong:
        msg = "\n".join(wrong)
        raise AssertionError(f"The following variables were incorrect: {msg}")


def function_does_not_fail(func, *inputs, multiple_args=False):
    """function does not fail on the provided inputs"""
    errors = []
    for input in inputs:
        try:
            if multiple_args:
                _ = func(*input)
            else:
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
            got_types = None

        if got_types != expected_types and got_types is not None:
            msg = (
                f"{got_types[0]} != {expected_types[0]}"
                if single
                else f"{got_types} != {expected_types}"
            )
            errors.append(msg)

    if errors:
        raise AssertionError("\n".join(errors))


_accessory = {
    "pandas": ["pandas", "numpy", "dateutil", "pytz", "six"],
    "numpy": ["numpy"],
    "cogent3": [
        "_cffi_backend",
        "mpi4py",
        "wcwidth",
        "platformdirs",
        "jedi",
        "jupyter_client",
        "cogent3",
        "ptyprocess",
        "decorator",
        "ipykernel",
        "pycparser",
        "asttokens",
        "yaml",
        "pickleshare",
        "pure_eval",
        "tornado",
        "typing_extensions",
        "ipython_genutils",
        "pexpect",
        "executing",
        "zmq",
        "parso",
        "comm",
        "tinydb",
        "backcall",
        "psutil",
        "entrypoints",
        "prompt_toolkit",
        "six",
        "tqdm",
        "cffi",
        "numba",
        "ipywidgets",
        "IPython",
        "scipy",
        "jupyter_core",
        "colorama",
        "stack_data",
        "pygments",
        "scitrack",
        "dateutil",
        "traitlets",
        "llvmlite",
        "chardet",
        "plotly",
        "_plotly_utils",
        "_distutils_hack",
        "pkg_resources",
        "sphinxcontrib",
        "numpy",
    ],
    "plotly": [
        "plotly",
        "_plotly_utils",
        "_distutils_hack",
        "sphinxcontrib",
    ],
    "jupyter": [
        "argcomplete",
        "storemagic",
        "ipython_genutils",
        "appnope",
        "traitlets",
        "pickleshare",
        "jupyter_client",
        "_pydev_bundle",
        "parso",
        "prompt_toolkit",
        "ptyprocess",
        "pexpect",
        "_distutils_hack",
        "_pydevd_bundle",
        "IPython",
        "setuptools",
        "dateutil",
        "pygments",
        "pydevconsole",
        "_pydevd_frame_eval",
        "sphinxcontrib",
        "decorator",
        "wcwidth",
        "backcall",
        "colorama",
        "entrypoints",
        "six",
        "_pydev_runfiles",
        "distutils",
        "pydevd_tracing",
        "numpy",
        "jupyter_core",
        "zmq",
        "pkg_resources",
        "ipykernel",
        "debugpy",
        "pydevd_file_utils",
        "pydevd_plugins",
        "jedi",
        "gutils",
        "pydev_ipython",
        "tornado",
        "pydevd",
    ],
}


def allowed_modules(allowed=None):
    import inspect
    import pathlib
    import sys

    invalid = set()
    allowed = allowed or []
    allowed.append("jupyter")
    if allowed:
        for k, v in _accessory.items():
            if k in allowed:
                allowed.extend(v)

    allowed.extend(sys.builtin_module_names)
    allowed = set(allowed)
    for name, module in sorted(sys.modules.items()):
        if not inspect.ismodule(module):
            continue
        name = name.split(".")[0]
        if name in allowed:
            continue

        try:
            name = module.__name__.split(".")[0]
        except AttributeError:
            print(name, type(module))
            exit()
        f = getattr(module, "__file__", "") or ""
        path = pathlib.Path(f)
        if "site-packages" in path.parts:
            invalid.add(name.split(".")[0])

    if invalid:
        invalid = ", ".join(f"{i!r}" for i in invalid)
        raise RuntimeError(f"the following 3rd-party modules not allowed: {invalid}")


def trapped_result(func, *args, **kwargs):
    """if func fails, returns the triggered exception type as a string"""
    try:
        result = func(*args, **kwargs)
    except Exception:
        result = traceback.format_exc().splitlines()[-1:]
    return result


def two_funcs_equivalent(func1, func2, *args, **kwargs):
    r1 = trapped_result(func1, *copy.deepcopy(args), **copy.deepcopy(kwargs))
    r2 = trapped_result(func2, *copy.deepcopy(args), **copy.deepcopy(kwargs))
    assert r1 == r2, f"Outputs from {func1.__name__} != {func2.__name__}\n{r1}\n{r2}\n"
    return True
