#!/usr/bin/env python
"""Usage: %prog patterns.txt
Groups patterns with the same end states together.
"""

import sys
import operator

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

def _group_by_end_states(pattern_end_states):
    groups = {}
    for pattern, end_states in pattern_end_states:
        groups.setdefault(end_states, []).append(pattern)

    return groups

def _generalize_with_end_states(patterns):
    return [_get_generalized(p) for p in patterns]

def _get_generalized(pattern):
    """Returns (generalized_pattern, end_states) pair.
    """
    #TODO: allow to specify the set of rules
    # based on the env that generated the patterns.
    rules = SOKOBAN_RULES
    end_states, used_cells = preproc.detect_end_states(pattern, rules)

    pattern = preproc.generalize(pattern, used_cells)
    end_states = set(preproc.generalize(s, used_cells) for s in end_states)
    return pattern, tuple(end_states)

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
    pattern_end_states = _generalize_with_end_states(patterns)
    pattern_end_states = _filter_duplicates(pattern_end_states)
    groups = _group_by_end_states(pattern_end_states)

    num_key_pairs = [(len(patterns), key) for key, patterns in groups.iteritems()]
    num_key_pairs.sort(reverse=True)
    N = 8
    print "DEBUG: top %s items:" % N
    for num_patterns, end_states in num_key_pairs[:N]:
        print num_patterns, len(end_states)
        print Maze(end_states[0])
        print "=" * 5
        print Maze(groups[end_states][0])
        print "=" * 5

main()
