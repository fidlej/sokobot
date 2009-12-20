
class Maze(object):
    """An immutable maze info.
    """

    def __init__(self, field, border=None):
        self.field = field
        self.border = border

    def get(self, pos):
        x, y = pos
        try:
            return self.field[y][x]
        except IndexError:
            if self.border is not None:
                return self.border
            raise

    def find_positions(self, mark):
        """Returns all positions of the given mark in the maze.
        """
        positions = []
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell == mark:
                    positions.append((x, y))

        return positions

    def find_all_positions(self, marks):
        """Returns positions of all given marks.
        """
        positions = []
        for mark in marks:
            positions += self.find_positions(mark)
        return positions

    def render_maze(self):
        """Returns a list of rows with maze cells.
        """
        rows = []
        for line in self.field:
            rows.append(list(line))
        return rows

    def __str__(self):
        rows = []
        for line in self.field:
            rows.append(''.join(line))
        return "\n".join(rows)


def parse_maze(level_filename):
    field = []
    for line in file(level_filename):
        line = line.rstrip()
        field.append(line)
    return Maze(field)

