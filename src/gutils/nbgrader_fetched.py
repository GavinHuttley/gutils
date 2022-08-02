import json
import pathlib
import re
import time


def get_courseid():
    """returns the name of the courseid, which will also be
    the directory interrogated in student accounts"""
    import socket

    hostname = socket.gethostname().split(".")
    courseid = hostname[0].replace("bio", "biol")
    return courseid


USER_ROOT = pathlib.Path("/home2")
COURSEID = get_courseid()
EXHCHANGE_OUTBOUND = pathlib.Path(f"/home/srv/nbgrader/exchange/{COURSEID}/outbound/")
LOGPATH = pathlib.Path("/home/srv/nbgrader/nbgrader_fetched.json")


def get_student_homes():
    """returns all student home directories"""
    pattern = re.compile("u\d+$")
    student_homes = []
    for dn in USER_ROOT.glob("u*"):
        if pattern.search(str(dn)):
            student_homes.append(dn)
    return student_homes


def get_released_assignments():
    """returns the list of released assignments"""
    assignments = []
    for dn in EXHCHANGE_OUTBOUND.glob("*"):
        if dn.is_dir():
            assignments.append(dn.name)
    return assignments


def get_student_fetched_times(stored):
    """returns a dict of {<assignment>: {<student>: created time}, adds new records to stored"""
    student_homes = get_student_homes()
    assignments = set(get_released_assignments())
    for assignment in assignments:
        if assignment not in stored:
            stored[assignment] = {}

        for home in student_homes:
            if home.name in stored[assignment]:
                continue

            expected_path = home / COURSEID / assignment
            if not expected_path.exists():
                continue

            t = time.ctime(expected_path.stat().st_mtime)
            stored[assignment][home.name] = t

    return stored


def load_log():
    """loads the existing log data"""
    data = json.loads(LOGPATH.read_text()) if LOGPATH.exists() else {}
    return data


def write_log(data):
    """loads the existing log data"""
    if LOGPATH.exists():
        bk = pathlib.Path(f"{LOGPATH}.bak")
        LOGPATH.rename(bk)
    else:
        bk = None

    log = json.dumps(data)
    LOGPATH.write_text(log)
    if bk:
        # safely remove the backup
        bk.unlink()


def main():
    if not USER_ROOT.exists():
        print("Expected dir /home2, which doesn't exist. Exiting")
        exit(1)

    currlog = load_log()
    mods = get_student_fetched_times(currlog)
    write_log(mods)


def check_student(student_id):
    from cogent3 import make_table

    currlog = load_log()
    columns = ["Assignment", "Time Seen"]
    result = {c: [] for c in columns}
    for assignment in currlog:
        time = currlog[assignment].get(student_id, "None")
        result["Assignment"].append(assignment)
        result["Time Seen"].append(time)

    table = make_table(columns, data=result, title=f"Fetch times for {student_id}")
    print(table)
