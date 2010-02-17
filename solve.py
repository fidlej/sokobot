#!/usr/bin/env python
"""\
Usage: %prog [level_file]
Outputs a solution path.
"""

import optparse
import logging
import sys

from soko import runtime
from soko.visual import StateVisualizer, LengthVisualizer, WalkVisualizer
from soko.env import env_lookup
from soko.solver import solver_lookup

LEVEL_FILENAME = "data/sokoban/sokoban5.txt"
DEFAULT_SOLVER="astar"


def _parse_args():
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option("--vs", action="store_true",
            help="visualize solution states")
    parser.add_option("--vw", action="store_true",
            help="visualize the walk over expanded states")
    parser.add_option("-s", "--solver",
            help="solver to use (default=%s)" % DEFAULT_SOLVER)
    parser.set_defaults(solver=DEFAULT_SOLVER)

    options, args = parser.parse_args()
    if len(args) == 0:
        level_filename = LEVEL_FILENAME
    elif len(args) == 1:
        level_filename = args[0]
    else:
        parser.error("expected only one level file")

    logging.debug("Solving %s", level_filename)
    return options, level_filename

def _build_visualizers(options, env_wrapper, call_counter):
    visualizers = []
    if options.vs:
        visualizers.append(StateVisualizer())
    if options.vw:
        visualizers.append(WalkVisualizer(env_wrapper))

    visualizers.append(LengthVisualizer(call_counter))
    return visualizers

def _solve_level(env, solver):
    path = solver.solve(env)
    if path is None:
        logging.warning("No path found!")
        sys.exit(0)

    return path

def _visualize(env, path, visualizers):
    for vis in visualizers:
        sys.stdout.write(vis.render(env, path))

def main(use_psyco=False):
    logging.basicConfig(level=logging.DEBUG)
    options, level_filename = _parse_args()

    call_counter = env_lookup.CallCounter()
    env_wrapper = env_lookup.create_env(level_filename, call_counter)
    visualizers = _build_visualizers(options, env_wrapper, call_counter)
    env, solver = solver_lookup.create_task(env_wrapper, options.solver)

    if use_psyco:
        runtime.use_psyco()
    path = _solve_level(env, solver)

    env_wrapper.stop_listeners()
    _visualize(env, path, visualizers)

if __name__ == "__main__":
    main()

