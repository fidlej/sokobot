
import logging
from soko import runtime, INF_COST
from soko.solver.solver import Solver as BaseSolver

class Solver(BaseSolver):
    def solve(self, env):
        """Returns a solution as a list of actions.
        """
        s = env.init()
        logging.info("initial state: %s", s)
        search = IdaSearch()
        search.configure(self.config)
        return search.ida(env, s)

class HCache(object):
    def __init__(self):
        self.cache = {}
        self.exact = set()

    def mark_exact(self, s, h):
        self.cache[s] = h
        self.exact.add(s)

    def is_exact(self, s):
        return s in self.exact

    def get(self, *args):
        return self.cache.get(*args)

    def __getitem__(self, s):
        return self.cache[s]

    def __setitem__(self, s, h):
        self.cache[s] = h

class PathInfo(object):
    def __init__(self, env, h_cache):
        self.env = env
        self.reversed_path = None
        self.h_cache = h_cache
        self.g_cache = {}
        self.num_visited = 0
        self.unpref_h_cache = {}

    def configure(self, config):
        self.config = config
        weight = config.hweight
        self.cost_fn = lambda g, h: g + h*weight

    def estim_cost(self, s, cost_limit):
        if not self.config.estim_limit:
            cost_limit = INF_COST

        h = self.h_cache.get(s)
        if h is not None:
            return h

        return self.env.estim_cost(s, cost_limit)

    def remember_h(self, s, h):
        self.h_cache[s] = h

    def remember_as_unsolvable(self):
        for s in self.g_cache.iterkeys():
            self.h_cache[s] = INF_COST


class IdaSearch(object):
    def configure(self, config):
        self.config = config

    def ida(self, env, s, h_cache=None, cost_limit=INF_COST):
        if h_cache is None:
            h_cache = HCache()
        info = PathInfo(env, h_cache)
        info.configure(self.config)
        path = _ida(info, s, cost_limit)
        return path


def _ida(info, s, cost_limit=INF_COST):
    """Does an iterative deepening search.
    """
    estim_h = info.estim_cost(s, cost_limit)
    info.remember_h(s, estim_h)

    runtime.ensure_high_recursionlimit()
    last_visited = 0
    limit = estim_h + 1
    while limit <= cost_limit:
        info.visited = {}
        h = cached_depth_search(info, s, 0, limit)

        logging.debug("limit %s: %s", limit, info.num_visited - last_visited)
        last_visited = info.num_visited

        if info.reversed_path is not None:
            logging.debug("total: %s", info.num_visited)
            return list(reversed(info.reversed_path))
        elif h >= cost_limit:
            if h >= INF_COST:
                info.remember_as_unsolvable()
            return None

        limit = info.cost_fn(0, h) + 1

    return None

#@runtime.count_recursion
def cached_depth_search(info, s, g, path_limit):
    # The g_cache reduces the number of visited states
    # in the following IDA iterations.
    # It also prevents endless deepening in an env with no solution.
    prev_g = info.g_cache.get(s)
    if prev_g is None or g < prev_g:
        info.g_cache[s] = g
    elif prev_g < g:
        return INF_COST

    # The memory of visited states in an iteration
    # prevents the cycling even when an action_cost is zero.
    if info.visited.get(s, INF_COST) <= g:
        return INF_COST
    info.visited[s] = g

    return _h_cached_depth_search(info, s, g, path_limit)

def _h_cached_depth_search(info, s, g, path_limit):
    if info.h_cache.is_exact(s) and (
            info.cost_fn(g, info.h_cache[s]) < path_limit
            or info.config.greedy_on_exact):
        # Assumes that nobody will need the full path.
        info.reversed_path = []
        return info.h_cache[s]

    h = _estim_h(info, s, g, path_limit)
    info.remember_h(s, max(h, _calc_limit_h(info, g, path_limit)))
    h = _depth_search(info, s, g, h, path_limit)
    if info.config.one_way:
        if h < INF_COST:
            info.remember_h(s, h)
        else:
            info.g_cache[s] = -1

    # The returned h is not remembered.
    # It could be overestimated by the cycle prevention.
    # The remembered h value must not depend on g.
    return h


def _depth_search(info, s, g, h, path_limit):
    """Does a depth search until g + h < path_limit.
    """
    if h == 0:
        info.reversed_path = []
        info.h_cache.mark_exact(s, 0)
        return 0

    if info.cost_fn(g, h) >= path_limit:
        return h

    min_h = INF_COST
    env = info.env
    unpref_h = _calc_unpref_h(info, s, g, h)
    actions = _order_actions(env.get_actions(s))
    for a in actions:
        if not a.is_preferred() and info.cost_fn(g, unpref_h) >= path_limit:
            min_h = min(min_h, unpref_h)
            break

        next_s = env.predict(s, a)
        action_cost = a.get_cost()
        info.num_visited += 1
        next_g = g + action_cost
        child_h = cached_depth_search(info, next_s, next_g, path_limit)

        if info.reversed_path is not None:
            h = child_h + action_cost
            info.reversed_path.append(a)
            info.h_cache.mark_exact(s, h)
            return h

        min_h = min(min_h, child_h + action_cost)

    return min_h

def _order_actions(actions):
    """Reorders the actions to try the prefered ones first.
    """
    return ([a for a in actions if a.is_preferred()]
            + [a for a in actions if not a.is_preferred()])

def _calc_unpref_h(info, s, g, h):
    """Estimates h of this state
    if an unpreferred child has to be followed.

    The unpref_h(s) should depend just on the original h(s).
    It should not be extended by the h back-propagation.
    """
    if info.config.unprefpenalty == 0:
        return h

    unpref_h = info.unpref_h_cache.get(s)
    if unpref_h is not None:
        return max(h, unpref_h)

    unpref_h = h + info.config.unprefpenalty
    info.unpref_h_cache[s] = unpref_h
    return unpref_h

def _estim_h(info, s, g, path_limit):
    h = info.estim_cost(s, path_limit - g)
    h = _get_parent_consistency(info, g, h, path_limit)
    return h

def _get_parent_consistency(info, g, h, path_limit):
    """Returns h that is incremented when parent_h
    is better informed than h for this node.
    Holte calls this heuristic P-g.
    It is helpful when the h(s) is admissible.
    """
    if not info.config.admissible:
        return h

    bound = _calc_limit_h(info, g, path_limit) - 1
    # The h != 0 check is needed when
    # using an overestimating heuristics.
    if bound > h and h != 0:
        h = bound

    return h

def _calc_limit_h(info, g, path_limit):
    """Returns h that would be outside the path_limit.
    """
    return (path_limit - g)//info.config.hweight

