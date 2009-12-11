
from soko.formatting import OutputField
from soko.env.env import Env, Action
from . import parsing, ruling

class FilletsEnv(Env):
    def __init__(self, maze, models=None):
        self.maze = maze
        self.rules = ruling.Rules(maze)
        if models is not None:
            self.models = _sorted_by_type(models)
        else:
            self.models = _sorted_by_type(parsing.parse_models(maze))

        self.orig_positions = self.rules.init_positions(self.models)
        self._group_models()

    def _group_models(self):
        self.h_caches = []
        self.units = []
        self.fixed_models = []
        for model in self.models:
            if model.is_unit():
                self.units.append(model)
                self.h_caches.append({})
            elif model.is_fixed():
                self.fixed_models.append(model)

    def init(self):
        return _create_state(self.models, self.orig_positions)

    def get_actions(self, s):
        self._use_state(s)

        acts = []
        self.rules.set_models(self.models)
        for unit in self.units:
            if unit.is_out():
                continue

            for shift in ruling.ACTION_SHIFTS:
                positions, cost = self.rules.calc_move(unit, shift)
                if positions is not None:
                    acts.append(Action(
                        _create_state(self.models, positions), cost))

        return acts

    def predict(self, s, a):
        return a.get_cmd()

    def estim_cost(self, s, cost_limit=None):
        self._use_state(s)
        num_out = 0
        for unit in self.units:
            if unit.is_out():
                num_out += 1

        return len(self.units) - num_out

    def format(self, s):
        self._use_state(s)
        field = OutputField(self.maze)
        for model in self.models:
            field.place_model(model)

        return str(field)

    def _use_state(self, s):
        for pos, model in zip(s, self.models):
            model.pos = pos

def _sorted_by_type(models):
    def key_fn(model):
        return (model.style, model.shape)

    return sorted(models, key=key_fn)

def _create_state(models, positions):
    """Returns a representation of the new state.
    The models are sorted by style, shape and pos
    to make the interchangeable states equal.
    """
    array = [(m.style, m.shape, pos) for m, pos in zip(models, positions)]
    array.sort()
    return tuple(pos for style, shape, pos in array)

