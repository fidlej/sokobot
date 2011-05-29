
from soko.solver.solver import Solver
from soko.perception import perceiving

from libctw import ctw, modeling


class PerceptSolver(Solver):

    def solve(self, env):
        """Returns a rollout path for testing.
        The path does not have to be a solution.
        """
        #TODO: load a trained model
        agent_model = ctw.create_model()
        perceiver = perceiving.SokobanPerceiver()
        num_action_bits = perceiver.get_num_action_bits()

        s = env.init()
        num_steps = 100
        path = []
        for i in xrange(num_steps):
            percept = perceiver.encode_state(env, s)
            print "percept:", percept
            agent_model.see_added(percept)
            action_bits = _advance(agent_model, num_action_bits)
            action = perceiver.decode_action(action_bits)
            path.append(action)
            s = env.predict(s, action)

        return path


def _advance(model, num_bits):
    return [_advance_bit(model) for i in xrange(num_bits)]


def _advance_bit(model):
    one_p = model.predict_one()
    assert 0 <= one_p <= 1.0, "invalid P: %s" % one_p
    if one_p >= 0.5:
        bit = 1
    else:
        bit = 0

    model.see_generated([bit])
    return bit

