# convert student notebooks to python scripts
import json
import pathlib
import re

_excludes = re.compile(
    "(Additional checks|ANUID|Enter your code here|This part worth|complete this function)"
)


def get_code_cells(path):
    path = pathlib.Path(path)
    with open(path) as infile:
        data = json.load(infile)

    result = []
    for cell in data["cells"]:
        if cell["cell_type"] == "markdown" or cell.get("metadata", {}).get(
            "nbgrader", {}
        ).get("grade"):
            continue
        code = "\n".join(l.rstrip() for l in cell["source"] if not _excludes.search(l))
        if code:
            result.extend([code, "\n", "\n"])

    return "".join(result)


def make_scripts(indir, assignment_name):
    indir = pathlib.Path(indir)
    paths = indir.glob("**/*.ipynb")
    for path in paths:
        if assignment_name not in path.parts:
            continue
        code = get_code_cells(path)
        outpath = path.parent / f"{path.stem}.py"
        outpath.write_text(code)

