
from pylib import namedtuple

WEIGHT_LIGHT = 1
WEIGHT_HEAVY = 2
WEIGHT_FIXED = 3

class Model(object):
    def __init__(self, style, shape, pos, mark):
        self.style = style
        self.shape = shape
        self.pos = pos
        self.mark = mark

    def is_unit(self):
        return self.style.is_unit

    def get_weight(self):
        return self.style.weight

    def is_fixed(self):
        return self.get_weight() == WEIGHT_FIXED

    def is_immovable(self):
        return self.is_fixed() or self.is_unit()

    def should_go_out(self):
        return self.is_unit()

    def is_out(self):
        """Returns whether the model left the room.
        """
        x, y = self.pos
        return x < 0

    def __repr__(self):
        return "%s:%s" % (self.mark, self.pos)

def parse_models(maze):
    models = []
    for style, marks in STYLE_MARKS.iteritems():
        for mark in marks:
            positions = maze.find_positions(mark)
            if len(positions) == 0:
                continue
            pos, shape = _normalize_shape(positions)
            models.append(Model(style, shape, pos, mark))

    return models

def _normalize_shape(positions):
    """Returns the first position
    and a list of offests from it.
    """
    pos = positions[0]
    x, y = pos
    shape = []
    for x2, y2 in positions:
        dx = x2 - x
        dy = y2 - y
        shape.append((dx,dy))

    return pos, shape

def find_model(models, mark):
    """Finds the model with the given mark.
    """
    for model in models:
        if model.mark == mark:
            return model

    return None

def _chars(start, end):
    """Returns a string with chars the from [start-end] set.
    """
    return "".join(chr(i) for i in range(ord(start), ord(end) + 1))

Style = namedtuple.namedtuple("Style", "weight is_unit")
STYLE_FIXED = Style(WEIGHT_FIXED, False)
STYLE_SMALL_FISH = Style(WEIGHT_LIGHT, True)
STYLE_BIG_FISH = Style(WEIGHT_HEAVY, True)
STYLE_LIGHT = Style(WEIGHT_LIGHT, False)
STYLE_HEAVY = Style(WEIGHT_HEAVY, False)

STYLE_MARKS = {
        STYLE_FIXED: "#",
        STYLE_SMALL_FISH: "+0123456789",
        STYLE_BIG_FISH: "*",
        STYLE_LIGHT: _chars("a", "z"),
        STYLE_HEAVY: _chars("A", "Z"),
        }

