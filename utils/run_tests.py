#!/usr/bin/env python
"""\
Usage: %prog [tests/test_file.py ..]
Runs all or the given tests.
It adds the current working directory into the sys.path.
"""

import glob
import unittest
import sys
import optparse
import logging
import os.path

sys.path.insert(0, os.path.realpath("."))

def _parse_args():
    """Returns (options, test_filenames).
    """
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option("-v", "--verbose", action="count",
            help="increase verbosity")
    parser.set_defaults(verbose=0)

    options, filenames = parser.parse_args()
    if len(filenames) == 0:
        filenames = glob.glob("tests/test_*.py")
        filenames += glob.glob("tests/*/test_*.py")
        filenames += glob.glob("tests/*/*/test_*.py")

    return options, filenames

def _is_failed(test_result):
    return len(test_result.errors) > 0 or len(test_result.failures) > 0

def _set_logging(verbosity):
    loglevel = max(logging.DEBUG, logging.WARNING - 10*verbosity)
    logging.basicConfig(level=loglevel,
            format="%(levelname)s: %(message)s")
def main():
    options, filenames = _parse_args()
    _set_logging(options.verbose)

    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=options.verbose)

    for filename in filenames:
        print "Test %s" % filename
        modname = filename.replace("/", ".")[:-3]
        module = __import__(modname, None, None, [""])
        test = loader.loadTestsFromModule(module)
        result = runner.run(test)

        if _is_failed(result):
            sys.exit(1)


if __name__ == "__main__":
    main()
