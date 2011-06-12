
import logging
from soko.solver.solver import Solver
from soko.perception import perceiving, saving

from libctw import factored, modeling


class PerceptSolver(Solver):
    """A sokoban solver.
    It converts the seen states to a sequence of bits.
    It then predicts the next action to take.

    It is used to show the predicted paths.
    """

    def solve(self, env):
        """Returns a rollout path for testing.
        The path does not have to be a solution.
        """
        policy = PerceptPolicy()

        s = env.init()
        num_steps = 100
        path = []
        for i in xrange(num_steps):
            policy.add_history(env, s)
            actions = env.get_actions(s)
            a = policy.next_action(actions)
            if a is None:
                logging.warn("ending the path because of an invalid action")
                return path

            path.append(a)
            s = env.predict(s, a)

        return path


def _prepare_model(perceiver, num_remembered_steps):
    num_action_bits = perceiver.get_num_action_bits()
    return _get_trained_agent(perceiver.get_num_percept_bits(),
            num_action_bits, num_remembered_steps)


class PerceptPolicy:
    def __init__(self):
        self.num_remembered_steps = 2
        self.perceiver = perceiving.SokobanPerceiver()
        self.agent_model = _prepare_model(self.perceiver,
                self.num_remembered_steps)

    def init_history(self, env, node):
        self.agent_model.switch_history()
        self._show_history(env, self.agent_model, node)

    def _show_history(self, env, agent_model, node):
        from soko.env.env import Action
        sas = [node.s]
        for i in xrange(self.num_remembered_steps):
            if node.prev_node is None:
                break
            sas.insert(0, node.a)
            sas.insert(0, node.prev_node.s)
            node = node.prev_node

        for item in sas:
            if isinstance(item, Action):
                bits = self.perceiver.encode_action(item)
            else:
                bits = self.perceiver.encode_state(env, item)
            agent_model.see_added(bits)

    def next_action(self, actions):
        """Returns a valid action or None.
        """
        action_bits = _advance(self.agent_model,
                self.perceiver.get_num_action_bits())
        try:
            action = self.perceiver.decode_action(action_bits)
        except ValueError, e:
            logging.warn("predicted invalid action_bits: %s", action_bits)
            return None

        if action.cmd not in [a.cmd for a in actions]:
            logging.info("predicted impossible action: %s", action_bits)
            return None

        return action

    def add_history(self, env, s):
        percept = self.perceiver.encode_state(env, s)
        self.agent_model.see_added(percept)


def _advance(model, num_bits):
    return [_advance_bit(model) for i in xrange(num_bits)]


def _advance_bit(model):
    one_p = model.predict_one()
    assert 0 <= one_p <= 1.0, "invalid P: %s" % one_p
    if one_p >= 0.5:
        bit = 1
    else:
        bit = 0

    model.see_added([bit])
    return bit


def _get_trained_agent(num_percept_bits, num_action_bits,
        num_remembered_steps):
    train_seqs = saving.load_training_seqs()
    #TEST: don't limit the number of used seqs
    train_seqs = train_seqs[:15]

    max_depth = (num_remembered_steps * (num_percept_bits + num_action_bits) +
            num_action_bits)
    agent_model = factored.create_model(max_depth=max_depth)
    source_info = modeling.Interlaced(num_percept_bits, num_action_bits)
    modeling.train_model(agent_model, train_seqs, bytes=False,
            source_info=source_info)
    return agent_model

