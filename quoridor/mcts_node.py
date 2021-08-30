import numpy as np
from copy import deepcopy
import config


class Node:
    '''

    Attribute
    ----------
    board : Board
        This node's board Class.
    cpuct : floar
        c puct constance.
    w : float
        Value this node ever got.
    n : int
        How many times this node ever simulated.
    children : list
        Contains Node classes this node has.
    root : bool
        Is this node root.
    history : set
        Match's history.
    dammy : bool
        Is this node dammy.
    eps : float
        Constance for noise.
    alpha : float
        Constance for noise.

    '''
    def __init__(self, board, policy, cpuct, root = False, history = None, dammy = False):
        '''

        Parameters
        ----------
        board : Board
            Board class defined in game.py.
        policy : numpy.ndarray
            Monte-Carlo's policy only for movable actions.
        cpuct : float
            Constant used for node evaluation
        root : bool
            Wether this node is root one.
        history : dict
            Board's history contains board's string expression.
        dammy : bool
            Is this instance dammy (has this node's board already appeared)?

        Returns
        -------
        None.

        '''
        self.board = board
        self.policy = policy
        self.cput = cpuct
        self.w = 0
        self.n = 0
        self.children = None
        self.root = root
        self.history = set() if history is None else history
        self.dammy = dammy
        self.eps = config.EPS
        self.alpha = config.ALPHA

    def _select(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        node : Node class
            Node class of this node's children which has highest value.

        '''
        t = sum([c.n for c in self.children])
        sq = np.sqrt(t)
        values = []

        for c in self.children:
            if c.dammy:
                v = -np.inf
            elif c.n == 0:
                v = self.cput * c.policy * sq / (1 + c.n)
            else:
                v = -c.w / c.n + self.cput * c.policy * sq / (1 + c.n)
            values.append(v)
        node = self.children[np.argmax(values)]

        return node

    def _select_without_net(self):
        '''

        Returns
        -------
        node : Node class
            Node class which has highest UCB1 value.

        '''
        for c in self.children:
            if c.n == 0 and not c.dammy:
                return c

        total = 0
        for c in self.children:
            total += c.n
        values = [-c.w / c.n + pow(2 * np.log(total) / c.n, 0.5) if not c.dammy else -np.inf for c in self.children]
        node = self.children[np.argmax(values)]

        return node

    def _random_action(self, board):
        '''

        Parameters
        ----------
        board : Board
            Board class defined in game.py.

        Returns
        -------
        action : int
            Action index chosen randomly.

        '''
        takables = board.takable_actions()
        action = takables[np.random.randint(0, len(takables))]

        return action

    def _playout(self, board):
        '''

        Parameters
        ----------
        board : Board
            Board class defined in game.py.

        Returns
        -------
        value : int
            Value got in playout. This works recursivly.

        '''
        if board.is_lose():
            return -1
        elif board.is_draw():
            return 0
        old_board = deepcopy(board)

        return -self._playout(old_board.next_board(self._random_action(board)))

    def _predict(self, net, board):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model.
        board : Board
            Board class defined in game.py.

        Returns
        -------
        policy : numpy.ndarray
            Monte-Carlo's policy only for movable actions.
        value : float
            Monte-Carlo's value.

        '''
        x = board.reshape_input()
        y = net.model.predict(x, batch_size=1)
        takables = board.takable_actions()

        policy = y[0][0][takables]
        policy /=  sum(policy) if sum(policy) else 1
        value = y[1][0][0]

        return policy, value

    def eval(self, net):
        '''

        Parameters
        ----------
        net : Neural Network
            Neural network class defined in network.py.
            This class has instance variable "model",
            which is tensorflow.keras.models.Model

        Returns
        -------
        value : float
            Monte-Carlo's value.

        '''
        if self.board.is_over():
            value = -1 if self.board.is_lose() else 0
            self.w += value
            self.n += 1

            return value

        if self.children is None:
            policy, value = self._predict(net, self.board)
            noises = np.random.dirichlet(alpha=[self.alpha] * len(policy))
            if self.root:
                policy = (1 - self.eps) * policy + self.eps * noises

            self.w += value
            self.n += 1
            takables = self.board.takable_actions()
            self.children = []
            idx = 0

            for a, p in zip(takables, policy):
                old_board = deepcopy(self.board)
                next_board = old_board.next_board(a)
                s = next_board.board_to_str()

                if s in self.history:
                    policy[idx] = -pow(10, 10)
                    self.children.append(Node(next_board, p, self.cput, history=self.history, dammy=True))
                else:
                    self.history.add(s)
                    self.children.append(Node(next_board, p, self.cput, history=self.history, ))
                idx += 1

        else:
            value = -self._select().eval(net)
            self.w += value
            self.n += 1

        return value

    def eval_without_net(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        value : int
            Node class of this node's children which has highest value.

        '''
        if self.board.is_over():
            value = -1 if self.board.is_lose() else 0
            self.w += value
            self.n += 1
            return value

        if self.children is None:
            value = self._playout(self.board)
            self.w += value
            self.n += 1

            if self.n == 10:
                takables = self.board.takable_actions()
                self.children = []

                for a in takables:
                    old_board = deepcopy(self.board)
                    next_board = old_board.next_board(a)
                    s = next_board.board_to_str()

                    if s in self.history:
                        self.children.append(Node(next_board, 0, self.cput, history=self.history, dammy=True))
                    else:
                        self.history.add(s)
                        self.children.append(Node(next_board, 0, self.cput, self.history))

            return value

        else:
            value = -self._select_without_net().eval_without_net()
            self.w += value
            self.n += 1

            return value
