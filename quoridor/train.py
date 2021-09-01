import glob
from match import Match
from networks import Network
from montecarlo import MCTS
from selfmatch import SelfMatch
import config


if __name__ == '__main__':
    # Network, Algorithm, Match & Selfmatch Instances
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
    mcts = MCTS(config.C_PUT)
    match = Match()
    selfmatch = SelfMatch()
    start = len(glob.glob('./histories_input/*'))

    for i in range(start, config.CYCLES, 1):
        print('********** Train for {} / {} **********'.format(i + 1, config.CYCLES))
        net = Network(load=True, )
        selfmatch.selfmatch(
            net,
            mcts,
            config.SELFMATCH,
            config.SIMULATIONS,
            config.GAMMA,
            i + 1,
        )
        net.train(
            config.EPOCHS,
            config.BATCH_SIZE,
            i + 1,
        )
        match.evaluate(
            config.SIMULATIONS,
            0,
            config.EVAL_MATCH,
            i + 1,
        )
