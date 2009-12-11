
from pylib import v2

from soko.estim.pg.extender import Extender, ShiftGrinder, Action
from soko.estim.pg.extender import ActionTrigger

def cond_in(val, shift=(0,0)):
    """A condition that the value is available in tile + shift.
    """
    return (val, shift)

def _get_pusher_actions(num_boxes):
    actions = []
    for shift in ((0,-1), (0,1), (-1,0), (1,0)):
        actions.append(Action(
            (cond_in('x'), cond_in('.', shift)),
            (cond_in('.'), cond_in('x', shift))))

        next_next = v2.scale(shift, 2)
        for bval in _get_boxvals(num_boxes):
            actions.append(Action(
                (cond_in('x'), cond_in(bval, shift), cond_in('.', next_next)),
                (cond_in('.'), cond_in('x', shift), cond_in(bval, next_next))))

    return actions


class PusherExtender(Extender):
    def __init__(self, env):
        self.env = env
        self.non_walls = env.get_non_walls()
        s = env.init()
        pos, boxes = s
        vars = [var for value, var in self._toeffects(s)]
        grinder = ShiftGrinder(vars, _get_pusher_actions(len(boxes)))
        self.trigger = ActionTrigger(grinder)

    def reset(self, start_s):
        self.trigger.reset()
        return self._toeffects(start_s)

    def get_new_actions(self, reachable, new_values):
        return self.trigger.get_new_actions(new_values)

    def get_reached_goal(self, start_s, reachable):
        """Returns the preconditions of a reached goal or None.
        """
        for goal in self.env.get_goals():
            if reachable.is_in('x', goal):
                return (('x', goal),)
        return None

    def _toeffects(self, s):
        pos, boxes = s
        effects = []
        effects.append(('x', pos))
        for bval, box_pos in zip(_get_boxvals(len(boxes)), boxes):
            effects.append((bval, box_pos))
        for tile in self.non_walls:
            if tile != pos and tile not in boxes:
                effects.append(('.', tile))
        return effects


class SokobanExtender(Extender):
    def __init__(self, env):
        self.targets = env.get_targets()
        self.pusher_extender = PusherExtender(env)

    def reset(self, start_s):
        return self.pusher_extender.reset(start_s)

    def get_new_actions(self, *args):
        return self.pusher_extender.get_new_actions(*args)

    def get_reached_goal(self, start_s, reachable):
        """Returns the reached goal or None.
        The goal is represented as a list of (value, tile) pairs.
        """
        # an abstract env with more targets than boxes is supported
        pos, boxes = start_s

        boxvals = _get_boxvals(len(boxes))
        goal_pres = _assign_boxes(boxvals, self.targets, reachable)
        return goal_pres


def _get_boxvals(num_boxes):
    boxvals = []
    for box_num in xrange(num_boxes):
        boxvals.append('o%s' % box_num)
    return boxvals

def _assign_boxes(boxvals, targets, reachable):
    """Assigns every box to a target.
    It is OK to have more targets than boxes.
    The function returns pairs (bval, target)
    or None when no such assignment is possible.
    """
    if len(boxvals) == 0:
        return []

    bval = boxvals[0]
    rest_boxes = boxvals[1:]
    for i, target in enumerate(targets):
        if reachable.is_in(bval, target):
            rest_targets = targets[:i] + targets[i+1:]
            assignment = _assign_boxes(rest_boxes, rest_targets, reachable)
            if assignment is not None:
                assignment.append((bval, target))
                return assignment

    return None

