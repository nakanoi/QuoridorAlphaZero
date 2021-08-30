import numpy as np
import os
import pickle
from copy import deepcopy
from board import Board
from logs import Log
import config


class SelfMatch:
    '''

    Attribute
    ----------
    log : Log
        Logging class.

    '''
    def __init__(self):
        '''

        Paramators
        ----------
        None.

        '''
        self.log = Log()

    def first_play_value(self, board):
        '''

        Parameters
        ----------
        board : Board
            Final Board.

        Returns
        -------
        value : int
            End value. Win=1, Draw=0, Lose=-1

        '''
        if not board.is_over():
            ValueError('This Match Hasnt Over yet.')
        if board.is_lose():
            return 0 if board.is_first() else 1
        else:
            return .5

    def _save_history(self, hist_input, hist_pv, epochs):
        '''

        Parameters
        ----------
        hist_input : list
            Match's board history.
        hist_pv : list
            Match's policy and value history.

        Returns
        -------
        None.

        '''
        os.makedirs('histories_input', exist_ok=True)
        os.makedirs('histories_policy_value', exist_ok=True)

        path = os.path.join('histories_input', '{}.history'.format(epochs))
        with open(path, 'wb') as f:
            pickle.dump(hist_input, f)

        path = os.path.join('histories_policy_value', '{}.history'.format(epochs))
        with open(path, 'wb') as f:
            pickle.dump(hist_pv, f)

    def match(self, net, algo, simulations, gamma):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        algo : Monte-Carlo Class
            Monte-Carlo algorithm class.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        hist_input : list
            Match's board history.
        hist_pv : list
            Match's policy and value history.
        ret : int
            Match Value.

        '''
        board = Board()
        hist_input, hist_pv = [], []
        turn = 0

        while not board.is_over():
            probs = algo.get_probs(net, board, simulations, gamma)
#            print(probs)
            policy = [0 for _ in range(config.OUTPUT_SHAPE)]

            for a, p in zip(board.takable_actions(), probs):
                policy[a] = p
            hist_input.append(board.reshape_input())
            hist_pv.append([policy, None])

            action = np.random.choice(board.takable_actions(), p=probs)
            old_board = deepcopy(board)
            board = old_board.next_board(action)
#            print(board, '\naction =', action, board.walls_self, board.walls_other)
            turn += 1

        value = self.first_play_value(board)
        ret = value
        for i in range(len(hist_pv)):
            hist_pv[i][1] = value
            value *= -1

        return hist_input, hist_pv, ret

    def selfmatch(self, net, algo, matches, simulations, gamma, epoches=0):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model
        algo : Monte-Carlo Class
            Monte-Carlo algorithm class.
        matches : int
            Match times.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.
        epoches : int
            Played epoch times.

        Returns
        -------
        None.

        '''
        hist_inputs, hist_pvs, results = [], [], []

        for i in range(matches):
            print('\rSelf Play: {}/{} => '.format(i + 1, matches), end='')
            hist_input, hist_pv, value = self.match(net, algo, simulations, gamma)

            hist_inputs.extend(hist_input)
            hist_pvs.extend(hist_pv)
            results.append(value)
            print(value)

        self.log.log_result(results, epoches)
        self._save_history(hist_inputs, hist_pvs, epoches)
