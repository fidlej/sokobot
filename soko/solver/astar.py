
import logging
import operator

from soko.solver.solver import Solver as BaseSolver
from soko.collections import PriorityQueue
from pylib import namedtuple

class Solver(BaseSolver):
    def configure(self, config):
        self.config = config

        weight = self.config.hweight
        cost_fn = lambda g, h: g + h*weight

        tools = _ExpandTools(cost_fn)
        if self.config.rollout:
            self.expander = _RolloutExpander(tools)
        else:
            self.expander = _ChildExpander(tools)

    def solve(self, env, s=None):
        if s is None:
            s = env.init()

        self.expander.tools.set_env(env)
        return _find_path(env, s, self.expander)


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

def _find_path(env, s, expander):
    """Computes the shortest path from s by A*.
    Returns None where there is no way to the goal.

    See the theory:
    http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    """
    queue = PriorityQueue(operator.attrgetter("s"))
    closed = set()
    expander.tools.set_memory(queue, closed)

    LOG_G_INCREMENT = 10
    log_g = LOG_G_INCREMENT
    num_visited = 0

    start_s = s
    cur = expander.tools.create_start_node(s)
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

        num_visited += expander.expand_node(env, cur)

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


class _ExpandTools:
    def __init__(self, cost_fn):
        self.cost_fn = cost_fn

    def set_env(self, env):
        self.env = env

    def set_memory(self, queue, closed):
        self.queue = queue
        self.closed = closed

    def create_start_node(self, s):
        return _create_node(self.env, s, 0, None, None, self.cost_fn)

    def create_node(self, s, prev_node, a):
        g = prev_node.g + a.get_cost()
        return _create_node(self.env, s, g, prev_node, a, self.cost_fn)

    def queue_chilren(self, node, actions):
        s = node.s
        for a in actions:
            next_s = self.env.predict(s, a)
            if next_s in self.closed:
                # A consistent heuristic is assumed
                # so no reopening is needed.
                continue

            new = self.create_node(next_s, node, a)
            self.queue.schedule(new)


class _ChildExpander:
    def __init__(self, tools):
        self.tools = tools

    def expand_node(self, env, node):
        """Puts node children to the queue.
        """
        actions = env.get_actions(node.s)
        self.tools.queue_chilren(node, actions)
        num_visited = len(actions)
        return num_visited


class _RolloutExpander:
    def __init__(self, tools):
        self.tools = tools
        #self.policy = _RandomPolicy()
        from soko.perception.solver import PerceptPolicy
        self.policy = PerceptPolicy()

    def expand_node(self, env, node):
        """Puts more than just node children to the queue.
        """
        num_visited = 0
        self.policy.init_history(env, node)
        while True:
            self.tools.closed.add(node.s)
            actions = env.get_actions(node.s)
            a = self.policy.next_action(actions)
            if a is None:
                break

            next_s = env.predict(node.s, a)
            num_visited += 1
            if next_s in self.tools.closed:
                break

            # The queue is checked before adding children to it.
            if next_s in self.tools.queue.opened:
                break

            other_actions = [other for other in actions if a.cmd != other.cmd]
            self.tools.queue_chilren(node, other_actions)
            num_visited += len(other_actions)

            self.policy.add_history(env, next_s)
            node = self.tools.create_node(next_s, node, a)

        self.tools.queue_chilren(node, actions)
        return num_visited + len(actions)


class _RandomPolicy:
    def next_action(self, actions):
        import random
        return random.choice(actions)

    def init_history(self, env, node):
        pass

    def add_history(self, env, s):
        pass

