"""An environment that allows to push boxes that say in the way.
The player has power to push only one box.
"""

from soko.formatting import OutputField
from soko import INF_COST
from soko.env.env import Env, Action
from soko.env.pathfinder import PathFinderEnv
from soko.env.coding import BOX_MARKS, TARGET_MARKS, WALL_MARKS

from pylib import namedtuple

class PusherEnv(Env):
    PUSH_COST = 0
    MOVE_COST = 1

    def __init__(self, maze):
        self.maze = maze
        self.path_env = PathFinderEnv(maze)

    def init(self):
        pos = self.path_env.init()
        boxes = _uniquize(self.maze.find_all_positions(BOX_MARKS))
        return (pos, boxes)

    def get_actions(self, s):
        pos, boxes = s
        transitions = self.path_env.get_near_transitions(pos)
        actions = []
        for cell_pos, a in transitions:
            if cell_pos in boxes:
                if self._is_pushable(s, cell_pos):
                    actions.append(self._create_act(a, 1, 1))
            elif self._is_empty(boxes, cell_pos):
                actions.append(self._create_act(a, 0, 1))
        return actions

    def predict(self, s, a):
        pos, boxes = s
        next_pos = self.path_env.predict(pos, a)
        if next_pos in boxes:
            next_boxes = self._push_box(s, next_pos)
        else:
            next_boxes = boxes
        return (next_pos, next_boxes)

    def estim_cost(self, s, cost_limit=INF_COST):
        pos, boxes = s
        return self.path_env.estim_cost(pos, cost_limit) * self.MOVE_COST

    def _create_act(self, action, pushes, moves):
        cost = pushes * self.PUSH_COST + moves * self.MOVE_COST
        action.set_cost(cost)
        return action

    def _push_box(self, s, box_pos):
        """Returns a new tuple with boxes.
        """
        pos, boxes = s
        next_box_pos = self._get_next_box_pos(pos, box_pos)
        new_boxes = list(boxes)
        new_boxes[new_boxes.index(box_pos)] = next_box_pos
        return _uniquize(new_boxes)

    def _get_next_box_pos(self, pos, box_pos):
        x, y = pos
        bx, by = box_pos
        sx, sy = (bx - x, by - y)
        return (bx + sx, by + sy)

    def _is_pushable(self, s, box_pos):
        pos, boxes = s
        next_box_pos = self._get_next_box_pos(pos, box_pos)
        return self._is_empty(boxes, next_box_pos)

    def _is_empty(self, boxes, cell_pos):
        return (self.maze.get(cell_pos) not in WALL_MARKS
                and cell_pos not in boxes)

    def relax(self, s):
        pos, boxes = s
        if len(boxes) == 0:
            return ()

        return [(pos, boxes[:-1])]

    def format(self, s):
        field = OutputField(self.maze)
        pos, boxes = s
        field.place_targets(self.path_env.get_goals())
        field.place_player(pos)
        field.place_boxes(boxes)
        return str(field)

    def get_goals(self):
        return self.path_env.get_goals()

    def get_non_walls(self):
        non_walls = []
        field = self.maze.render_maze()
        for y, row in enumerate(field):
            for x, cell in enumerate(row):
                if cell not in WALL_MARKS:
                    non_walls.append((x, y))
        return non_walls


class SokobanEnv(PusherEnv):
    PUSH_COST = 0
    MOVE_COST = 1

    def __init__(self, maze):
        PusherEnv.__init__(self, maze)
        self.targets = _uniquize(self.maze.find_all_positions(TARGET_MARKS))
        #self.estim_cost = self._blind_estim_cost

    def _blind_estim_cost(self, s, cost_limit=None):
        pos, boxes = s
        remaining = 0
        for box in boxes:
            if box not in self.targets:
                remaining += 1

        return remaining * (self.PUSH_COST + self.MOVE_COST)

    def estim_cost(self, s, cost_limit=None):
        pos, boxes = s
        cost = 0
        for box, target in self._assign_targets(boxes):
            bx, by = box
            tx, ty = target
            cost += abs(bx - tx) + abs(by - ty)

        return cost * (self.PUSH_COST + self.MOVE_COST)

    def _assign_targets(self, boxes):
        """Returns a list of pairs (box, nearest_target).
        """
        #TODO: try all possible assignments
        # to assign a target to just one box,
        # but still don't overestimate.
        pairs = []
        targets = list(self.targets)
        for box in boxes:
            i = _index_nearest(box, targets)
            pairs.append((box, targets[i]))

        return pairs

    def relax(self, s):
        pos, boxes = s
        if len(boxes) <= 1:
            return ()

        #return [(pos, (box,)) for box in boxes]
        #return [(pos, boxes[:1]), (pos, boxes[1:])]
        half = len(boxes) // 2
        return [(pos, boxes[:half]), (pos, boxes[half:])]

    def format(self, s):
        field = OutputField(self.maze)
        pos, boxes = s
        field.place_targets(self.targets)
        field.place_player(pos)
        field.place_boxes(boxes)
        return str(field)

    def get_targets(self):
        return self.targets

class UnorderedTuple(tuple):
    def __eq__(self, other):
        return sorted(self) == sorted(other)
    def __hash__(self):
        return hash(tuple(sorted(self)))

def _uniquize(items):
    """Encodes the given list of items as an unique set.
    The returned boxes are sorted to represent
    equivalent box positions with the same state.
    An alternative would be a special __hash__() function.
    """
    #return UnorderedTuple(items)
    items.sort()
    return tuple(items)

def _index_nearest(pos, targets):
    """Returns index of the nearest target.
    """
    min_d = None
    index = None
    x, y = pos
    for i, (tx, ty) in enumerate(targets):
        d = abs(tx - x) + abs(ty - y)
        if min_d is None or d < min_d:
            min_d = d
            index = i

    return index

