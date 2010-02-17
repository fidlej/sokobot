#!/bin/sh
# Usage: ./view.sh data/env_name/maze.txt
# Finds and displays a solution.
solution_file=`mktemp /tmp/sokobot.solution.XXXXXXXXXX` || exit 1
trap 'rm -f "$solution_file"' 0 1 2 3 15
if ./solve.py --vs "$@" >"$solution_file" ; then
    python2.6 ./utils/scroll.py "$solution_file"
fi
