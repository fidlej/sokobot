
from soko.env import coding

class OutputField(object):
    def __init__(self, maze):
        self.field = maze.render_maze()
        self._clear_field()

    def _clear_field(self):
        """It leaves just walls in the field.
        """
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell not in coding.WALL_MARKS:
                    self.field[y][x] = coding.EMPTY_MARKS[0]


    def place_targets(self, targets):
        for x, y in targets:
            self.field[y][x] = coding.TARGET_MARKS[0]

    def place_boxes(self, boxes):
        for x, y in boxes:
            self.field[y][x] = coding.BOX_MARKS[0]

    def place_player(self, pos):
        x, y = pos
        self.field[y][x] = coding.PLAYER_MARKS[0]

    def place_model(self, model):
        if model.is_out():
            return

        x, y = model.pos
        for sx, sy in model.shape:
            self.field[y + sy][x + sx] = model.mark

    def __str__(self):
        rows = []
        for row in self.field:
            rows.append(''.join(row))

        return "\n".join(rows)

