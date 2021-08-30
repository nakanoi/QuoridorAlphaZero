import numpy as np
from board import Board
from match import Match
from selfmatch import SelfMatch
from montecarlo import MCTS
from networks import Network
import config


if __name__ == '__main__':
    ''' # Sample Game(by random)
    def random_action(board):
        takables = board.takable_actions()
        action = np.random.choice(np.where(np.array(takables) == 1)[0].tolist())
        print(np.where(np.array(takables) == 1)[0][:8].tolist(), np.count_nonzero(np.array(takables)))
        return action

    res = [0, 0, 0]
    times = 10
    for i in range(times):
        board = Board()
        turn = 1
        while not board.is_over():
            if board.is_first(): state = '{} Is First: True, First: {} walls, Second: {} walls'.format(turn, board.walls_self, board.walls_other)
            else: state = '{} Is First: False, First: {} walls, Second: {} walls'.format(turn, board.walls_other, board.walls_self)
            print(state)
            print(board)

            action = random_action(board)
            board = board.next_board(action)
            turn += 1

        print(board)
        print('Over.\nIs First:', board.is_first(), '|| Is Draw:', board.is_draw(), '|| Is Lose:', board.is_lose())
        if board.is_draw(): res[1] += 1
        else:
            if board.is_first():
                if board.is_lose(): res[2] += 1
                else: res[0] += 1
            else:
                if board.is_lose(): res[0] += 1
                else: res[2] += 1
        print('[WIN, DRAW, LOSE] for first player =>', res)
        # Sample Result => [2992, 3898, 3110]

    #'''

    #''' # Sample Network 
    net = Network(
        config.INPUT_SHAPE,
        config.OUTPUT_SHAPE,
        config.FILTER,
        config.KERNEL,
        config.STRIDE,
        config.INITIALIZER,
        config.REGULARIZER,
        config.RES_NUM,
    )
    #'''

    ''' # Sample Monte-Carlo Game Play
    board = Board()
    net = Network(load=True)
    mcts = MCTS(config.C_PUT)

    while not board.is_over():
        action = mcts.next_action(
            net,
            board,
            config.SIMULATIONS,
            config.GAMMA,
        )
        board = board.next_board(action)
    print(board)
    print('Is First:', board.is_first(), 'Is Lose:', board.is_lose(), 'Is Draw:', board.is_draw())

    #'''
    ''' # Sample another verison
    match = Match()
    net = Network(load=True)
    mcts = MCTS(config.C_PUT)

    match.play(
        net,
        config.SIMULATIONS,
        config.GAMMA,
        nets=[mcts.take_action, mcts.mcts_action]
    )
    #'''

    ''' # Sample self match
    net = Network(load=True)
    mcts = MCTS(config.C_PUT)
    selfmatch = SelfMatch()
    selfmatch.selfmatch(
        net,
        mcts,
        1,#config.SELFMATCH,
        config.SIMULATIONS,
        config.GAMMA
    )
    #'''

    ''' # Sample Evaluation
    net = Network(load=True)
    match = Match()
    match.evaluate(
        config.SIMULATIONS,
        config.GAMMA,
        config.EVAL_MATCH
    )
    #'''
