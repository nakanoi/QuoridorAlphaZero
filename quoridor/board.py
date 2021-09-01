'''
1: Passable
0: Blocked

direction =  1: Go Left
direction = -1: Go Right
direction =  9: Go Forward
direction = -9: Go Backward
'''
import numpy as np
from config import LENGTH, BREAK, WALLS


class WallHorizontal:
    '''

    Attributes
    ----------
    open_horizontal : np.nddarray
        Numpy array represents each horizontal wall is passable.
        1 means passible.

    '''
    def __init__(self, horizontal=None):
        '''

        Paramators
        ----------
        horizontal : np.nddarray
            Numpy array represents each horizontal wall is passable.
            1 means passible.

        '''
        self.open_horizontal = np.ones(shape=(LENGTH - 1, LENGTH), dtype=np.int32) if horizontal is None else horizontal

    def block(self, idx):
        '''

        Parameters
        ----------
        idx : int
            Index of board.

        Returns
        -------
        None

        '''
        v, h = divmod(idx, LENGTH - 1)
        self.open_horizontal[v, h] = 0
        self.open_horizontal[v, h + 1] = 0

    def passable(self, before_idx, direction):
        '''

        Parameters
        ----------
        before_idx : int
            Index of board.
        direction : int
            Moving direction mentioned avobe.

        Returns
        -------
        movable : int
            Wheter this action from 'before_position' to 'after_action' is valid according to instance variable open_horizontal.
            1 equals to that you can move(valid).

        '''
        v, h = divmod(before_idx, LENGTH) # == idx to position
        # Go Forward
        if direction == LENGTH:
            return self.open_horizontal[v, h]
        # Go Backward
        elif direction == -LENGTH:
            return self.open_horizontal[v - 1, h]


class WallVertical:
    '''

    Attributes
    ----------
    open_vertical : np.nddarray
        Numpy array represents each vertical wall is passable.
        1 means passible.

    '''
    def __init__(self, vertical=None):
        '''

        Paramators
        ----------
        vertical : np.nddarray
            Numpy array represents each vertical wall is passable.
            1 means passible.

        '''
        self.open_vertical = np.ones(shape=(LENGTH, LENGTH - 1), dtype=np.int32) if vertical is None else vertical

    def block(self, idx):
        '''

        Parameters
        ----------
        idx : int
            Index of board.

        Returns
        -------
        None

        '''
        v, h = divmod(idx, LENGTH - 1)
        self.open_vertical[v, h] = 0
        self.open_vertical[v + 1, h] = 0

    def passable(self, before_idx, direction):
        '''

        Parameters
        ----------
        before_idx : int
            Index of board.
        direction : int
            Moving direction mentioned avobe.

        Returns
        -------
        movable : int
            Wheter this action from 'before_position' to 'after_action' is valid according to instance variable open_vartical.
            1 equals to that you can move(valid).

        '''
        # Go Left
        v, h = divmod(before_idx, LENGTH)
        if direction == 1:
            movable = self.open_vertical[v, h]
        # Go Right
        elif direction == -1:
            movable = self.open_vertical[v, h - 1]

        return movable


class Wall:
    '''

    Attributes
    ----------
    vertical : np.nddarray
        Numpy array represents each vertical wall is passable.
        1 means passible.

    horizontal : np.nddarray
        Numpy array represents each horizontal wall is passable.
        1 means passible.

    '''
    def __init__(self, vertical=None, horizontal=None):
        '''

        Paramators
        ----------
        vertical : np.nddarray
            Numpy array represents each vertical wall is passable.
            1 means passible.

        horizontal : np.nddarray
            Numpy array represents each horizontal wall is passable.
            1 means passible.

        '''
        self.vertical = np.ones(shape=(LENGTH - 1, LENGTH - 1), dtype=np.int32) if vertical is None else vertical
        self.horizontal = np.ones(shape=(LENGTH - 1, LENGTH - 1), dtype=np.int32) if horizontal is None else horizontal


class Pawn:
    '''

    Attributes
    ----------
    pawn : np.ndarray
        Numpy array represents where pawn is and which is 1.
    position : np.nddarray
        Pawn's position index. [vertical, horizontal].
    walls : int
        How many walls does this pawn have.

    '''
    def __init__(self, position=None):
        '''

        Paramators
        ----------
        position : np.ndarray
            Pawn's position. [vertical, horizontal].

        '''
        mid = LENGTH // 2
        self.pawn = np.zeros(shape=(LENGTH, LENGTH), dtype=np.int32)
        self.position = np.array([0, mid]) if position is None else position # [vertical, horitontal]
        self.pawn[self.position[0], self.position[1]] = 1
        self.walls = WALLS


class UnionFind:
    def __init__(self):
        self.pars = [-1 for _ in range(LENGTH ** 2)]
        self.sizes = [1 for _ in range(LENGTH ** 2)]

    def root(self, x):
        if self.pars[x] == -1:
            return x
        else:
            self.pars[x] = self.root(self.pars[x])
            return self.pars[x]

    def issame(self, x, y):
        return self.root(x) == self.root(y)

    def unite(self, x, y):
        x, y = self.root(x), self.root(y)
        if x == y: return False
        if self.size(x) < self.size(y):
            x, y = y, x
        self.pars[y] = x
        self.sizes[x] += self.sizes[y]

        return True

    def size(self, x):
        return self.sizes[self.root(x)]


class Board:
    '''

    Attributes
    ----------
    pawn_self : Pawn
        Pawn class for self player.
    pawn_other : Pawn
        Pawn class for other player.
    pawn_other_position : np.ndarray
        Other Pawn's position from self pawn's view.
        [vertical, horizontal].
    wall_vertical : WallVertical
        WallVertical class from self pawn's view.
    wall_horizontal : WallHorizontal
        WallHorizontal class from self pawn's view.
    wall : Wall
        Wall class from self pawn's view.
    walls_self : int
        How many walls does self pawn have.
    walls_other : int
        How many walls does other pawn have.
    turn : int
        Match turn.
    forward : np.ndarray
        Pawn's move for forward.
    left : np.ndarray
        Pawn's move for left.
    backward : np.ndarray
        Pawn's move for backward.
    right : np.ndarray
        Pawn's move for right.
    moves : tupple
        4 moves tupple avobe.
    attr_names : dict
        This Class's attribute name for building class.

    '''
    def __init__(
            self,
            pawn_self = None,
            pawn_other = None,
            wall_vertical = None,
            wall_horizontal = None,
            wall = None,
            walls_self = None,
            walls_other = None,
            turn = 1,
        ):
        '''

        Paramators
        ----------
        pawn_self : Pawn
            Pawn class for self player.
        pawn_other : Pawn
            Pawn class for other player.
        pawn_other_position : np.ndarray
            Other Pawn's position from self pawn's view.
            [vertical, horizontal].
        wall_vertical : WallVertical
            WallVertical class from self pawn's view.
        wall_horizontal : WallHorizontal
            WallHorizontal class from self pawn's view.
        wall : Wall
            Wall class from self pawn's view.
        walls_self : int
            How many walls does self pawn have.
        walls_other : int
            How many walls does other pawn have.
        turn : int
            Match turn.

        '''
        self.pawn_self = Pawn() if pawn_self is None else pawn_self
        self.pawn_other = Pawn() if pawn_other is None else pawn_other
        self.pawn_other_position = np.array([LENGTH - 1, LENGTH - 1]) - self.pawn_other.position
        self.wall_vertical = WallVertical() if wall_vertical is None else wall_vertical
        self.wall_horizontal = WallHorizontal() if wall_horizontal is None else wall_horizontal
        self.wall = Wall() if wall is None else wall
        self.walls_self = WALLS if walls_self is None else walls_self
        self.walls_other = WALLS if walls_other is None else walls_other
        self.turn = turn
        # Moves
        self.forward = np.array([1, 0])
        self.left = np.array([0, 1])
        self.backward = np.array([-1, 0])
        self.right = np.array([0, -1])
        self.moves = (self.forward, self.left, self.backward, self.right)

        self.attr_names = {
            'pawn_self', 'pawn_other', 'pawn_other_position', 'wall_vertical',
            'wall_horizontal', 'wall', 'walls_self', 'walls_other', 'turn',
        }
        self._build_attrs_dict()

    def __str__(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        s : str
            Board's expression in string.

        '''
        s = ''
        for v in range(LENGTH):
            for h in range(LENGTH - 1):
                if self.pawn_self.pawn[v, h]:
                    s += ' 1 ' if self.is_first() else ' 2 '
                elif np.all(np.array([v, h]) == self.pawn_other_position):
                    s += ' 2 ' if self.is_first() else ' 1 '
                else:
                    s += '   '
                s += ' ' if self.wall_vertical.open_vertical[v, h] else '|'

            if self.pawn_self.pawn[v, LENGTH - 1]:
                s += ' 1 \n' if self.is_first() else ' 2 \n'
            elif np.all(np.array([v, LENGTH - 1]) == self.pawn_other_position):
                s += ' 2 \n' if self.is_first() else ' 1 \n'
            else:
                s += '   \n'

            if v == LENGTH - 1: continue
            for h in range(LENGTH - 1):
                s += '   *' if self.wall_horizontal.open_horizontal[v, h] else '---*'
            s += '   \n' if self.wall_horizontal.open_horizontal[v, LENGTH - 1] else '---\n'

        return s
    
    def _build_attrs_dict(self):
        '''

        Parameters
        ----------
        None.
        Returns
        -------
        None

        '''
        self.attrs = {}
        for k in self.attr_names:
            self.attrs[k] = getattr(self, k)

    def _set_attrs(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None

        '''
        for k, v in self.attrs.items():
            delattr(self, k)
            setattr(self, k, v)

    def _position_to_idx(self, position):
        '''

        Parameters
        ----------
        position : list
            Position indecs list.

        Returns
        -------
        idx : int
            Index of board.

        '''
        idx = position[0] * LENGTH + position[1]

        return idx

    def _idx_to_position(self, idx):
        '''

        Parameters
        ----------
        idx : int
            Index of board.

        Returns
        -------
        position : list
            Position indecs list. [vertical, horizontal].

        '''
        position = divmod(idx, LENGTH)

        return list(position)

    def _is_out_board(self, after_position):
        '''

        Parameters
        ----------
        after_position : numpy.ndarray
            Position after moving.

        Returns
        -------
        movable : bool
            Wheter this 'after_position' is valid. If this is out, return True.

        '''
        movable = after_position[0] < 0 or LENGTH <= after_position[0] or after_position[1] < 0 or LENGTH <= after_position[1]

        return movable

    def _is_movable_from_move(self, before_position, after_position):
        '''

        Parameters
        ----------
        before_position : numpy.ndarray
            Position befre moving.

        after_position : numpy.ndarray
            Position after moving.

        Returns
        -------
        movable : int
            Wheter this action from 'before_position' to 'after_action' is valid.
            If movable, return 1.(valid).

        '''
        before_idx = self._position_to_idx(before_position)
        after_idx = self._position_to_idx(after_position)
        direction = after_idx - before_idx

        if direction in (LENGTH, -LENGTH):
            movable = self.wall_horizontal.passable(before_idx, direction)
        elif direction in (1, -1):
            movable = self.wall_vertical.passable(before_idx, direction)

        return movable

    def _is_blockable_vertical(self, vertical, horizontal):
        '''

        Parameters
        ----------
        vertical : int
            Vertical index where you want to build wall. (= np's axis 0)

        horizontal : int
            Horizontal index where you want to build wall. (= np's axis 1)

        Returns
        -------
        blockable : int
            Wheter you can put wall on this position .
            If blockable(you can put wall on there), return 1.(valid).

        '''
        # Whether vertical block is doubled.
        blockable = self.wall_vertical.open_vertical[vertical, horizontal] & self.wall_vertical.open_vertical[vertical + 1, horizontal]
        # Build Block over horizontal block.
        if not self.wall.horizontal[vertical, horizontal]:
            blockable = 0

        return blockable

    def _is_blockable_horizontal(self, vertical, horizontal):
        '''

        Parameters
        ----------
        vertical : int
            Vertical index where you want to build wall. (= np's axis 0)

        horizontal : int
            Horizontal index where you want to build wall. (= np's axis 1)

        Returns
        -------
        blockable : int
            Wheter you can put wall on this position .
            If blockable(you can put wall on there), return 1.(valid).

        '''
        # Whether horizontal block is doubled.
        blockable = self.wall_horizontal.open_horizontal[vertical, horizontal] & self.wall_horizontal.open_horizontal[vertical, horizontal + 1]
        # Build Block over vertical block.
        if not self.wall.vertical[vertical, horizontal]:
            blockable = 0

        return blockable
    
    def _build_union_find(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        uf : UnionFind
            Union Find Class which considers for self.block.

        '''
        uf = UnionFind()
        for i in range(LENGTH):
            for j in range(LENGTH):
                idx = self._position_to_idx([i, j])
                if j < LENGTH - 1 and self.wall_vertical.open_vertical[i, j] == 1:
                    uf.unite(idx, idx + 1)
                if i < LENGTH - 1 and self.wall_horizontal.open_horizontal[i, j] == 1:
                    uf.unite(idx, idx + LENGTH)

        return uf

    def _union_find_goalable(self, uf, is_self):
        '''

        Parameters
        ----------
        uf : UnionFind
            Union Find Class which considers for self.block.

        is_self : Bool
            Is this check for Self or Other.

        Returns
        -------
        res : bool
            Is this block valid. When valid, return True.

        '''
        self_idx = self._position_to_idx(self.pawn_self.position)
        other_idx = self._position_to_idx(self.pawn_other_position)
        for g in range(LENGTH):
            if is_self:
                res = uf.issame(self_idx, self._position_to_idx([LENGTH - 1, g]))
            else:
                res = uf.issame(other_idx, self._position_to_idx([0, g]))
            if res: return True

        return False

    def is_lose(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None

        '''
        return 1 in self.pawn_other.pawn[LENGTH - 1]

    def is_draw(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None

        '''
        return self.turn >= BREAK

    def is_over(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None

        '''
        return self.is_lose() or self.is_draw()

    def is_first(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None

        '''
        return self.turn % 2 == 1

    def movable(self):
        '''

        Parameters
        ----------
        None

        Returns
        -------
        movables : list
            Takable actions for moving pawn. 1 means takable.
            [forward, left, backward, right, jump_forward, jump_left, jump_backward, jump_right]

        '''
        movables = [0 for _ in range(8)]
        for i, move in enumerate(self.moves):
            next_position = self.pawn_self.position + move
            if self._is_out_board(next_position):
                continue

            # If this move is not distructed by wall (= pawn can move),
            if self._is_movable_from_move(self.pawn_self.position, next_position):
                # If there is other pawn on the next position
                if np.all(self.pawn_other_position == next_position):
                    # Repeat The same action => 2 * move
                    jumped_position = next_position + move
                    if not self._is_out_board(jumped_position) and self._is_movable_from_move(next_position, jumped_position):
                        movables[i + 4] = 1
                        continue

                    else:
                        for j, jump in enumerate(self.moves):
                            # jump == move => Checked avobe, == -move => Return to before position.
                            if np.all(jump == move) or np.all(jump == -move):
                                continue
                            jumped_position = next_position + jump
                            # This jump is valid
                            if not self._is_out_board(jumped_position) and self._is_movable_from_move(next_position, jumped_position):
                                movables[j + 4] = 1
                # This move is valid. You dont have to jump.
                else:
                    movables[i] = 1

        return movables

    def blockable(self):
        '''

        Parameters
        ----------
        None

        Returns
        -------
        blockable : list
            blockable indecs. 1 means takable.
            [block_idx(vertical)...] + [block_idx(horizontal)...]

        '''
        # Whether you can have more than a bloc
        if self.walls_self <= 0:
            blockable = [0 for _ in range(2 * (LENGTH - 1) * (LENGTH - 1))]
            return blockable

        # Where are blocks already build
        vertical, horizontal = [1 for _ in range((LENGTH - 1) ** 2)], [1 for _ in range((LENGTH - 1) ** 2)]
        for v in range(LENGTH - 1):
            for h in range(LENGTH - 1):
                # If this point hasnt been built wall
                if self._is_blockable_vertical(v, h):
                    self.wall_vertical.open_vertical[v, h] = 0
                    self.wall_vertical.open_vertical[v + 1, h] = 0
                    self.wall.vertical[v, h] = 0
                    uf = self._build_union_find()
                    res_s = self._union_find_goalable(uf, True)
                    res_o = self._union_find_goalable(uf, False)

                    if not res_s or not res_o:
                        vertical[v * (LENGTH - 1) + h] = 0

                    self.wall_vertical.open_vertical[v, h] = 1
                    self.wall_vertical.open_vertical[v + 1, h] = 1
                    self.wall.vertical[v, h] = 1
                else:
                    vertical[v * (LENGTH - 1) + h] = 0

                # If this point hasnt been built wall
                if self._is_blockable_horizontal(v, h):
                    self.wall_horizontal.open_horizontal[v, h] = 0
                    self.wall_horizontal.open_horizontal[v, h + 1] = 0
                    self.wall.horizontal[v, h] = 0
                    uf = self._build_union_find()
                    res_s = self._union_find_goalable(uf, True)
                    res_o = self._union_find_goalable(uf, False)

                    if not res_s or not res_o:
                        horizontal[v * (LENGTH - 1) + h] = 0

                    self.wall_horizontal.open_horizontal[v, h] = 1
                    self.wall_horizontal.open_horizontal[v, h + 1] = 1
                    self.wall.horizontal[v, h] = 1
                else:
                    horizontal[v * (LENGTH - 1) + h] = 0

        return vertical + horizontal

    def takable_actions(self):
        '''

        Parameters
        ----------
        None

        Returns
        -------
        actions : list
            Takable actions indecs. 1 means takable.
            [forward, left, backward, right, jump_forward, jump_left, jump_backward, jump_right]
            + [block_idx(vertical)...] + [block_idx(horizontal)...]
            0  ~   3: Just move next to self pawn.
            4  ~   7: Move next to other's pawn.
            8  ~  71: Build Wall Vertically.
            72 ~ 127: Build Wall Horizontally.

        '''
        actions = self.movable() + self.blockable()
        actions = np.nonzero(actions)[0].tolist()

        return actions

    def move(self, action):
        '''

        Parameters
        ----------
        action : int
            Action index defined in takable_actions.
            [forward, left, backward, right, jump_forward, jump_left, jump_backward, jump_right]

        Returns
        -------
        None

        '''
        # Just Move to the next
        if action < 4:
            self.pawn_self.position += self.moves[action]

        # Move next to other pawn
        elif 4 <= action < 8:
            self.pawn_self.position = self.pawn_other_position + self.moves[action - 4]

    def block(self, action):
        '''

        Parameters
        ----------
        action : int
            Action index defined in takable_actions.

        Returns
        -------
        None

        '''
        # Build Wall Vertically
        if action < (LENGTH - 1) * (LENGTH - 1) + 8:
            idx = action - 8
            v, h = divmod(idx, LENGTH - 1)
            self.wall_vertical.open_vertical[v, h] = 0
            self.wall_vertical.open_vertical[v + 1, h] = 0
            self.wall.vertical[v, h] = 0

        # Build Wall Horizontally
        elif action < 2 * (LENGTH - 1) * (LENGTH - 1) + 8:
            idx = action - ((LENGTH - 1) * (LENGTH - 1) + 8)
            v, h = divmod(idx, LENGTH - 1)
            self.wall_horizontal.open_horizontal[v, h] = 0
            self.wall_horizontal.open_horizontal[v, h + 1] = 0
            self.wall.horizontal[v, h] = 0

        self.walls_self -= 1

    def next_board(self, action):
        '''

        Parameters
        ----------
        action : int
            Action index defined in takable_actions.

        Returns
        -------
        Board : Board Class
            Board Class after took arg's action.

        '''
        # Move Pawn
        if action < 8:
            self.move(action)

        # Build Wall
        elif action < 2 * (LENGTH - 1) * (LENGTH - 1) + 8:
            self.block(action)

        open_vertical = np.rot90(self.wall_vertical.open_vertical, 2)
        open_horizontal = np.rot90(self.wall_horizontal.open_horizontal, 2)
        wall_vertical = np.rot90(self.wall.vertical, 2)
        wall_horizontal = np.rot90(self.wall.horizontal, 2)

        new_board = Board(
            pawn_self = Pawn(position = self.pawn_other.position, ),
            pawn_other = Pawn(position = self.pawn_self.position, ),
            wall_vertical = WallVertical(vertical = open_vertical, ),
            wall_horizontal = WallHorizontal(horizontal = open_horizontal, ),
            wall = Wall(vertical = wall_vertical, horizontal = wall_horizontal),
            walls_self = self.walls_other,
            walls_other = self.walls_self,
            turn = self.turn + 1,
        )

        return new_board

    def reshape_input(self):
        '''

        Parameters
        ----------
        None

        Returns
        -------
        array : np.ndarray
            Network Input like [self_pawan, other_pawan, wall_vertical, wall_horizontal].
            Each array has (9, 9) shape. => (9, 9, 4) => reshape (1, 9, 9, 4) for batch training.

        '''
        add = np.zeros(LENGTH)
        v = np.hstack((self.wall_vertical.open_vertical, add.reshape(LENGTH, 1)))
        h = np.vstack((self.wall_horizontal.open_horizontal, add))
        array = np.dstack([self.pawn_self.pawn, self.pawn_other.pawn, v, h])

        for _ in range(self.walls_self):
            array = np.dstack([array, np.ones(shape=(LENGTH, LENGTH))])
        for _ in range(WALLS - self.walls_self):
            array = np.dstack([array, np.zeros(shape=(LENGTH, LENGTH))])
        for _ in range(self.walls_other):
            array = np.dstack([array, np.ones(shape=(LENGTH, LENGTH))])
        for _ in range(WALLS - self.walls_other):
            array = np.dstack([array, np.zeros(shape=(LENGTH, LENGTH))])

        array = array.reshape(1, LENGTH, LENGTH, 4 + WALLS * 2)

        return array
    
    def board_to_str(self):
        s = ''
        for v in range(LENGTH):
            for h in range(LENGTH - 1):
                if self.pawn_self.pawn[v, h]:
                    s += ' 1 ' if self.is_first() else ' 2 '
                else:
                    s += '   '
                s += ' ' if self.wall_vertical.open_vertical[v, h] else '|'

            if self.pawn_self.pawn[v, LENGTH - 1]:
                    s += ' 1 ' if self.is_first() else ' 2 '
            else:
                s += '   \n'

            if v == LENGTH - 1: continue
            for h in range(LENGTH - 1):
                s += '   *' if self.wall_horizontal.open_horizontal[v, h] else '---*'
            s += '   \n' if self.wall_horizontal.open_horizontal[v, LENGTH - 1] else '---\n'

        return s
