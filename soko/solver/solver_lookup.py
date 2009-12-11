
from soko.solver import astar, ida, steering, rbfs
from pylib.namedtuple import namedtuple

from soko.env.macroenv import MacroEnv
from soko.env.hyperenv import HyperEnv
from soko.env.relaxedenv import RelaxedEnv
from soko.env.estimenv import EstimPgEnv

"""
Solver name format:
name,option1=value,option2=value

Options:
estim_limit - relaxed envs get inherits the path_limit from
              the current IDA iteration.
exact_h - h is recomputed when it isn't exact. It applies to relax envs.
one_way - use just one way to a state, even if it isn't the optimal one.
          This could overestimate some paths. It applies to IDA.
greedy_on_exact - behaves greedy when stumbling upon an exact h.
                  The search is then ended without care about the g.
                  It applies to IDA.
admissible - allows to assume an admissible heuristic.
hweight - the weight of h in a weighted A*. It overestimates at most weight-times.
unprefpenalty - an extra penalty to h
                if an unpreferred action has to be followed.
"""
DEFAULT_CONFIG = dict(
        estim_limit=False,
        exact_h=True,
        one_way=False,
        greedy_on_exact=False,
        admissible=True,
        hweight=1,
        unprefpenalty=0,
        glimit=3,
        greduce=1,
        )

Config = namedtuple("Config", " ".join(DEFAULT_CONFIG.keys()))

SOLVERS = dict(
        ida=ida.Solver,
        astar=astar.Solver,
        steer=steering.SteeringSolver,
        rbfs=rbfs.RbfsSolver,
        rida=rbfs.IdaSolver,
        )

PREFIXES = (
        ("macro", MacroEnv),
        ("hyper", HyperEnv),
        ("relaxed", RelaxedEnv),
        ("relax", RelaxedEnv),
        ("pg", EstimPgEnv),
        )

def create_task(env, solver_spec):
    """Returns (wrapped_env, solver) for the given spec.
    """
    name, vars = _split_name_vars(solver_spec)
    name, env_wrappers = _extract_prefixes(name)

    solver = SOLVERS[name]()
    config = _parse_vars(vars)
    solver.configure(config)
    env.configure(config)
    for wrapper in reversed(env_wrappers):
        env = wrapper(env)
        env.configure(config)

    return env, solver

def _split_name_vars(solver_spec):
    """Splits the solver spec on (name, vars).
    """
    parts = solver_spec.split(",", 1)
    if len(parts) == 1:
        name = parts[0]
        vars = ""
    else:
        name, vars = parts
    return name, vars

def _extract_prefixes(name):
    env_wrappers = []
    was_change = True
    while was_change:
        was_change = False
        for prefix, env_wrapper in PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix):]
                env_wrappers.append(env_wrapper)
                was_change = True
                break

    return name, env_wrappers

def _parse_vars(vars):
    var_dict = eval("dict(" + vars + ")", globals())
    default = dict(DEFAULT_CONFIG)
    default.update(var_dict)
    return Config(**default)

