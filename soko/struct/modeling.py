"""
Operations over the common 2D state representation.
"""

def extract_state(maze):
    """Extract the initial state from the maze.
    """
    field = maze.render_maze()
    return immutablize(field)

def predict(s, a):
    """Returns the next state.
    """
    next_s = mutablize(s)
    for pos, mark in a.get_cmd():
        x, y = pos
        next_s[y][x] = mark

    return immutablize(next_s)

def immutablize(field):
    return tuple(tuple(line) for line in field)

def mutablize(field):
    return list(list(line) for line in field)


