#!/usr/bin/env python

import sokopath
from soko.env import env_lookup
from soko.solver import solver_lookup

def _create_task(level_filename, solver_spec="astar"):
    env_wrapper = env_lookup.create_env(level_filename)
    return solver_lookup.create_task(env_wrapper, solver_spec)

def _sample_along(env, s, path):
    state_costs = []
    total_cost = sum(a.get_cost() for a in path)
    for a in path:
        state_costs.append((s, total_cost))
        next_s = env.predict(s, a)
        total_cost -= a.get_cost()
        s = next_s

    state_costs.append((s, 0))
    return state_costs

def main():
    level_filename = "data/sokoban/sokoban2.txt"
    env, solver = _create_task(level_filename)
    s = env.init()
    path = solver.solve(env, s)
    state_costs = _sample_along(env, s, path)
    for s, cost in state_costs:
        print cost


main()
