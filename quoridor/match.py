import os
from copy import deepcopy
from board import Board
from networks import Network
from montecarlo import MCTS
from logs import Log
import config


class Match:
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

    def _first_point(self, board):
        '''

        Parameters
        ----------
        board : Board Class
            Board Class build in board.py.

        Returns
        -------
        point : int
            Match's result point.

        '''
        if not board.is_over():
            ValueError('This Match Hasnt Over yet.')
        if board.is_lose():
            return 0 if board.is_first() else 1
        else:
            return .5

    def _update_network(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        os.remove(os.path.join('networks', 'best_network.h5'))
        os.rename(
            os.path.join('networks', 'current_network.h5'),
            os.path.join('networks', 'best_network.h5'),
        )

    def play(self, algo, simulations, gamma, nets):
        '''

        Parameters
        ----------
        algo : MCTS Class
            Monte-Carlo algorithm class.
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.

        Returns
        -------
        point : float
            Match's result point.

        '''
        board = Board()
        while not board.is_over():
            if board.is_first():
                action = algo.take_action(
                    nets[0], board, simulations, gamma
                )
            else:
                action = algo.take_action(
                    nets[1], board, simulations, gamma
                )
            old_board = deepcopy(board)
            board = old_board.next_board(action)

        point = self._first_point(board)

        return point

    def evaluate(self, simulations, gamma, eval_matches, epoches=0):
        '''

        Parameters
        ----------
        simulations : int
            Number you want to repeat for root noe evaluation.
        gamma : int, float
            Constance used on Bolzman distribution.
        eval_matches : int
            Iterations for Monte-Carlo evaluation.
        epoches : int
            Played epoch times.

        Returns
        -------
        None.

        '''
        current_net = Network(load=True, load_file='current_network.h5')
        best_net = Network(load=True)
        mcts = MCTS(config.C_PUT)

        nets = [current_net, best_net]
        total_points = 0
        results = []

        for i in range(eval_matches):
            if i % 2 == 0:
                v = self.play(mcts, simulations, gamma, nets)
            else:
                v = 1 - self.play(mcts, simulations, gamma, list(reversed(nets)))

            total_points += v
            results.append(v)
            print('\rEvaluation: {}/{}'.format(i + 1, eval_matches), end=' ')

        av = total_points / eval_matches
        print('Average: {}'.format(av))

        best_net.clean()
        current_net.clean()
        self.log.log_result(results, epoches)
        self._update_network()

    def play_with(self, board, actions, action_idx, cwd=None):
        '''

        Parameters
        ----------
        board : Board
            Board Class.
        actions : list
            Action list. [first player action, second player action].
        action_idx : int
            Action index for person.
        cwd : str
            Current directory string.

        Returns
        -------
        over : bool
            Is this game over.
        new_board : Board
            Board class after action.
        point : float
            Match's result point.

        '''
        net = Network(load=True, cwd=cwd)

        if board.is_over():
            point = self._first_point(board)
            return True, board, point

        else:
            if board.is_first():
                print('FIRST')
                action = actions[0](net, board, action_idx)
            else:
                print('SECOND')
                action = actions[1](net, board, action_idx)

            old_board = deepcopy(board)
            new_board = old_board.next_board(action)

        return False, new_board, None
