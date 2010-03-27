#!/usr/bin/env python

import sokopath
from soko.solver import solver_lookup, mc
from soko.credit.assigning import Critic
from soko.env import env_lookup

MAZE_FILENAMES = [
        "data/sokoban/move1.txt",
        "data/sokoban/move2.txt",
        "data/sokoban/move3.txt",
        "data/sokoban/sokoban2.txt",
        ]

NUM_REPEATS = 10
NUM_MEASURES = 1

def _create_envs(maze_filenames, counter):
    envs = []
    config = solver_lookup.Config(**solver_lookup.DEFAULT_CONFIG)
    for filename in maze_filenames:
        env = env_lookup.create_env(filename, counter)
        env.configure(config)
        envs.append(env)

    return envs


def main():
    critic = Critic(storage_filename=None)
    counter = env_lookup.CallCounter()
    envs = _create_envs(MAZE_FILENAMES, counter)
    num_failed = 0
    num_plays = 0
    total_count = 0
    for i in xrange(NUM_MEASURES):
        for env, filename in zip(envs, MAZE_FILENAMES):
            print "%s/%s failed before %s" % (num_failed, num_plays, filename)
            solver = mc.McSolver()
            for repeat in xrange(NUM_REPEATS):
                path = None
                num_attempts = 0
                while path is None:
                    num_attempts += 1
                    num_plays += 1
                    counter.reset()
                    path = solver.solve_with_critic(env, critic)
                    total_count += counter.get_count()
                    if path is None:
                        num_failed += 1
                    else:
                        print "%s: ok with %s" % (
                                num_attempts, counter.get_count())

    print "failed: %s/%s with %s" % (num_failed, num_plays, total_count)


if __name__ == "__main__":
    main()

