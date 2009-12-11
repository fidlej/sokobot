#!/usr/bin/env python
"""Checks that the relaxida h is not overestimating
in a task.
"""

import logging
import sys
import operator

import sokopath
from soko import mazing
from soko.env import env_lookup
from soko.env.relaxedenv import RelaxedEnv
from soko.solver import solver_lookup, ida
from soko.visual.lengthvisualizer import calc_path_cost

LEVEL_FILENAME = "data/sokoban/microban/level018.txt"
CONFIG = solver_lookup.Config(**solver_lookup.DEFAULT_CONFIG)

def _calc_h_cache(env, config):
    env.configure(config)
    env = RelaxedEnv(env)
    s = env.init()

    h_cache = env.h_cache
    search = ida.IdaSearch()
    search.configure(config)
    path = search.ida(env, s, h_cache=h_cache)
    assert path is not None
    return h_cache

def _verify_h(env, s, h):
    """Verifies that the h is not overestimated.
    """
    logging.info("Checking %s h: %s", s, h)
    env, solver = solver_lookup.create_task(env, "astar")
    path = solver.solve(env, s)
    if path is None:
        cost = ida.INF_COST
    else:
        cost = calc_path_cost(path)

    if cost < ida.INF_COST and h > cost:
        print "Overestimated h for %s: %s > %s" % (s, h, cost)
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.WARN)
    env = env_lookup.create_env(LEVEL_FILENAME)
    h_cache = _calc_h_cache(env, CONFIG)
    cache = h_cache.cache

    states = cache.keys()
    def key(s):
        return (len(s[1]), s)
    states.sort(key=key)

    for s in states:
        h = cache[s]
        _verify_h(env, s, h)

if __name__ == "__main__":
    main()

