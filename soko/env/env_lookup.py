
from soko import mazing

from soko.env.pathfinder import PathFinderEnv
from soko.env.pusherenv import PusherEnv, SokobanEnv
from soko.env.fillets import FilletsEnv
from soko.env.npuzzle import PuzzleEnv
from soko.struct.glue import EnvGlue
#SokobanEnv = EnvGlue

ENVS = dict(
        finder=PathFinderEnv,
        pusher=PusherEnv,
        sokoban=SokobanEnv,
        soko=SokobanEnv,
        microban=SokobanEnv,
        xsokoban=SokobanEnv,
        fillets=FilletsEnv,
        npuzzle=PuzzleEnv,
        )

def create_env(level_filename, call_counter=None):
    name = _parse_envname(level_filename)
    env_factory = ENVS[name]
    maze = mazing.parse_maze(level_filename)
    env = env_factory(maze)
    env = EnvWrapper(env)
    if call_counter is not None:
        env.add_listener("predict", call_counter.call_me)

    return env

class EnvWrapper(object):
    """Provides the env methods
    and also allows to place listeners on them.
    """
    def __init__(self, env):
        self.env = env
        self.listeners = {}
        self._support_listeners("get_actions")
        self._support_listeners("predict")

    def _support_listeners(self, type):
        def fn(*args, **kw):
            for listener in self.listeners[type]:
                listener(*args, **kw)
            return getattr(self.env, type)(*args, **kw)

        setattr(self, type, fn)
        self.listeners[type] = []

    def add_listener(self, type, listener):
        self.listeners[type].append(listener)

    def stop_listeners(self):
        for key in self.listeners.iterkeys():
            self.listeners[key] = []

    def __getattr__(self, name):
        return getattr(self.env, name)



def _parse_envname(level_filename):
    """Returns the dirname of the level.
    """
    import os.path
    return os.path.basename(os.path.dirname(os.path.realpath(level_filename)))

class CallCounter(object):
    class LimitReachedError(Exception):
        pass

    def __init__(self, limit=None):
        self.count = 0
        self.limit = limit

    def get_count(self):
        return self.count

    def reset(self):
        self.count = 0

    def _inc(self):
        self.count += 1
        if self.limit and self.count >= self.limit:
            raise self.LimitReachedError

    def call_me(self, *args, **kw):
        self._inc()

