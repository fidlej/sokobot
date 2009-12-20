#!/usr/bin/env python
"""Usage: %prog patterns.txt
Groups patterns with the same end states together.
"""

import sys

import sokopath
from soko.mazing import Maze
from soko.struct.rules.sokorule import SOKOBAN_RULES
from soko.struct import preproc

def _read_patterns(input):
    patterns = []
    separator = input.readline().rstrip()
    pattern_w = len(separator)
    pattern_h = None
    lines = []
    for line in input:
        line = line[:pattern_w]
        if line != separator:
            lines.append(line)

        if len(lines) == pattern_h or (pattern_h is None and line == separator):
            pattern_h = len(lines)
            patterns.append(tuple(lines))
            lines = []

    return patterns

def _group_by(patterns, key):
    groups = {}
    for pattern in patterns:
        k = key(pattern)
        groups.setdefault(k, []).append(pattern)

    return groups

def _get_end_states(pattern):
    #TODO: allow to specify the set of rules
    # based on the env that generated the patterns.
    rules = SOKOBAN_RULES
    end_states, used_cells = preproc.detect_end_states(pattern, rules)

    #TODO: Generalize the pattern. Keep just the used cells in it.
    return tuple(end_states)

def _filter_duplicates(patterns):
    return list(set(patterns))

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    filename = args[0]
    patterns = _read_patterns(open(filename))
    patterns = _filter_duplicates(patterns)
    groups = _group_by(patterns, key=_get_end_states)

    num_key_pairs = [(len(patterns), key) for key, patterns in groups.iteritems()]
    num_key_pairs.sort(reverse=True)
    N = 8
    print "DEBUG: top %s items:" % N
    for num_patterns, end_states in num_key_pairs[:N]:
        print num_patterns, len(end_states)
        print Maze(groups[end_states][0])
        print "=" * 5
        print Maze(groups[end_states][1])
        print "=" * 5

main()
