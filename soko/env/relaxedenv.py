
import logging

from soko import INF_COST, runtime
from soko.solver import ida

# It does not inherit from the Env,
# because it wraps an env.
# It must not overshadow its methods.
class RelaxedEnv(object):
    """An environment that estimates the cost
    based on distance to the goal from relaxed states.
    It is good when the relaxed paths have informative action costs.
    """
    def __init__(self, env):
        self.env = env
        self.h_cache = ida.HCache()
        self.nesting = 0

    def __getattr__(self, name):
        return getattr(self.env, name)

    def estim_cost(self, s, cost_limit=INF_COST):
        total_cost = 0
        relaxed_states = self.env.relax(s)
        if len(relaxed_states) == 0:
            return self.env.estim_cost(s, cost_limit)

        for relaxed_s in relaxed_states:
            total_cost += self._estim_relaxed(relaxed_s,
                    cost_limit - total_cost)

        # A goal has to be confirmed in its unrelaxed version.
        if total_cost == 0 and self.nesting == 0:
            return self.env.estim_cost(s, cost_limit)

        return total_cost

    def _estim_relaxed(self, s, cost_limit):
        h = self.h_cache.get(s)
        if h is not None:
            # Using a possibly smaller estimate,
            # but it saves the computation.
            if not self.config.exact_h:
                return h

            if h >= cost_limit:
                return h
            if self.h_cache.is_exact(s):
                return h

        self._update_h_cache(s, self.h_cache, cost_limit)
        return self.h_cache[s]

    @runtime.suppress_logging
    def _update_h_cache(self, s, h_cache, cost_limit):
        search = ida.IdaSearch()
        search.configure(self.config)
        self.nesting += 1
        try:
            path = search.ida(self, s, h_cache=h_cache, cost_limit=cost_limit)
        finally:
            self.nesting -= 1

