#!/usr/bin/env python

import sys

import sokopath
from solve import main as command

PROF_FILENAME = "stats.prof"

def _collect_profile(filename):
    import cProfile as profile
    profile.run("command(use_psyco=False)", filename)

def _view_profile(filename):
    import pstats
    p = pstats.Stats(filename)
    p.strip_dirs()
    #p.sort_stats('time')
    p.sort_stats('cumulative')
    p.print_stats(20)

def main():
    args = sys.argv[1:]
    if len(args) == 1 and args[0].endswith(".prof"):
        filename = args[0]
    else:
        filename = PROF_FILENAME
        _collect_profile(filename)
    _view_profile(filename)

if __name__ == "__main__":
    main()
