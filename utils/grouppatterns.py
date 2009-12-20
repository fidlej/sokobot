#!/usr/bin/env python
"""Usage: %prog patterns.txt
Groups patterns with the same end states together.
"""

import sys
import pprint

import sokopath
from soko.struct.rules.sokorule import SOKOBAN_RULES

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

    s = pattern
    used_cells = set()
    children = _get_children(rules, s, used_cells)
    if children is None:
        children = [s]

    #TODO: do a breath-first till all end states.
    return tuple(children)

def _get_children(rules, s, used_cells):
    """Returns a list of children or None
    when the given state is an end state of its pattern.
    An end state does not have enough info for a rule.
    """
    local_used_cells = set()
    children = []
    for rule in rules:
        rule_children = rule.get_children(s, local_used_cells)
        if rule_children is None:
            return None
        else:
            children += rule_children

    used_cells.update(local_used_cells)
    return children

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

    print "DEBUG: some pattern groups:"
    for key, value in groups.items()[:8]:
        print len(key), len(value)

main()
