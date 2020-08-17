#!/usr/bin/env python3
"""Export grades for each cell to json"""

import json
import sys

from nbgrader.api import MissingEntry
from nbgrader.plugins import ExportPlugin


class PerCellExporter(ExportPlugin):
    """
    Export plugin for nbgrader which ouputs per-cell grades to a json formatted file.
    """

    def export(self, gradebook):
        grades = {}

        # It's awful, but I think this nested for loop is the only way to proceed
        for assignment in gradebook.assignments:
            grades[assignment.name] = {}

            for notebook in assignment.notebooks:
                grades[assignment.name][notebook.name] = {}

                for grade_cell in notebook.grade_cells:
                    grades[assignment.name][notebook.name][grade_cell.name] = {}

                    for student in gradebook.students:
                        try:
                            grade = gradebook.find_grade(
                                grade_cell.name,
                                notebook.name,
                                assignment.name,
                                student.id,
                            )
                            grades[assignment.name][notebook.name][grade_cell.name][
                                student.id
                            ] = grade.score
                        except MissingEntry:
                            grades[assignment.name][notebook.name][grade_cell.name][
                                student.id
                            ] = None

        if self.to:
            out_file = self.to
        else:
            out_file = "grades.json"

        with open(out_file, "w") as f:
            json.dump(grades, f, indent=4)


def main():
    sys.exit(
        "Usage: $ nbgrader export --exporter=gutils.per_cell_export.PerCellExporter"
    )


if __name__ == "__main__":
    main()
