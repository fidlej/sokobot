
from soko.env.coding import TARGET_MARKS, BOX_MARKS, PLAYER_MARKS
from soko.mazing import Maze

PUSH_COST = 0
MOVE_COST = 1

class BoxCountingSokoEstimator(object):
    def setup_goal(self, maze):
        self.targets = maze.find_all_positions(TARGET_MARKS)

    def estim_cost(self, s):
        boxes = Maze(s).find_all_positions(BOX_MARKS)
        remaining = 0
        for box in boxes:
            if box not in self.targets:
                remaining += 1

        return remaining * (PUSH_COST + MOVE_COST)

class SokoEnvSokoEstimator(object):
    def setup_goal(self, maze):
        from soko.env.pusherenv import SokobanEnv
        self.env = SokobanEnv(maze)

    def estim_cost(self, s):
        boxes = Maze(s).find_all_positions(BOX_MARKS)
        env_s = (None, boxes)
        return self.env.estim_cost(env_s)
