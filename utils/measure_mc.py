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
NUM_MEASURES = 3

def _create_envs(maze_filenames):
    envs = []
    config = solver_lookup.Config(**solver_lookup.DEFAULT_CONFIG)
    for filename in maze_filenames:
        env = env_lookup.create_env(filename)
        env.configure(config)
        envs.append(env)

    return envs


def main():
    critic = Critic(storage_filename=None)
    envs = _create_envs(MAZE_FILENAMES)
    num_failed = 0
    num_plays = 0
    for i in xrange(NUM_MEASURES):
        for env, filename in zip(envs, MAZE_FILENAMES):
            print "%s/%s failed before %s" % (num_failed, num_plays, filename)
            for repeat in xrange(NUM_REPEATS):
                path = None
                num_attempts = 0
                while path is None:
                    num_attempts += 1
                    num_plays += 1
                    path = mc.play(env, critic)
                    if path is None:
                        num_failed += 1
                    else:
                        print "%s: ok" % num_attempts

    print "failed: %s/%s" % (num_failed, num_plays)


if __name__ == "__main__":
    main()

