
import random
import math

from soko.solver.solver import Solver
from soko.visual.lengthvisualizer import calc_path_cost

MAX_NUM_VISITS = 10

class McSolver(Solver):
    """A Nested Monte-Carlo search.
    """
    def solve(self, env):
        """Returns a solution as a list of actions.
        """
        s = env.init()
        info = _SearchInfo(env)
        level = 1
        path = _nested(info, s, level)
        #path = _sample(info, s)
        return path


class _SearchInfo(object):
    def __init__(self, env):
        self.env = env
        self.costs = {}

    def calc_best_cost(self, s, path):
        """Returns and stores the best known cost for the given state.
        It could return None when there seems to be no solution.
        """
        known_cost = self.costs.get(s)
        if path is None:
            return known_cost

        cost = calc_path_cost(path)
        if known_cost is None or cost < known_cost:
            known_cost = self.costs[s] = cost
        return known_cost

class _Memory(object):
    def __init__(self):
        self.visits = {}
    def get_num_visits(self, s):
        return self.visits.get(s, 0)
    def inc_num_visits(self, s):
        self.visits[s] = self.visits.get(s, 0) + 1


def _nested(info, s, level):
    env = info.env
    path = []
    while not _is_goal(env, s):
        a = _choose_best_action(info, s, level)
        if a is None:
            return None

        path.append(a)
        s = env.predict(s, a)

    return path

def _choose_best_action(info, s, level):
    """Returns the best known action in the given state.
    It returns None if the problem seems unsolvable.
    """
    env = info.env
    min_cost = None
    best_action = None
    for a in env.get_actions(s):
        next_s = env.predict(s, a)
        if level == 1:
            path = _sample(info, next_s)
        else:
            path = _nested(info, next_s, level - 1)

        cost = info.calc_best_cost(next_s, path)
        if cost is None:
            continue

        if min_cost is None or cost < min_cost:
            min_cost = cost
            best_action = a

    #print "best action:", s, best_action, min_cost
    return best_action

def _is_goal(env, s):
    return env.estim_cost(s) == 0

def _sample(info, s):
    """Returns a random path to the goal or None.
    """
    start_s = s
    memory = _Memory()
    env = info.env
    path = []
    while not _is_goal(env, s):
        a = _choose_random_action(env, s, memory)
        if a is None:
            return None
        if memory.get_num_visits(s) > MAX_NUM_VISITS:
            return None

        path.append(a)
        memory.inc_num_visits(s)
        s = env.predict(s, a)
        if s == start_s:
            path = []

    return path


def _choose_random_action(env, s, memory):
    """Chooses a random action.
    It gives more probability to less visited next states.
    """
    weights = []
    actions =  env.get_actions(s)
    for a in actions:
        next_s = env.predict(s, a)
        num_visits = memory.get_num_visits(next_s)
        weights.append(1.0/(num_visits + 1))

    if not weights:
        return None

    a_index = _softmax(weights)
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

