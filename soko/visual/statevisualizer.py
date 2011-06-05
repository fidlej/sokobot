
from soko.visual.lengthvisualizer import calc_costs

class StateVisualizer(object):
    def render(self, env, path):
        costs = calc_costs(path)
        real_cost = sum(costs)

        output = ""
        s = env.init()
        for i, a in enumerate(path):
            next_s = env.predict(s, a)
            output += self._format(env, s, real_cost)
            real_cost -= costs[i]
            s = next_s

        output += self._format(env, s, real_cost)
        return output

    def _format(self, env, s, real_cost):
        state = env.format(s)
        h = env.estim_cost(s)
        h_diff = h - real_cost
        return "%s h(s)=%s (%s)\n\n" % (state, h, h_diff)
