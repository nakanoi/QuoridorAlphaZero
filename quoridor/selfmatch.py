import numpy as np
import os
import time
import subprocess
from networks import Network
from montecarlo import MCTS
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

    def _save_history(self, hist_input, hist_policy, hist_value, epochs):
        '''

        Parameters
        ----------
        hist_input : np.ndarray
            Match's board history.
        hist_policy : np.ndarray
            Match's policy history.
        hist_value : np.ndarray
            Match's value history.

        Returns
        -------
        None.

        '''
        os.makedirs('histories_input', exist_ok=True)
        os.makedirs('histories_policy', exist_ok=True)
        os.makedirs('histories_value', exist_ok=True)

        path = os.path.join('histories_input', '{}.npy'.format(epochs))
        np.save(path, hist_input)
        path = os.path.join('histories_policy', '{}.npy'.format(epochs))
        np.save(path, hist_policy)
        path = os.path.join('histories_value', '{}.npy'.format(epochs))
        np.save(path, hist_value)

    def match(self, net, algo, simulations, gamma):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
                his class has instance variable "model",
            which is tensorflow.keras.models.Model
        algo : Monte-Carlo Class
            Monte-Carlo algorithm class.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        hist_input : np.ndarray
            Match's board history.
        hist_policy : np.ndarray
            Match's policy history.
        hist_value : np.ndarray
            Match's value history.
        ret : int
            Match Value.

        '''
        board = Board()
        hist_input, hist_policy = None, None

        while not board.is_over():
            probs = algo.get_probs(net, board, simulations, gamma)
            policy = np.zeros(config.OUTPUT_SHAPE)
            for a, p in zip(board.takable_actions(), probs):
                policy[a] = p

            inp = board.reshape_input()
            if hist_input is None:
                hist_input = inp.copy()
            else:
                hist_input = np.vstack([hist_input, inp])

            if hist_policy is None:
                hist_policy = policy.copy()
            else:
                hist_policy = np.vstack([hist_policy, policy])

            action = np.random.choice(board.takable_actions(), p=probs)
            old_board = deepcopy(board)
            board = old_board.next_board(action)

        value = self.first_play_value(board)
        ret = value
        hist_value = np.zeros(hist_policy.shape[0])
        for i in range(len(hist_value)):
            hist_value[i] = value
            value *= -1

        return hist_input, hist_policy, hist_value, ret
    
    def selfmatch(self, net, algo, matches, simulations, gamma, epoch):
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
        epoch : int
            Train epoch.

        Returns
        -------
        None.

        '''
        hist_inputs, hist_policies, hist_values, results = None, None, None, []
        for i in range(matches):
            print('Self Play Repeats: {}-{}/{}'.format(j, i, matches))
            hist_input, hist_policy, hist_value, value = self.match(net, algo, simulations, gamma)
            results.append(value)

            if hist_inputs is None:
                hist_inputs = hist_input.copy()
            else:
                hist_inputs = np.vstack([hist_inputs, hist_input])

            if hist_policies is None:
                hist_policies = hist_policy.copy()
            else:
                hist_policies = np.vstack([hist_policies, hist_policy])

            if hist_values is None:
                hist_values = hist_value.copy()
            else:
                hist_values = np.append(hist_values, hist_value)

        self.log.log_result(results, epoches)
        self._save_history(hist_inputs, hist_policies, hist_values, epoches * config.PARALLEL_MATCH + j)
        

    def parallel_match(self, epoch):
        '''

        Parameters
        ----------
        epoch : int
            Train epoch.

        Returns
        -------
        None.

        '''
        for i in range(config.SELFMATCH // config.PARALLEL_MATCH):
            rs = []
            for process in range(config.PARALLEL_MATCH):
                sh = 'python async_match.py {} {} {}'.format('selfmatch', epoch, i * config.PARALLEL_MATCH + process)
                r = subprocess.Popen(sh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                rs.append(r)
            for r in rs:
                r.wait()
                print('\rSELF MATCH {} / {}'.format(i * config.PARALLEL_MATCH + process + 1, config.SELFMATCH), end='')
        print()
