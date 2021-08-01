# inserts a markdown cell into nbgrader assignment notebooks
import json
import pathlib

MARK_COMMENT = "This part worth"


def remove_previous(source):
    """removes all previous lines containing a mark"""
    result = [l for l in source if MARK_COMMENT not in l]
    # now remove all blank lines at the start
    return [l for l in result if l.strip()]


def insert_total(cell, point):
    cell["source"] = remove_previous(cell["source"])
    is_code = cell["cell_type"] != "markdown"
    msg = (
        f"# {MARK_COMMENT} {point}\n\n" if is_code else f"`{MARK_COMMENT} {point}`\n\n"
    )
    cell["source"].insert(0, msg)


def inject_mark_comments(path):
    with open(path) as infile:
        data = json.load(infile)

    total = 0
    for cell in data["cells"]:
        try:
            points = cell["metadata"]["nbgrader"]["points"]
            total += float(points)
        except KeyError:
            points = None

        if points is not None:
            insert_total(cell, points)

    # backup original
    i = 0
    while True:
        new = f"{path}.bak" if not i else f"{path}.bak.{i}"
        new = pathlib.Path(new)
        i += 1
        if not new.exists():
            break
    path.rename(new)

    output = json.dumps(data, indent=2)
    path.write_text(output)

    print(f"total assignment points = {total}")


def main(path):
    path = pathlib.Path(path)
    inject_mark_comments(path)
