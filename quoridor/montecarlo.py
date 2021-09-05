from copy import deepcopy
import numpy as np
from mcts_node import Node
import config


class MCTS:
    '''

    Attributes
    ----------
    cpuct : float
        Constant used for node evaluation

    '''
    def __init__(self):
        '''

        Paramators
        ----------
        None.

        '''
        self.cpuct = config.C_PUT

    def _bolzman_distribution(self, probs, gamma):
        '''

        Parameters
        ----------
        probs : list, numpy.ndarray
            Probabilities got from node(times of root node's childeren => score).
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        scores : numpy.ndarray
            regularized Scores.

        '''
        probs = np.power(np.array(probs), 1 / gamma)
        probs = probs / np.sum(probs)

        return probs

    def get_probs(self, net, board, simulations, gamma):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        board : Board
            Board class defined in game.py.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        probs : numpy.ndarray
            Rate distribution only for movale actions.

        '''
        root = Node(board, 0, self.cpuct, root=True)
        for _ in range(simulations):
            root.eval(net)
        probs = [c.n for c in root.children]

        if gamma == 0:
            action = np.argmax(probs)
            probs = np.zeros_like(probs)
            probs[action] = 1
        else:
            probs = self._bolzman_distribution(probs, gamma)

        return probs

    def take_action(self, net, board, simulations, gamma=0):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        board : Board
            Board class defined in game.py.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        action : int
            Next action this Monte-Carlo Algorithm says you should choose.

        '''
        probs = self.get_probs(net, board, simulations, gamma)
        action = np.random.choice(board.takable_actions(), p=probs)

        return action

    def mcts_action(self, net, board, simulations, gamma=0):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        board : Board
            Board class defined in game.py.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        action : int
            Next action this Monte-Carlo Algorithm says you should choose.

        '''
        root = Node(board, 0, self.cpuct)
        takables = root.board.takable_actions()
        root.children = []

        for a in takables:
            old_board = deepcopy(board)
            root.children.append(Node(old_board.next_board(a), 0, self.cpuct))

        for _ in range(100):
            root.eval_without_net()

        takables = board.takable_actions()
        ns = [c.n for c in root.children]
        action = takables[np.argmax(ns)]

        return action

    def take_match_action(self, net, board, action_idx):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        board : Board
            Board class defined in game.py.
        action_idx : int
            Action index for person turn.

        Returns
        -------
        action : int
            Next action this Monte-Carlo Algorithm says you should choose.

        '''
        xs = board.reshape_input()
        y = net.model.predict(xs, batch_size = 1)
        takables = board.takable_actions()

        policy = y[0][0][takables]
        argmax = np.argmax(policy)
        action = takables[argmax]

        return action

    def person_action(self, net, board, action_idx):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        board : Board
            Board class defined in game.py.
        action_idx : int
            Action index for person turn.

        Returns
        -------
        action : int
            Next action from arg.

        '''
        return action_idx
