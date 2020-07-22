#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

import click
import tqdm


def install_r_package(
    cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, command_prefix="R --quiet -e"
):
    # we're calling R to do this...
    command = f'{command_prefix} "{cmnd}"'.strip()
    proc = subprocess.Popen(command, shell=True, stdout=stdout, stderr=stderr)
    out, err = proc.communicate()
    if proc.returncode != 0:
        msg = err
        sys.stderr.writelines(f"FAILED: {command}\n\n{msg}\n")
        sys.exit(proc.returncode)

    if out is not None:
        r = out.decode("utf8")
    else:
        r = None
    return r


def install_r_packages(packages):
    for pack in tqdm.tqdm(packages):
        cmnd = f"if (! '{pack}' %in% installed.packages()[,'Package']) install.packages('{pack}', repos='http://cran.rstudio.com/')"
        install_r_package(cmnd)


def rkernel():
    """installs the R kernel for Jupyter"""
    r_kernel_dependencies = [
        "repr",
        "IRdisplay",
        "evaluate",
        "crayon",
        "pbdZMQ",
        "devtools",
        "uuid",
        "digest",
        "stringi",
        "devtools",
    ]

    # installing the kernel dependencies
    click.secho("Install dependencies for IRkernel", fg="blue")
    install_r_packages(r_kernel_dependencies)
    # installing the R kernel
    click.secho("Install and configure IRkernel", fg="blue")
    cmnd = "if (! 'IRkernel' %in% installed.packages()[,'Package']) devtools::install_github('IRkernel/IRkernel')"
    install_r_package(cmnd)

    # install irkernel kernelspec for jupyter
    install_r_package("IRkernel::installspec(user = FALSE)")
    click.secho("\n\nDone!")


def cran(package_file):
    """installs CRAN packages"""
    cran_packages = [l.strip() for l in Path(package_file).read_text().splitlines()]
    click.secho("Install packages", fg="blue")
    install_r_packages(cran_packages)
    click.secho("\n\nDone!")


if __name__ == "__main__":
    main()
