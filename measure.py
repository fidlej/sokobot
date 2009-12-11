#!/usr/bin/env python
"""Mesures multiple tasks specified in tasking.py.
"""

import logging

from soko.env import env_lookup
from soko.solver import solver_lookup
from soko import runtime
from soko.stats import tasking, resulting
from soko.stats.resulting import Result
from soko.visual.lengthvisualizer import calc_path_cost

def _measure(task, state_limit=None):
    """Computes the given task
    and return a Result or None when the task remains unsolved.
    """
    level_filename, spec = task
    counter = env_lookup.CallCounter(state_limit)
    env_wrapper = env_lookup.create_env(level_filename, counter)
    env, solver = solver_lookup.create_task(env_wrapper, spec)

    try:
        path = solver.solve(env)
        if path is None:
            raise ValueError("Task with no solution: %s" % (task,))
    except counter.LimitReachedError:
        return Result(False, 0, 0, counter.get_count())

    env_wrapper.stop_listeners()
    num_visited = counter.get_count()
    solution = _render_solution(env, path, counter)
    cost = calc_path_cost(path)
    resulting.store_solution(task, solution)
    return Result(True, len(path), cost, num_visited)

def _render_solution(env, path, call_counter):
    from soko.visual import StateVisualizer, LengthVisualizer
    output = ""
    for vis in [StateVisualizer(), LengthVisualizer(call_counter)]:
        output += vis.render(env, path)
    return output

def main():
    logging.basicConfig(level=logging.DEBUG)
    runtime.use_psyco()
    for task in tasking.get_tasks():
        print "task:", task
        result = _measure(task, state_limit=100000)
        print "result:", result
        resulting.store_result(task, result)

if __name__ == "__main__":
    main()
