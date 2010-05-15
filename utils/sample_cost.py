#!/usr/bin/env python

import sokopath
from soko.env import env_lookup
from soko.solver import solver_lookup
from soko import formatting

from pylib import picklite

def _create_task(level_filename, solver_spec="astar"):
    env_wrapper = env_lookup.create_env(level_filename)
    return solver_lookup.create_task(env_wrapper, solver_spec)

def _sample_along(env, s, path):
    state_costs = {}
    total_cost = sum(a.get_cost() for a in path)
    for a in path:
        state_costs[s] = total_cost
        next_s = env.predict(s, a)
        total_cost -= a.get_cost()
        s = next_s

    state_costs[s] = 0
    return state_costs

INF_COST = None

class Collector(object):
    def __init__(self, env, solver):
        self.env = env
        self.solver = solver
        self.state_costs = {}

    def collect_costs(self, s, spread=0):
        """Collects the cost along the path to the goal.
        It could also spreads the collecting to the children
        of the path states.
        """
        if s  in self.state_costs:
            return

        path = self.solver.solve(self.env, s)
        if path is None:
            self.state_costs[s] = INF_COST
        else:
            path_costs = _sample_along(self.env, s, path)
            self.state_costs.update(path_costs)

            if spread > 0:
                self._spread_into_children(path_costs.keys(), spread - 1)

    def _spread_into_children(self, states, spread):
        for s in states:
            children = _get_children(self.env, s)
            for child in children:
                self.collect_costs(child, spread)


def _get_children(env, s):
    return [env.predict(s, a) for a in env.get_actions(s)]

def _save_values(store, property, state_values):
    for s, value in state_values.iteritems():
        store[_get_key(property, s)] = value

def _get_key(property, s):
    s_key = formatting.stringify(s)
    return "%s:\n%s" % (property, s_key)


def main():
    level_filename = "data/sokoban/sokoban2.txt"
    env, solver = _create_task(level_filename)
    s = env.init()
    collector = Collector(env, solver)
    collector.collect_costs(s, spread=3)

    state_costs = collector.state_costs
    print "collected states:", len(state_costs)

    store = picklite.open("../export/sample.plite")
    _save_values(store, "cost", state_costs)

    state_children = dict((s, _get_children(env, s)) for s in
            state_costs.iterkeys())
    _save_values(store, "children", state_children)

main()
