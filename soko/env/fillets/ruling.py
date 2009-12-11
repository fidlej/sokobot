
from . import fall, resisting
from pylib import v2

DOWN_SHIFT = (0, 1)
ACTION_SHIFTS = ((-1,0), (1,0), (0,-1), (0,1))

class Rules(object):
    def __init__(self, maze):
        self.field = resisting.Field(maze)
        self.models = []

    def set_models(self, models):
        #TODO: ignore the movable models that are out
        self.models = models
        self.field.place_models(models)

    def calc_move(self, unit, shift):
        """Returns (next_positions, cost) pair or (None, None)
        when the action is not possible.
        """
        self.push_cost = 0
        deep_resist = resisting.get_unit_resist(self.field, unit, shift)
        if deep_resist is False:
            return None, None

        self.memory = Memory(self.models)
        deep_resist.append(unit)
        self._do_pushing(deep_resist, shift)
        self._settle_positions()

        #TODO: check dead fall
        #TODO: check dead tickling
        #TODO: check dead stress

        positions = [m.pos for m in self.models]
        self._restore_models()

        return positions, _action_cost_fn(self.push_cost, 1)

    def init_positions(self, models):
        self.set_models(models)
        self._settle_positions()
        return [m.pos for m in self.models]

    def _do_pushing(self, models, shift):
        if len(models) > 1:
            self.push_cost = 1

        self._move_models(models, shift)

    def _settle_positions(self):
        was_change = True
        while was_change:
            was_change = self._do_falling()
            #TODO: prevent moving out when it is dead
            was_change = was_change or self._do_moving_out()

    def _do_falling(self):
        was_falling = False
        landslip = fall.Landslip(self.field, self.models)
        falling = landslip.get_falling()
        while len(falling) > 0:
            was_falling = True
            self.push_cost = 1
            self._move_models(falling, DOWN_SHIFT)
            falling = landslip.get_falling()

        return was_falling

    def _do_moving_out(self):
        was_moved_out = False
        for model in self.models:
            if not model.should_go_out() or model.is_out():
                continue

            x, y = model.pos
            for shift in ACTION_SHIFTS:
                if self.field.is_way_out(model, shift):
                    was_moved_out = True
                    self._move_out(model)
                    break

        return was_moved_out

    def _restore_models(self):
        self.memory.restore_models()
        self.field.place_models(self.models)

    def _move_models(self, moving_models, shift):
        for model in moving_models:
            model.pos = v2.sum(model.pos, shift)
        self.field.place_models(self.models)

    def _move_out(self, model):
        self.field.unmark(model)
        model.pos = (-1000,-1000)

class Memory(object):
    """It remebers falls and pushes
    to know what the dangerous moves.
    """
    def __init__(self, models):
        self.models = models
        self.orig_positions = [m.pos for m in models]

    def restore_models(self):
        for pos, model in zip(self.orig_positions, self.models):
            model.pos = pos

    def get_falling(self):
        return self._get_moved(lambda dx, dy: dy > 0)

    def get_pushed(self):
        return self._get_moved(lambda dx, dy: dx != 0)

    def _get_moved(self, condition):
        moved = []
        for pos, model in zip(self.orig_positions, self.models):
            dx, dy = v2.diff(model.pos, pos)
            if condition(dx, dy):
                moved.append(model)

        return moved

def _action_cost_fn(pushes, moves):
    #return pushes
    return moves

