#!/usr/bin/env python3
"""bundles all non-python, non-r, non-ipynb script files into a dir
replacing with symlinks"""
import datetime
import pathlib
from warnings import simplefilter

simplefilter("ignore", Warning)

import click

import gutils.bundle_data as BD
import gutils.inject_marks as MK
import gutils.nbgrader_fetched as FETCH
import gutils.rinstall as RK


@click.group()
def main():
    """utilities for nbgrader etc.."""
    pass


@main.command()
@click.argument("assign_dir", type=click.Path(exists=True))
@click.argument("dest_root_dir", type=click.Path(), default="/home/data")
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


@main.command()
@click.option("-i", "--uni_id", required=True, help="student ID")
def student_fetch_record(uni_id):
    """displays times when student fetched assignments"""
    FETCH.check_student(uni_id)


@main.command()
@click.argument("notebooks", required=True, type=click.Path(exists=True))
def inject_marks(notebooks):
    """inserts how many points each nbgrader assessed cell is worth"""
    MK.main(notebooks)


@main.command()
@click.argument("submitted_dir", type=click.Path(exists=True))
@click.argument("assignment_name", type=str)
def nb2py(submitted_dir, assignment_name):
    """convert notebook to just the script portion"""
    from gutils.nb2py import make_scripts

    make_scripts(submitted_dir, assignment_name)


def _assessment_key(name):
    import re

    digit = re.compile("\d$")
    if digit.search(name):
        n = int(name[-1])
    else:
        n = 4
    q = 1 if "quiz" in name else 2
    topic = {"python": 1, "seqcomp": 2, "molevol": 3, "microres": 4}[name.split("_")[0]]
    return topic, q, n


@main.command()
@click.argument("outdir", required=True, type=pathlib.Path, default=".")
def export_grades(outdir):
    """export all assignments in the gradebook.db"""

    outdir = outdir.expanduser().absolute()

    if not outdir.is_dir():
        outdir = str(outdir)
        click.secho(f"{outdir=} must be a directory", fg="red")
        exit(1)

    import os
    import re

    from cogent3 import make_table
    from nbgrader.api import Gradebook

    valid_user = re.compile("grader-biol(3157|6243)")
    course = re.compile("(biol3157|biol6243)")
    topics = re.compile("(python|seqcomp|molevol|microres)")

    user = os.environ["USER"]
    if not valid_user.search(user):
        click.secho(f"Invalid user {user!r}")
        exit(1)

    rootdir = pathlib.Path("~").expanduser()
    courseid = course.findall(user)[0]
    gradebook_path = rootdir / courseid / "gradebook.db"

    today = datetime.date.today()
    outpath = outdir / f"{courseid}-{today:%Y-%m-%d}.tsv"

    if not gradebook_path.exists():
        click.secho(f"Could not find {str(gradebook_path)!r}")
        exit(1)

    gb = Gradebook(f"sqlite:///{str(gradebook_path)}")

    assignment_scores = {}
    students = {}
    for assignment in gb.assignments:
        if not topics.search(assignment.name):
            continue

        results = {}
        for s in assignment.submissions:
            students[s.student_id] = s.student
            results[s.student_id] = s.score
        assignment_scores[assignment.name] = results

    student_ids = {s: s for s in students}
    data = {
        "anuid": student_ids,
        "name": {
            s: " ".join((students[s].first_name, students[s].last_name))
            for s in students
        },
    }
    assignment_titles = sorted(assignment_scores, key=lambda x: _assessment_key(x))
    for title in assignment_titles:
        scores = assignment_scores[title]
        data[title] = {s: scores.get(s, 0.0) for s in student_ids}

    table = make_table(data=data, digits=2)
    table.write(outpath)
    click.secho(f"Wrote {str(outpath)!r}", fg="green")


if __name__ == "__main__":
    main()
