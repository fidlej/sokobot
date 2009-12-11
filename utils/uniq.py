#!/usr/bin/env python
"""\
Usage: uniq.py [filename.txt]
Prints only the unique lines.
"""

import sys

def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    if len(args) == 0:
        input = sys.stdin
    else:
        input = open(args[0])

    seen = set()
    for line in input:
        if line in seen:
            continue
        seen.add(line)
        sys.stdout.write(line)

main()
