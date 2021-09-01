import numpy as np
import os
from concurrent import futures

from copy import deepcopy
from board import Board
from logs import Log
import config


def get_value(board):
    if not board.is_over():
        ValueError('This Match Hasnt Over yet.')
    if board.is_lose():
        return -1 if board.is_first() else 1
    else:
        return 0

def single_match(net, algo, simulations, gamma, j):
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

    value = get_value(board)
    ret = value
    hist_value = np.zeros(hist_policy.shape[0])
    for i in range(len(hist_value)):
        hist_value[i] = value
        value *= -1

    return hist_input, hist_policy, hist_value, ret

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

    def match(self, net, algo, simulations, gamma, j):
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
        hist_inputs, hist_policies, hist_values, results = None, None, None, []
        for i in range(matches // (os.cpu_count() * 5)):
            print('Self Play Repeats: {}'.format(i), end='')
            fs = []
            with futures.ThreadPoolExecutor() as executor:
                for j in range(os.cpu_count() * 5):
                    fs.append(executor.submit(single_match, net, algo, simulations, gamma, j))
                for f in futures.as_completed(fs):
                    res = f.result()
                    hist_input, hist_policy, hist_value, value = res

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
        self._save_history(hist_inputs, hist_policies, hist_values, epoches)
