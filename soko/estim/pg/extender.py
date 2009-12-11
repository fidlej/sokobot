
from pylib.namedtuple import namedtuple
from pylib import v2, cache

Action = namedtuple("Action", "pre effect")

class Extender(object):
    def reset(self, start_s):
        """Resets itself for a new reachability analysis.
        It returns the effects of the start state
        as a list of (value, variable) pairs.
        """
        raise NotImplementedError

    def get_new_actions(self, reachable, new_values):
        """Returns actions that become newly possible.
        """
        raise NotImplementedError

    def get_reached_goal(self, start_s, reachable):
        """Returns the reached goal or None.
        """
        raise NotImplementedError


class GroundAction(object):
    """An immutable ground action.
    """
    def __init__(self, action, tile):
        self.action = action
        self.tile = tile
        self.pres = None
        self.effects = None

    def get_pres(self):
        if self.pres is None:
            self.pres = self._get_ground_conds(self.action.pre)
        return self.pres

    def get_effects(self):
        if self.effects is None:
            self.effects = self._get_ground_conds(self.action.effect)
        return self.effects

    def _get_ground_conds(self, conds):
        ground = []
        for val, shift in conds:
            pos = v2.sum(self.tile, shift)
            ground.append((val, pos))
        return ground

    def __str__(self):
        return str((self.get_pres(), self.get_effects()))


class ActionTrigger(object):
    def __init__(self, grinder):
        # A map of precondition -> unmet_actions
        self.waiting = {}
        # A map of action -> num_met_preconditions
        self.num_mets = {}
        self.grinder = grinder

    def reset(self):
        """Resets itself for a new reachability analysis.
        """
        self.num_mets = {}

    def get_new_actions(self, new_values):
        """Returns the newly possible ground actions.
        """
        met_actions = []
        for gain in new_values:
            self._setup_waitlist(gain)
            met = self._collect_waiting(gain)
            met_actions += met

        return met_actions

    def _setup_waitlist(self, gain):
        """Setups the list of actions that
        have the given gain as a precondition.
        """
        if gain in self.waiting:
            return

        waiting_actions = self.grinder.get_ground_actions(gain)
        self.waiting[gain] = waiting_actions

    def _collect_waiting(self, gain):
        """Returns the ground actions that got
        all its preconditions met.
        """
        available_actions = []
        gain_waiting = self.waiting[gain]
        for action in gain_waiting:
            num_met = self.num_mets.get(action, 0)
            num_met += 1
            if num_met == len(action.get_pres()):
                available_actions.append(action)
            else:
                self.num_mets[action] = num_met

        return available_actions


class ShiftGrinder(object):
    def __init__(self, vars, schematic_actions):
        self.vars = frozenset(vars)
        # A map of pre_value -> a list of (schem_action, pre_shift) pairs
        self.accepting = {}
        for a in schematic_actions:
            for value, shift in a.pre:
                self.accepting.setdefault(value, []).append((a, shift))

    def get_ground_actions(self, gain):
        """Returns all ground actions that
        have the gain as a precondition.
        """
        actions = []
        new_value, pos = gain
        value_accepting = self.accepting[new_value]
        for schem_action, shift in value_accepting:
            base_tile = v2.diff(pos, shift)
            a = self._get_action_instance(schem_action, base_tile)
            if self._is_valid(a):
                actions.append(a)
        return actions

    def _is_valid(self, action):
        for value, pos in action.get_pres():
            if pos not in self.vars:
                return False
        return True

    @cache.selfmem
    def _get_action_instance(self, schem_action, base_tile):
        """Returns the existing or a new GroundAction.
        The ground actions are never recreated,
        so it is possible compare them by their memory.
        """
        return GroundAction(schem_action, base_tile)

