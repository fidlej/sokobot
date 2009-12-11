
import logging

from soko import runtime, INF_COST
from soko.solver.solver import Solver

class RbfsSolver(Solver):
    """A recursive best-first search solver.
    """
    def __init__(self, search=None):
        self.search = search or _rbfs

    def solve(self, env):
        """Returns a solution as a list of actions.
        """
        runtime.ensure_high_recursionlimit()

        s = env.init()
        info = _PathInfo(env, self.config)
        edge = info.create_edge(s, 0)
        f = self.search(info, edge, INF_COST)
        return info.get_path()

def IdaSolver():
    return RbfsSolver(_ida)

class _PathInfo(object):
    def __init__(self, env, config):
        self.env = env
        self.config = config
        weight = config.hweight
        self.cost_fn = lambda g, h: g + h*weight
        self.reversed_path = None
        self.h_cache = {}

        self.num_visited = 0
        self.depth_to_log = 0

    def create_edge(self, s, g, a=None):
        self.num_visited += 1
        h = self._estim_cost(s)
        f = self.cost_fn(g, h)
        return Edge(s, f, g, h==0, a)

    def _estim_cost(self, s):
        h = self.h_cache.get(s)
        if h is not None:
            return h

        h = self.env.estim_cost(s)
        self.h_cache[s] = h
        return h

    def remember_h(self, s, h):
        self.h_cache[s] = h

    def get_path(self):
        if self.reversed_path is None:
            return None
        return list(reversed(self.reversed_path))

    def log_backtracking(self, edge, max_path_len):
        if self.depth_to_log < max_path_len:
            self.depth_to_log = (max_path_len + 10) // 10 * 10
            logging.debug("backtracking %s > %s: %s",
                    edge.f, max_path_len, self.num_visited)

class Edge(object):
    """An object with modifiable f.
    It holds info about a successor.
    """
    def __init__(self, s, f, g, is_goal=False, a=None):
        self.s = s
        self.f = f
        self.g = g
        self.is_goal = is_goal
        self.a = a

    def key(self):
        return self.f

def _rbfs(info, parent, max_path_len):
    """Does recursive best first search.
    It returns a more accurate f value for the node.
    """
    if parent.is_goal:
        info.reversed_path = []
        return parent.f

    edges = _get_edges(info, parent)
    if len(edges) == 0:
        return INF_COST

    while True:
        edges.sort(key=Edge.key)
        edge = edges[0]
        if edge.f > max_path_len:
            info.log_backtracking(edge, max_path_len)
            return edge.f

        alternative_path_len = max_path_len
        if len(edges) > 1:
            alternative_path_len = min(max_path_len, edges[1].f)

        edge.f = _rbfs(info, edge, alternative_path_len)
        if info.reversed_path is not None:
            info.reversed_path.append(edge.a)
            return edge.f

        child_h = (edge.f - edge.g) // info.config.hweight
        info.remember_h(edge.s, child_h)

def _get_edges(info, parent):
    #TODO: Should be parent_f used to prevent cycling?
    # But how will that behave with overestimated h?
    # It forces the path to have the parent.f length.

    env = info.env
    edges = []
    for a in env.get_actions(parent.s):
        next_s = env.predict(parent.s, a)
        next_g = parent.g + a.get_cost()
        edge = info.create_edge(next_s, next_g, a)
        #edge.f = max(parent.f, edge.f)
        edges.append(edge)

    return edges


def _ida(info, node, max_path_len=INF_COST):
    """A plain IDA* search without caching.
    """
    max_cost = node.f
    while max_cost <= max_path_len:
        logging.debug("max_cost: %s", max_cost)
        max_cost = _ida_search(info, node, max_cost)
        if info.reversed_path is not None:
            return info.reversed_path

    return None

def _ida_search(info, parent, max_cost):
    if parent.is_goal:
        info.reversed_path = []
        return parent.f

    min_f = INF_COST
    for edge in _get_edges(info, parent):
        if edge.f > max_cost:
            min_f = min(min_f, edge.f)
            continue

        child_f = _ida_search(info, edge, max_cost)
        if info.reversed_path is not None:
            info.reversed_path.append(edge.a)
            return child_f

        min_f = min(min_f, child_f)

    assert min_f > max_cost
    return min_f

