
import logging
import random

from soko import runtime, INF_COST
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
    path = []
    cost = env.estim_cost(s)
    while cost > 0:
        a = random.choice(env.get_actions(s))
        path.append(a)
        s = env.predict(s, a)
        cost = env.estim_cost(s)

    return path

