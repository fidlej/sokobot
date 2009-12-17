"""
Operations over the common 2D state representation.
"""

def extract_state(maze):
    """Extract the initial state from the maze.
    """
    field = maze.render_maze()
    return _immutablize(field)

def predict(s, a):
    """Returns the next state.
    """
    next_s = _mutablize(s)
    for pos, mark in a.get_cmd():
        x, y = pos
        next_s[y][x] = mark

    return _immutablize(next_s)

def _immutablize(field):
    return tuple(tuple(line) for line in field)

def _mutablize(field):
    return list(list(line) for line in field)


