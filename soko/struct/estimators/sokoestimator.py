
from soko.env.coding import TARGET_MARKS, BOX_MARKS
from soko.mazing import Maze

PUSH_COST = 0
MOVE_COST = 1

class BoxCountingSokoEstimator(object):
    def setup_goal(self, maze):
        self.targets = maze.find_all_positions(TARGET_MARKS)

    def estim_cost(self, s, cost_limit=None):
        boxes = Maze(s).find_all_positions(BOX_MARKS)
        remaining = 0
        for box in boxes:
            if box not in self.targets:
                remaining += 1

        return remaining * (PUSH_COST + MOVE_COST)
