
import logging

from pylib import namedtuple
from pylib.cache import memoize
from soko.env.env import Env, Action

class HyperEnv(Env):
    """An environment with high-level states.
    The found high-level path could be expanded into a concrete path,
    but the concrete path is not guaranteed to be optimal.
    """
    def __init__(self, env):
        """Wraps the given lower-level environment.
        """
        self.env = env
        #self.gator = CycleGator()
        self.gator = GroupGator()

    def configure(self, config):
        if hasattr(self.gator, "configure"):
            self.gator.configure(config)
        self.env.configure(config)

    def init(self):
        s = self.env.init()
        return self._get_hyper_s(s)

    def _get_hyper_s(self, s):
        connected_states = self.gator.get_connected(self.env, s)
        return frozenset(connected_states)

    def get_actions(self, hyper_s):
        """Returns a list of possible actions from the given state.
        """
        hyper_actions = []
        for next_s in self._get_periphery(hyper_s):
            if not self._is_covered(hyper_actions, next_s):
                hyper_actions.append(Action(self._get_hyper_s(next_s)))

        return hyper_actions

    def _get_periphery(self, hyper_s):
        """Returns states that are just outside the hyper_s.
        """
        periphery = []
        for s in hyper_s:
            for child in _get_children(self.env, s):
                if child not in hyper_s:
                    periphery.append(child)

        return periphery

    def _is_covered(self, hyper_actions, next_s):
        for hyper_a in hyper_actions:
            if next_s in hyper_a.get_cmd():
                return True

        return False

    def predict(self, hyper_s, hyper_a):
        return hyper_a.get_cmd()

    @memoize
    def estim_cost(self, hyper_s, cost_limit=None):
        return min(self.env.estim_cost(s) for s in hyper_s)

    def format(self, hyper_s):
        """Returns a single member of the given hyperstate.
        """
        s = min(hyper_s)
        return self.env.format(s)


class Gator(object):
    """Aggregates states.
    """
    def get_connected(self, env, s):
        """Returns states similar to and communicating with the given state.
        The returned set is a strongly connected subgraph of the state-space.
        """
        raise NotImplementedError

class GroupGator(object):
    """Does loosy grouping of the states.
    It does not check their bidirectional connectivity.
    """
    def __init__(self):
        self.state_group = {}
    def configure(self, config):
        self.config = config
    def get_connected(self, env, s):
        group = self.state_group.get(s)
        if group is not None:
            return group

        group = [s]
        self.state_group[s] = group

        perimeter = [s]
        for i in xrange(self.config.glimit):
            new_perimeter = self._collect_perimeter(env, perimeter, group)
            group += new_perimeter
            if len(new_perimeter) * self.config.greduce <= len(perimeter):
                # Reduced branching factor is a good time
                # to close the group.
                break
            perimeter = new_perimeter

        return group

    def _collect_perimeter(self, env, old_perimeter, group):
        new_perimeter = []
        for s in old_perimeter:
            for child in _get_children(env, s):
                if child not in self.state_group:
                    self.state_group[child] = group
                    new_perimeter.append(child)

        return new_perimeter


# A Node is sortable by its distance from the connected set.
Node = namedtuple.namedtuple("Node", "g s")

class CycleGator(object):
    def __init__(self, k=2):
        """Creates a new aggregator with max perimeter <= k.
        """
        assert k >= 2
        self.k = k

    def get_connected(self, env, s):
        """Returns all states that are able
        to visit another state with k steps.
        """
        self.env = env
        self.parent_memory = ParentMemory()
        self.connected = set()

        opened = {}
        self._connect_state(s, opened)

        while len(opened):
            cur = self._pop_nearest(opened)
            if cur.s in self.connected:
                continue
            elif cur.g < self.k:
                self._open_child_nodes(cur, opened)

        return self.connected

    def _connect_parents(self, s, opened):
        """Adds parents of the given state into
        the set of connected states.
        """
        parents = self.parent_memory.get_parents(s)
        for parent in parents:
            if parent not in self.connected:
                self._connect_state(parent, opened)

    def _connect_state(self, s, opened):
        #logging.debug("Connecting: %s", s)
        self.connected.add(s)
        self._reopen_children(s, opened)
        self._connect_parents(s, opened)

    def _pop_nearest(self, opened):
        min_node = min(opened.itervalues())
        del opened[min_node.s]
        return min_node

    def _reopen_children(self, s, opened):
        """Reopens all childrens of the given connected state.
        """
        for child in _get_children(self.env, s):
            self._open_child(0, child, opened)

    def _open_child_nodes(self, node, opened):
        """Opens all childrens of the given node.
        """
        children = _get_children(self.env, node.s)
        for child in children:
            if child in self.connected:
                self._connect_state(node.s, opened)
                return

        for child in children:
            self.parent_memory.remember_parent(node.s, child)
            self._open_child(node.g, child, opened)

    def _open_child(self, parent_g, child, opened):
        """Opens the given child.
        When the child is already opened, its g distance is updated properly.
        """
        child_g = parent_g + 1
        existing = opened.get(child)
        if existing is None or existing.g > child_g:
            opened[child] = Node(child_g, child)

class ParentMemory(object):
    def __init__(self):
        # a map from a child to its set of parents
        self.child_parents_map = {}

    def get_parents(self, s):
        """Returns all seen parents of the given state.
        """
        # A copy is returned,
        # so it will be safe to iterate over it.
        return tuple(self.child_parents_map.get(s, []))

    def remember_parent(self, parent, child):
        """Remembers the given parent.
        """
        if child not in self.child_parents_map:
            self.child_parents_map[child] = set()
        self.child_parents_map[child].add(parent)


#@memoize
def _get_children(env, s):
    """Returns children states of the given state.
    """
    return [env.predict(s, a) for a in env.get_actions(s)]

