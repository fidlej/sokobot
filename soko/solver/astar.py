
import logging
import operator

from soko.solver.solver import Solver as BaseSolver
from soko.collections import PriorityQueue
from pylib import namedtuple

class Solver(BaseSolver):
    def solve(self, env, s=None):
        weight = self.config.hweight
        cost_fn = lambda g, h: g + h*weight

        if s is None:
            s = env.init()
        return find_path(env, s, cost_fn=cost_fn)


Node = namedtuple.namedtuple("Node", "f h g s prev_node a")

def _create_node(env, s, g, prev_node, a, cost_fn):
    """Returns a named tuple
    with a proper __cmp__.
    The node __cmp__ compares (f, h, g) values.
    A better node would have smaller (f, h, g) values.
    """
    h = env.estim_cost(s)
    f = cost_fn(g, h)
    return Node(f, h, g, s, prev_node, a)

def find_path(env, s, cost_fn):
    """Computes the shortest path from s by A*.
    Returns None where there is no way to the goal.

    See the theory:
    http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    """
    queue = PriorityQueue(operator.attrgetter("s"))
    closed = set()

    LOG_G_INCREMENT = 10
    log_g = LOG_G_INCREMENT
    num_visited = 0

    start_s = s
    cur = _create_node(env, s, 0, None, None, cost_fn)
    queue.schedule(cur)
    while not queue.is_empty():
        cur = queue.pop_smallest()
        s = cur.s
        closed.add(s)

        if cur.h == 0:
            break

        g = cur.g
        if g >= log_g:
            log_g += LOG_G_INCREMENT
            logging.debug("depth %s: %s", g, num_visited)

        actions = env.get_actions(s)
        for a in actions:
            next_s = env.predict(s, a)
            num_visited += 1
            if next_s in closed:
                # An consistent heuristic is assumed
                # so no reopening is needed.
                continue

            action_cost = a.get_cost()
            new = _create_node(env, next_s, g + action_cost, cur, a, cost_fn)
            queue.schedule(new)

    logging.debug("total %s: %s", cur.g, num_visited)
    if cur.h != 0:
        logging.info("no way to the goal from:\n%s", env.format(start_s))
        return None

    path = []
    while cur.prev_node is not None:
        path.append(cur.a)
        cur = cur.prev_node
    path.reverse()
    return path


