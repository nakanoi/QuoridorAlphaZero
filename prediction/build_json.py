import sys
sys.path.append('..')
sys.path.append('../quoridor')

import numpy as np
from quoridor import board


def board_to_dict(dict):
    ret_dict = {'_type': 'Board'}
    if isinstance(dict.pawn_self, board.Pawn):
        if isinstance(dict.pawn_self.position, list):
            ret_dict['pawn_self'] = {
                'position': dict.pawn_self.position,
                }
        else:
            ret_dict['pawn_self'] = {
                'position': dict.pawn_self.position.tolist(),
            }

    if isinstance(dict.pawn_other, board.Pawn):
        if isinstance(dict.pawn_other.position, list):
            ret_dict['pawn_other'] = {
                'position': dict.pawn_other.position,
            }
        else:
            ret_dict['pawn_other'] = {
                'position': dict.pawn_other.position.tolist(),
            }

    if isinstance(dict.pawn_other_position, (np.ndarray, list)):
        if isinstance(dict.pawn_other_position, list):
            ret_dict.setdefault('pawn_other_position', dict.pawn_other_position)
        else:
            ret_dict.setdefault('pawn_other_position', dict.pawn_other_position.tolist())

    if isinstance(dict.wall_vertical, board.WallVertical):
        if isinstance(dict.wall_vertical.open_vertical, list):
            ret_dict['wall_vertical'] = {
                'open_vertical': dict.wall_vertical.open_vertical
            }
        else:
            ret_dict['wall_vertical'] = {
                'open_vertical': dict.wall_vertical.open_vertical.tolist()
            }

    if isinstance(dict.wall_horizontal, board.WallHorizontal):
        if isinstance(dict.wall_horizontal.open_horizontal, list):
            ret_dict['wall_horizontal'] = {
                'open_horizontal': dict.wall_horizontal.open_horizontal
            }
        else:
            ret_dict['wall_horizontal'] = {
                'open_horizontal': dict.wall_horizontal.open_horizontal.tolist()
            }

    if isinstance(dict.wall, board.Wall):
        if isinstance(dict.wall.vertical, list):
            ret_dict['wall'] = {
                'vertical': dict.wall.vertical,
                'horizontal': dict.wall.horizontal
            }
        else:
            ret_dict['wall'] = {
                'vertical': dict.wall.vertical.tolist(),
                'horizontal': dict.wall.horizontal.tolist()
            }

    takables = dict.takable_actions()
    if isinstance(takables, list):
        ret_dict.setdefault('takables', takables)

    if isinstance(dict.walls_self, int):
        ret_dict.setdefault('walls_self', dict.walls_self)

    if isinstance(dict.walls_other, int):
        ret_dict.setdefault('walls_other', dict.walls_other)

    if isinstance(dict.turn, int):
        ret_dict.setdefault('turn', dict.turn)

    return ret_dict


def dict_to_board(dic):
    from quoridor.board import Board, WallHorizontal, WallVertical, Wall, Pawn

    if 'over' in dic and dic['over']:
        board = Board(
            pawn_self = Pawn(position =  np.array(dic['pawn_other']['position']), ),
            pawn_other = Pawn(position = np.array(dic['pawn_self']['position']), ),
            wall_vertical = WallVertical(vertical = np.rot90(np.array(dic['wall_vertical']['open_vertical']), 2), ),
            wall_horizontal = WallHorizontal(horizontal = np.rot90(np.array(dic['wall_horizontal']['open_horizontal']), 2), ),
            wall = Wall(vertical = np.rot90(np.array(dic['wall']['vertical']), 2), horizontal = np.rot90(np.array(dic['wall']['horizontal']), 2), ),
            walls_self = dic['walls_other'],
            walls_other = dic['walls_self'],
            turn = dic['turn'],
        )
        return board

    board = Board(
        pawn_self = Pawn(position = np.array(dic['pawn_self']['position']), ),
        pawn_other = Pawn(position = np.array(dic['pawn_other']['position']), ),
        wall_vertical = WallVertical(vertical = np.array(dic['wall_vertical']['open_vertical']), ),
        wall_horizontal = WallHorizontal(horizontal = np.array(dic['wall_horizontal']['open_horizontal']), ),
        wall = Wall(vertical = np.array(dic['wall']['vertical']), horizontal = np.array(dic['wall']['horizontal']), ),
        walls_self = dic['walls_self'],
        walls_other = dic['walls_other'],
        turn = dic['turn'],
    )

    return board
