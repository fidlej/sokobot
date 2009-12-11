
from soko.env import coding

class WalkVisualizer(object):
    def __init__(self, env_wrapper):
        self.env = env_wrapper
        env_wrapper.add_listener("get_actions", self._on_get_actions)

    def render(self, env, path):
        return ""

    def _on_get_actions(self, s):
        print self.env.format(s),
        print s
        print
