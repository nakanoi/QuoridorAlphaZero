import numpy as np
import os
import sys
from networks import Network
from montecarlo import MCTS
from copy import deepcopy
from board import Board
import config


def get_value(board, mode='selfmatch'):
    if not board.is_over():
        ValueError('This Match Hasnt Over yet.')

    if mode == 'selfmatch':
        if board.is_lose():
            return -1 if board.is_first() else 1
        else:
            return 0

    elif mode == 'eval_match':
        if board.is_lose():
            return 0 if board.is_first() else 1
        else:
            return 0.5


def save_history(hists, epoch, process):
    folders = ('histories_input', 'histories_policy', 'histories_value')
    for i, f in enumerate(folders):
        os.makedirs(os.path.join(f, epoch), exist_ok=True)
        path = os.path.join(f, epoch, process + '.npy')
        np.save(path, hists[i])


def single_match(epoch, process):
    '''same as class method'''
    net = Network(load=True, )
    algo = MCTS()
    board = Board()
    hist_input, hist_policy = None, None

    while not board.is_over():
        probs = algo.get_probs(net, board, config.SIMULATIONS, config.GAMMA)
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
    hist_value = np.zeros(hist_policy.shape[0])
    for i in range(len(hist_value)):
        hist_value[i] = value
        value *= -1

    save_history([hist_input, hist_policy, hist_value], epoch, process)


def eval_match(mode, first):
    '''

    Paramators
    ----------
    first : str
        Is this turn first for current network.
    
    Returns
    -------
    None.

    '''
    current_net = Network(load=True, load_file='current_network.h5')
    best_net = Network(load=True)
    algo = MCTS()
    nets = [current_net, best_net] if first == 'True' else [best_net, current_net]

    board = Board()
    while not board.is_over():
        if board.is_first():
            action = algo.take_action(
                nets[0], board, config.SIMULATIONS, 0,
            )
        else:
            action = algo.take_action(
                nets[1], board, config.SIMULATIONS, 0,
            )
        old_board = deepcopy(board)
        board = old_board.next_board(action)

    point = get_value(board, mode)
    best_net.clean()
    current_net.clean()
    print(point)


if __name__ == '__main__':
    match_type, args = sys.argv[1], sys.argv[2:]

    if match_type == 'selfmatch':
        single_match(*args[:2])
    else:
        eval_match(match_type, args[0])
