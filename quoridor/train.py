import glob
from match import Match
from networks import Network
from selfmatch import SelfMatch
import config


if __name__ == '__main__':
    # Network, Algorithm, Match & Selfmatch Instances
    net = Network()
    match = Match()
    selfmatch = SelfMatch()
    start = len(glob.glob('./histories_input/*'))

    for i in range(start, config.CYCLES, 1):
        print('********** Train for {} / {} **********'.format(i + 1, config.CYCLES))
        selfmatch.parallel_match(i)
        net.train(i)
        match.parallel_evaluate(i)
