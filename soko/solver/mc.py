
import random
import math

from soko.solver.solver import Solver

class McSolver(Solver):
    """A Nested Monte-Carlo search.
    """
    def solve(self, env):
        """Returns a solution as a list of actions.
        """
        s = env.init()
        path = _sample(env, s)
        return path


def _sample(env, s):
    """Returns a random path to the goal or None.
    """
    memory = Memory()
    path = []
    cost = env.estim_cost(s)
    while cost > 0:
        a = _choose_action(env, s, memory)
        if a is None:
            return None

        path.append(a)
        memory.inc_num_visits(s)
        s = env.predict(s, a)
        cost = env.estim_cost(s)

    return path


class Memory(object):
    def __init__(self):
        self.visits = {}
    def get_num_visits(self, s):
        return self.visits.get(s, 0)
    def inc_num_visits(self, s):
        self.visits[s] = self.visits.get(s, 0) + 1


def _choose_action(env, s, memory):
    weights = []
    actions =  env.get_actions(s)
    for a in actions:
        next_s = env.predict(s, a)
        num_visits = memory.get_num_visits(next_s)
        weights.append(1.0/(num_visits + 1))

    if not weights:
        return None

    a_index = _softmax(weights)
    #TODO: return also None when num_visits > k.
    return actions[a_index]

def _softmax(weights):
    """Returns the index of the choosen choice.
    """
    temperature = 0.1
    items = [math.exp(w/temperature) for w in weights]
    selection = random.random() * sum(items)
    boundary = 0
    for i, item in enumerate(items):
        boundary += item
        if boundary >= selection:
            return i

    assert not "Wrong normalization"

