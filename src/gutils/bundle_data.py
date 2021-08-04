#!/usr/bin/env python3
"""bundles all non-python, non-r, non-ipynb script files into a dir
replacing with symlinks"""
import pathlib

import click


def get_data_paths(assign_dir: pathlib.Path, excludes):
    moving = []
    for fn in assign_dir.glob("**/*"):
        fn = fn.relative_to(assign_dir)
        if (
            str(fn).startswith(".")
            or fn.suffix.lower() in excludes
            or fn.name.startswith(".")
            or fn.is_dir()
            or fn.is_symlink()
        ):
            continue

        moving.append(assign_dir / fn)
    return moving


def get_dest(assign_dir: pathlib.Path, dest_dir: pathlib.Path, path):
    rel_to = path.relative_to(assign_dir)
    dest = dest_dir / rel_to
    dest_path = dest.relative_to(dest_dir)
    dest_parent = dest_dir / dest_path.parent
    return dest, dest_parent


def valid_assignment_dir(assign_dir: pathlib.Path):
    """an assignment dir must have at least one notebook"""
    nbks = list(assign_dir.glob("*.ipynb"))
    return len(nbks) >= 1


def main(dest_root_dir, assign_dir, force, dry_run):
    """copies data files (not directories) from assign_dir/ to dest_root_dir/assign_dir/data"""
    cwd = pathlib.Path(".").absolute()
    assign_dir = pathlib.Path(assign_dir).expanduser().absolute()
    try:
        assign_dir = assign_dir.relative_to(cwd)
    except ValueError:
        pass

    if not valid_assignment_dir(assign_dir):
        click.secho(f"Assignment directories must contain a .ipynb file", fg="red")
        exit()

    assert assign_dir.is_dir(), "assign_dir must be a directory"

    dest_root_dir = pathlib.Path(dest_root_dir).expanduser().absolute()
    assert dest_root_dir.is_dir(), "dest_root_dir must be a directory"

    dest_dir = dest_root_dir / assign_dir.name

    if dry_run:
        click.secho(f"Assignment dir: {assign_dir}", fg="blue")
        click.secho(f"Dest dir: {dest_dir}", fg="blue")

    excludes = [".py", ".r", ".ipynb", ".png", ".jpg", ".html", ".docx"]
    # get data paths
    data_paths = get_data_paths(assign_dir, excludes)
    created_paths = set()
    for data_path in data_paths:
        # create dest paths
        dest, dest_parent = get_dest(assign_dir, dest_dir, data_path)
        if dest.exists() and not force:
            click.secho(
                f"Exiting, '{dest}' already exists. Use -F to overwrite.", fg="red"
            )
            exit()

        # create dirs for dest paths
        if not dry_run:
            dest_parent.mkdir(parents=True, exist_ok=True)
            # move data to dest
            data_path.replace(dest)
            # create symlink at original path
            data_path.symlink_to(dest)
        else:
            if str(dest_parent) not in created_paths:
                click.secho(f"Will create path: '{dest_parent}'", fg="blue")
                created_paths.add(str(dest_parent))

            click.secho(
                f"Will move '{data_path}' to '{dest}'",
                fg="green",
            )
            click.secho(
                f"Will symlink '{dest}' to '{data_path}'",
                fg="green",
            )

    click.secho("Done!", fg="green")


if __name__ == "__main__":
    main()
