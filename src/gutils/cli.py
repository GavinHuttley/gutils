#!/usr/bin/env python3
"""bundles all non-python, non-r, non-ipynb script files into a dir
replacing with symlinks"""
import pathlib

import click

import gutils.bundle_data as BD
import gutils.nbgrader_fetched as FETCH
import gutils.rinstall as RK


@click.group()
def main():
    """utilities for nbgrader etc.."""
    pass


@main.command()
@click.argument("assign_dir", type=click.Path(exists=True))
@click.argument("dest_root_dir", type=click.Path(), default="/home2/data")
@click.option("-F", "--force", flag_value=True, help="force over write of dest_dir")
@click.option("-D", "--dry_run", flag_value=True, help="display what will be done")
def bundle_data(dest_root_dir, assign_dir, force, dry_run):
    """replaces assignment directory data files with symlinks after moving originals to another location"""
    BD.main(dest_root_dir, assign_dir, force, dry_run)


@main.command()
def rkernel():
    """installs the R kernel for Jupyter"""
    RK.rkernel()


@main.command()
@click.argument("package_file", required=True, type=click.Path(exists=True))
def cran(package_file):
    """installs CRAN packages"""
    RK.cran(package_file)


@main.command()
def log_fetched():
    """logs times when assignments fetched to a json file"""
    FETCH.main()


if __name__ == "__main__":
    main()
