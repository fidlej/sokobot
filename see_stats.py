#!/usr/bin/env python
"""\
Usage: %prog [options]
Generates a HTML page with solver stats.
"""

import sys
import logging
import optparse

from soko.stats import resulting, rendering

def _parse_args():
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option("-l", "--listen", dest="port",
            help="listen on the given port")
    parser.add_option("-m", "--measured",
            help='see this measured value ("num_visted" or "cost")')
    parser.add_option("-u", "--urlprefix",
            help='prefix to a this measured value (default="")')
    parser.add_option("-v", "--verbose", action="count",
            help="increase verbosity")
    parser.set_defaults(verbose=0, measured="num_visited", urlprefix="")

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.error("No extra arg is expected: %s" % (args,))

    options.port = _parse_port(parser, options.port)
    logging.basicConfig(level=logging.WARNING - options.verbose * 10)
    return options

def _parse_port(parser, port):
    if port is None:
        return None

    try:
        port = int(port)
        if 0 < port < 65536:
            return port
        else:
            parser.error("Invalid port number: %s" % port)
    except ValueError:
        parser.error("Invalid port: %s" % port)

def _serve_pages(port):
    from soko.stats import serving
    serving.make_server(port)

def _output_stats(measured):
    records = resulting.get_latest_records()
    sys.stdout.write(rendering.render(records, measured))

def main():
    options = _parse_args()
    if options.port:
        _serve_pages(options.port)
    else:
        rendering.setup(url_prefix=options.urlprefix)
        _output_stats(options.measured)

if __name__ == "__main__":
    main()
