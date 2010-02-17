#!/usr/bin/env python
"""Usage: %prog patterns.txt
Groups patterns with the same end states together.
"""

import sys

import sokopath
from soko.mazing import Maze
from soko.struct.rules.sokorule import SOKOBAN_RULES
from soko.struct import preproc, modeling

from pylib.namedtuple import namedtuple

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
            patterns.append(modeling.immutablize(lines))
            lines = []

    return patterns

def _group_by_end_states(pattern_endings):
    """Returns pairs (end_states, patterns) for each end_states.
    """
    groups = {}
    for pe in pattern_endings:
        group_patterns = groups.setdefault(pe.end_states, [])
        group_patterns.append(pe.pattern)

    endings = []
    for pe in pattern_endings:
        if pe.end_states in groups:
            patterns = groups.pop(pe.end_states)
            endings.append((pe.end_states, tuple(patterns)))

    return endings


class PatternEnding(namedtuple("PatternEnding", "pattern end_states num_seen")):
    """A computed ending for a single pattern.
    """
    pass

def _generate_endings(patterns):
    return [_get_ending(p) for p in patterns]

def _get_ending(pattern):
    """Calculates the ending for the given pattern.
    The ending is a pair: (end_states, (generalized_pattern,))
    """
    #TODO: allow to specify the set of rules
    # based on the env that generated the patterns.
    rules = SOKOBAN_RULES
    end_states, used_cells, num_seen = preproc.detect_end_states(pattern, rules)

    generalized_pattern = preproc.generalize(pattern, used_cells)
    end_states = tuple(set(
        preproc.generalize(s, used_cells) for s in end_states))
    return PatternEnding(generalized_pattern, end_states, num_seen)

def _filter_duplicates(items):
    return list(set(items))

def _save_endings(endings, filename):
    from pylib import disk
    import cPickle as pickle
    disk.prepare_path(filename)
    pickle.dump(endings, open(filename, "wb"), pickle.HIGHEST_PROTOCOL)

def _sort_by_fitness(pattern_endings):
    def fitness(pattern_ending):
        return pattern_ending.num_seen / float(len(pattern_ending.end_states))

    pattern_endings.sort(key=fitness, reverse=True)
    return pattern_endings

def _show_top_patterns(pattern_endings, top=20):
    print "DEBUG: top %s pattern endings:" % top
    for pe in pattern_endings[:top]:
        print "%s/%s" % (pe.num_seen, len(pe.end_states))
        print Maze(pe.pattern)
        print "=" * 5

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    filename = args[0]
    patterns = _read_patterns(open(filename))
    patterns = _filter_duplicates(patterns)
    pattern_endings = _generate_endings(patterns)
    pattern_endings = _filter_duplicates(pattern_endings)
    pattern_endings = _sort_by_fitness(pattern_endings)
    _show_top_patterns(pattern_endings)

    endings = _group_by_end_states(pattern_endings)
    _save_endings(endings, "../export/endings/sokoban2.pickle")


main()
