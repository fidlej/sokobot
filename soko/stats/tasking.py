
from pylib.namedtuple import namedtuple
from soko import mazing

Task = namedtuple("Task", "level_filename spec")
TASKS = None

def get_tasks():
    if TASKS is None:
        _define_tasks()
    return TASKS

def _add(level_filename, spec):
    TASKS.append(Task(level_filename, spec))

def get_measured_solvers():
    solvers = [
        "astar",
        #"astar,hweight=1.2",
        #"macroastar",
        #"macroastar,hweight=2",
        #"pgastar",
        #"pgastar,hweight=2",
        #"pgastar,hweight=5",
        #"relaxastar",
        #"relaxastar,one_way=True,greedy_on_exact=True",
        #"relaxastar,hweight=1.2,one_way=True,greedy_on_exact=True",
        #"relaxastar,hweight=2,one_way=True,greedy_on_exact=True",
        #"relaxpgastar,hweight=1.2,one_way=True,greedy_on_exact=True",
        #"relaxpgastar,hweight=2,one_way=True,greedy_on_exact=True",
        #"ida",
        #"ida,one_way=True",
        #"ida,hweight=1.2",
        #"pgida",
        #"pgida,hweight=5",
        #"pgida,one_way=True,hweight=5",
        #"pgida,one_way=True,hweight=5,unprefpenalty=2",
        #"pgida,unprefpenalty=2",
        #"pgida,hweight=5",
        #"pgida,hweight=5,unprefpenalty=2",
        #"pgida,hweight=5,unprefpenalty=5",
        #"relaxida,admissible=True",
        #"relaxida,admissible=True,hweight=5",
        #"relaxida,greedy_on_exact=True",
        #"relaxida,one_way=True",
        #"relaxida,one_way=True,greedy_on_exact=True",
        #"relaxida,hweight=1.2",
        #"relaxida,hweight=1.2,one_way=True,greedy_on_exact=True",
        ]
    return solvers

def _define_tasks():
    global TASKS
    TASKS = []

    solvers = get_measured_solvers()
    levels = []
    for i in range(1, 101):
        levels.append("data/sokoban/microban/level%03d.txt" % i)

    for level in levels:
        for solver in solvers:
            _add(level, solver)

    TASKS = tuple(TASKS)

