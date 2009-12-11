
import os.path
import logging

from mako.template import Template
from mako.lookup import TemplateLookup
from soko.stats import formatting, tasking

PREFIX = ""
TEMPLATE_LOOKUP = None
TODISPLAY_SOLVERS = ["astar",
        "ida",
        "relaxastar",
        "relaxastar,hweight=1.2,one_way=True,greedy_on_exact=True",
        ] + tasking.get_measured_solvers()
TODISPLAY_LEVEL_PREFIX = "data/sokoban/microban/"

TITLES = {
        "num_visited": "The number of visited states",
        "cost": "The solution cost",
        }

def setup(url_prefix="", format_exceptions=True):
    global TEMPLATE_LOOKUP
    global PREFIX
    PREFIX = url_prefix
    TEMPLATE_LOOKUP = TemplateLookup(directories=["web/templates/"],
            format_exceptions=format_exceptions)

def render(records, measured="num_visited"):
    records = _filter_ignored(records)
    levels = sorted(set(task[0] for timestamp, task, result in records))
    levels.sort()

    specs = sorted(set(task[1] for timestamp, task, result in records))
    totals = [0] * len(specs)

    title = TITLES[measured]

    rows = []
    for level in levels:
        row = []
        row.append(level)
        for i, spec in enumerate(specs):
            result = _find_result(records, level, spec)
            value = None
            if result is not None:
                value = getattr(result, measured)
                totals[i] += value
            row.append((value, result))

        rows.append(row)

    heading = ["Level"] + specs
    footer = ["Totals"] + totals
    return _render("stats.html",
            title=title,
            heading=heading, rows=rows,
            footer=footer, prefix=PREFIX)

def _filter_ignored(records):
    todisplay = []
    for timestamp, task, result in records:
        level_filename, spec = task
        if spec not in TODISPLAY_SOLVERS:
            continue
        if not level_filename.startswith(TODISPLAY_LEVEL_PREFIX):
            continue
        todisplay.append((timestamp, task, result))

    return todisplay

def _find_result(records, level, spec):
    key_task = (level, spec)
    for timestamp, task, result in records:
        if task == key_task:
            return result

    return None

def _render(template_name, **kw):
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        import pprint
        logging.debug("template keywords:\n%s", pprint.pformat(kw))

    if TEMPLATE_LOOKUP is None:
        setup()
    template = TEMPLATE_LOOKUP.get_template(template_name)
    return template.render(formatting=formatting, **kw)
