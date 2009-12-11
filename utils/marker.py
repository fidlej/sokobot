#!/usr/bin/env python
"""Shows the specified places in a maze.
"""

FILENAME = "data/sokoban/microban/level018.txt"
MARK_GROUPS = (
        ((3, 6), ((3, 4), (3, 5))),
        ((4, 6), ((3, 4), (3, 5))),
        ((4, 5), ((3, 4), (3, 5))),
        ((4, 4), ((3, 4), (3, 5))),
        ((3, 4), ((2, 4), (3, 5))),
        )

import sokopath
from soko import mazing, formatting

def main():
    maze = mazing.parse_maze(FILENAME)
    for i, group in enumerate(MARK_GROUPS):
        field = formatting.OutputField(maze)
        if len(group) == 2 and isinstance(group[1][0], tuple):
            pos, boxes = group
            field.place_player(pos)
            field.place_boxes(boxes)
        else:
            field.place_boxes(group)
        print group
        print field
        raw_input()


main()

