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

def _group_by_end_states(endings):
    groups = {}
    for end_states, patterns in endings:
        group_patterns = groups.setdefault(end_states, [])
        group_patterns += list(patterns)

    return groups

def _generate_endings(patterns):
    return [_get_ending(p) for p in patterns]

def _get_ending(pattern):
    """Calculates the ending for the given pattern.
    The ending is a pair: (end_states, (generalized_pattern,))
    """
    #TODO: allow to specify the set of rules
    # based on the env that generated the patterns.
    rules = SOKOBAN_RULES
    end_states, used_cells = preproc.detect_end_states(pattern, rules)

    generalized_pattern = preproc.generalize(pattern, used_cells)
    end_states = set(preproc.generalize(s, used_cells) for s in end_states)
    return tuple(end_states), (generalized_pattern,)

def _filter_duplicates(patterns):
    return list(set(patterns))

def _save_endings(endings, filename):
    from pylib import disk
    import cPickle as pickle
    disk.prepare_path(filename)
    pickle.dump(endings, open(filename, "wb"), pickle.HIGHEST_PROTOCOL)

def _sort_by_fitness(endings):
    def fitness(ending):
        end_states, patterns = ending
        io_rate = len(patterns) / float(len(end_states))
        return (io_rate, len(patterns))

    endings.sort(key=fitness, reverse=True)

def _show_top_endings(endings, top=8):
    print "DEBUG: top %s endings:" % top
    for end_states, patterns in endings[:top]:
        print len(patterns), len(end_states)
        print Maze(end_states[0])
        print "=" * 5
        print Maze(patterns[0])
        print "=" * 5

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    filename = args[0]
    patterns = _read_patterns(open(filename))
    patterns = _filter_duplicates(patterns)
    endings = _generate_endings(patterns)
    endings = _filter_duplicates(endings)
    groups = _group_by_end_states(endings)

    endings = groups.items()
    _sort_by_fitness(endings)
    _save_endings(endings, "../export/endings/sokoban2.pickle")

    _show_top_endings(endings)

main()
