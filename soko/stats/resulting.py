
import errno
import time
import cPickle as pickle
import re

from pylib import disk
from pylib.namedtuple import namedtuple

RESULTS_PATH = "../export/results.p"
SOLUTION_PATH_TEMPLATE = "../export/solutions/%(level_filename)s_%(spec)s"
SANITIZE_PATTERN = re.compile(r"[^a-zA-Z0-9()_=,-]")

Result = namedtuple("Result", "solved length cost num_visited")

def store_result(task, result):
    timestamp = int(time.time())
    record = (timestamp, tuple(task), tuple(result))
    _store_record(record)

def _store_record(record):
    records = get_records()
    records.append(record)
    disk.store_content(RESULTS_PATH, pickle.dumps(records))

def get_records():
    try:
        records = pickle.load(disk.open(RESULTS_PATH))
    except IOError, e:
        if e.errno == errno.ENOENT:
            records = []
        else:
            raise

    return records

def get_latest_records():
    latest = []
    records = get_records()
    seen = set()
    for timestamp, task, result in reversed(records):
        if task in seen:
            continue

        seen.add(task)
        latest.append((timestamp, task, Result(*result)))

    latest.reverse()
    return latest

def store_solution(task, solution):
    disk.store_content(_get_solution_filename(task), solution)

def _get_solution_filename(task):
    level_filename, spec = task
    spec = SANITIZE_PATTERN.sub("_", spec)
    return SOLUTION_PATH_TEMPLATE % locals()

