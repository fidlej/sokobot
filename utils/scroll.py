#!/usr/bin/env python
"""\
Usage: scoll.py solution.txt
"""

import sys
import curses

def _get_maze_height(lines):
    for i, line in enumerate(lines):
        if line == "\n":
            return i + 1

    return len(lines) + 1

def _index_appendix(lines):
    """Returns the number of line where the appendix starts.
    """
    for i in range(len(lines)-2, 0, -1):
        if lines[i] == "\n":
            return i - 1

    return 0

class Walker(object):
    def __init__(self, lines, h):
        assert len(lines) >= h
        self.lines = lines
        self.h = h
        self.pos = 0

        appendix_index = _index_appendix(lines)
        self.max_pos = appendix_index//self.h

    def get_pos(self):
        return self.pos

    def get_appendix(self):
        after_last_step = (self.max_pos + 1) * self.h
        return self.lines[after_last_step:]

    def get_state(self):
        """Returns lines for the current state.
        """
        start = self.pos * self.h
        end = start + self.h
        return self.lines[start:end]

    def forward(self):
        self.pos += 1
        self.pos = min(self.pos, self.max_pos)

    def back(self):
        self.pos -= 1
        self.pos = max(self.pos, 0)

def _scroll(screen, walker):
    curses.curs_set(0)
    _addstr(screen, "Use PageUp/PageDown for scrolling.\n")
    while True:
        _update_display(screen, walker)

        key = screen.getch()
        if key in (curses.KEY_NPAGE, curses.KEY_DOWN, ord('j')):
            walker.forward()
        elif key in (curses.KEY_PPAGE, curses.KEY_UP, ord('k')):
            walker.back()
        elif key == ord('q'):
            return

def _update_display(screen, walker):
    screen.move(1, 0)
    lines = walker.get_state()
    for line in lines:
        _addstr(screen, line)

    _addstr(screen, "step: %s\n" % walker.get_pos())
    _addstr(screen, "\n")
    for line in walker.get_appendix():
        _addstr(screen, line)
    screen.refresh()

def _addstr(screen, line):
    try:
        screen.addstr(line)
    except curses.error:
        # Ignoring errors caused by a small screen
        pass

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    solution = args[0]
    lines = file(solution, "rU").readlines()
    h = _get_maze_height(lines)
    walker = Walker(lines, h)

    curses.wrapper(_scroll, walker)

if __name__ == "__main__":
    main()

