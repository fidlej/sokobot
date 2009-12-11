
import logging
import operator
from pylib.namedtuple import namedtuple

from soko.env.env import Env, Action
from soko.collections import PriorityQueue

class MacroEnv(object):
    """An environment that provides macro actions
    instead of the low-level actions.
    """
    def __init__(self, env):
        self.env = env
        self.partition = RadiusPartition(env)

    def get_actions(self, s):
        """Returns a list of macro actions from given state.
        """
        # The macro_action.cmd stores the end state of the macro.
        macros = []
        for cost, end_s in self.partition.get_macro_edges(s):
            macros.append(Action(end_s, cost))

        return macros

    def predict(self, s, macro_a):
        return macro_a.get_cmd()

    def __getattr__(self, name):
        return getattr(self.env, name)


# The edges are sortable by cost needed to reach s.
Edge = namedtuple("Edge", "cost s")

class RadiusPartition(object):
    """Limits the macro reach by a radius of a cube.
    States outside the radius are reported as the end states.
    """
    def __init__(self, env):
        self.env = env
        self.radius = 2

    def get_macro_edges(self, s):
        """Returns edges to the reachable states outside
        the current cluster.
        """
        start_coords = self._get_coords(s)

        seen = set([s])
        macro_edges = []
        queue = PriorityQueue(operator.attrgetter("s"))
        queue.schedule(Edge(0, s))
        while not queue.is_empty():
            edge = queue.pop_smallest()
            for child_cost, child in _get_edges(self.env, edge.s):
                if child in seen:
                    continue

                seen.add(child)
                child_edge = Edge(edge.cost + child_cost, child)
                if self._is_inside_cluster(child, start_coords):
                    queue.schedule(child_edge)
                else:
                    macro_edges.append(child_edge)

        #logging.debug('num end states: %s, seen: %s', len(macro_edges), len(seen))
        return macro_edges

    def _get_coords(self, s):
        """Returns the state coordinates.
        """
        #TODO: support not just PusherEnv
        pos, boxes = s
        coordinates = []
        for x, y in (pos,) + boxes:
            coordinates.append(x)
            coordinates.append(y)
        return coordinates

    def _is_inside_cluster(self, s, start_coords):
        coords = self._get_coords(s)
        return self._calc_distance(start_coords, coords) <= self.radius

    def _calc_distance(self, a_coords, b_coords):
        """Returns the distance between the coordinates.
        The distance is calculated by max(dx, dy, dz, ...)
        to get a rectangular local view.
        """
        return max(abs(bx - ax) for ax, bx in zip(a_coords, b_coords))


def _get_edges(env, s):
    return [Edge(a.get_cost(), env.predict(s, a)) for a in env.get_actions(s)]

