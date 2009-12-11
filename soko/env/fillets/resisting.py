
from . import parsing
from pylib import v2

class _Border(object):
    def is_unit(self):
        return False

    def get_weight(self):
        return parsing.WEIGHT_FIXED

class Field(object):
    def __init__(self, maze):
        self.field = maze.render_maze()
        self._clean_field()
        self.border = _Border()

    def _clean_field(self):
        for row in self.field:
            for c, model in enumerate(row):
                row[c] = None

    def place_models(self, models):
        self._clean_field()
        for model in models:
            self.mark(model)

    def mark(self, model):
        self._mark_value(model, model)

    def unmark(self, model):
        self._mark_value(model, None)

    def _mark_value(self, model, value):
        if model.is_out():
            return

        x, y = model.pos
        for sx, sy in model.shape:
            self.field[y + sy][x + sx] = value

    def _get_model(self, pos):
        """Returns the model on the given position or None.
        """
        try:
            x, y = pos
            return self.field[y][x]
        except IndexError:
            return self.border

    def is_way_out(self, model, shift):
        """Returns whether the model could go out
        in this direction.
        """
        #TODO: Check also resist in the other phases.
        # For example, when the object would have a wider tail.

        # Only the outer border should be in the way.
        resist_set = self.get_resist_set(model, shift)
        if len(resist_set) != 1:
            return False
        return self.border in resist_set

    def get_resist_set(self, model, shift):
        """Returns what blocks the model to be on the given pos.
        """
        pos = v2.sum(model.pos, shift)
        resist = set()
        for mark_pos in model.shape:
            resist.add(self._get_model(v2.sum(pos, mark_pos)))

        resist.discard(model)
        resist.discard(None)
        return resist


def get_unit_resist(field, unit, shift):
    """Returns what is in the way of the given unit.
    """
    return get_deep_resist(field, unit, shift, unit.get_weight(), True)

def get_deep_resist(field, model, shift, max_weight, stop_on_unit=False):
    """Returns what is in the way of the given model or False.
    It returns False when it stops on an object
    with a bigger weight or on a unit.
    """
    deep_resist = []
    closed = set()
    closed.add(model)

    stack = [model]
    while len(stack) > 0:
        model = stack.pop()
        resist = field.get_resist_set(model, shift)
        resist -= closed
        for item in resist:
            if item.is_unit():
                if stop_on_unit:
                    return False
                continue
            elif item.get_weight() > max_weight:
                return False

            closed.add(item)
            stack.append(item)
            deep_resist.append(item)

    return deep_resist


