
from soko.solver.solver import Solver

class SteeringSolver(Solver):
    def solve(self, env):
        """Returns a solution as a list of actions.
        """
        s = env.init()
        search = DepthSearch(env)
        return search.search(s)

class DepthSearch(object):
    def __init__(self, env):
        self.env = env
        self.cmp = MultiComparator(
                CyclePreventingComparator(),
                HComparator(env))

    def search(self, s):
        reversed_path = self._search(s)
        if reversed_path is None:
            return None

        reversed_path.reverse()
        return reversed_path

    def _search(self, s):
        """Returns a reversed path from the given state to the goal
        or None.
        """
        if self.env.estim_cost(s) == 0:
            return []

        self.cmp.note_visited(s)
        for a in self.env.get_actions(s):
            next_s = self.env.predict(s, a)
            if self.cmp.is_better(next_s, s):
                reversed_path = self._search(next_s)
                if reversed_path is not None:
                    reversed_path.append(a)
                    return reversed_path

        return None

class MultiComparator(object):
    def __init__(self, *cmps):
        self.cmps = cmps

    def is_better(self, child, parent):
        for cmp in self.cmps:
            if not cmp.is_better(child, parent):
                return False
        return True

    def note_visited(self, s):
        for cmp in self.cmps:
            cmp.note_visited(s)


class HComparator(object):
    def __init__(self, env):
        self.env = env

    def is_better(self, child, parent):
        #TODO: use just < when the h is informative enough
        return self.env.estim_cost(child) <= self.env.estim_cost(parent)

    def note_visited(self, s):
        pass


class CyclePreventingComparator(object):
    def __init__(self):
        self.visited = set()

    def is_better(self, child, parent):
        return child not in self.visited

    def note_visited(self, s):
        self.visited.add(s)

