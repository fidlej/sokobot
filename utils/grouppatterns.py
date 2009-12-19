#!/usr/bin/env python
"""Usage: %prog patterns.txt
Groups patterns with the same end states together.
"""

import sys
import pprint

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
            patterns.append(lines)
            lines = []

    return patterns

def _group_by(patterns, key):
    groups = {}
    for pattern in patterns:
        k = key(pattern)
        groups.setdefault(k, []).append(pattern)

    return groups

def _get_end_states(pattern):
    #TODO: implement
    return tuple(tuple(line) for line in pattern)

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    filename = args[0]
    patterns = _read_patterns(open(filename))
    groups = _group_by(patterns, key=_get_end_states)
    for key, value in groups.iteritems():
        print len(value)

main()
