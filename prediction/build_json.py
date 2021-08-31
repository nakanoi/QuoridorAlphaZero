import sys
sys.path.append('..')
sys.path.append('../quoridor')

import json
import numpy as np
from quoridor import board


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, board.Board):
            dic = {'_type': 'Board'}
            if isinstance(o.pawn_self, board.Pawn):
                if isinstance(o.pawn_self.position, list):
                    dic['pawn_self'] = {
                        'position': o.pawn_self.position,
                    }
                else:
                    dic['pawn_self'] = {
                        'position': o.pawn_self.position.tolist(),
                    }

            if isinstance(o.pawn_other, board.Pawn):
                if isinstance(o.pawn_other.position, list):
                    dic['pawn_other'] = {
                        'position': o.pawn_other.position,
                    }
                else:
                    dic['pawn_other'] = {
                        'position': o.pawn_other.position.tolist(),
                    }

            if isinstance(o.pawn_other_position, (np.ndarray, list)):
                if isinstance(o.pawn_other_position, list):
                    dic.setdefault('pawn_other_position', o.pawn_other_position)
                else:
                    dic.setdefault('pawn_other_position', o.pawn_other_position.tolist())

            if isinstance(o.wall_vertical, board.WallVertical):
                if isinstance(o.wall_vertical.open_vertical, list):
                    dic['wall_vertical'] = {
                        'open_vertical': o.wall_vertical.open_vertical
                    }
                else:
                    dic['wall_vertical'] = {
                        'open_vertical': o.wall_vertical.open_vertical.tolist()
                    }

            if isinstance(o.wall_horizontal, board.WallHorizontal):
                if isinstance(o.wall_horizontal.open_horizontal, list):
                    dic['wall_horizontal'] = {
                        'open_horizontal': o.wall_horizontal.open_horizontal
                    }
                else:
                    dic['wall_horizontal'] = {
                        'open_horizontal': o.wall_horizontal.open_horizontal.tolist()
                    }

            if isinstance(o.wall, board.Wall):
                if isinstance(o.wall.vertical, list):
                    dic['wall'] = {
                        'vertical': o.wall.vertical,
                        'horizontal': o.wall.horizontal
                    }
                else:
                    dic['wall'] = {
                        'vertical': o.wall.vertical.tolist(),
                        'horizontal': o.wall.horizontal.tolist()
                    }

            takables = o.takable_actions()
            if isinstance(takables, list):
                dic.setdefault('takables', takables)

            if isinstance(o.walls_self, int):
                dic.setdefault('walls_self', o.walls_self)

            if isinstance(o.walls_other, int):
                dic.setdefault('walls_other', o.walls_other)

            if isinstance(o.turn, int):
                dic.setdefault('turn', o.turn)

            return dic

        return json.JSONEncoder.default(self, o)


class Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        from quoridor.board import Board, WallHorizontal, WallVertical, Wall, Pawn

        if '_type' not in o:
            return o

        if o['over']:
            board = Board(
                pawn_self = Pawn(position =  np.array(o['pawn_other']['position']), ),
                pawn_other = Pawn(position = np.array(o['pawn_self']['position']), ),
                wall_vertical = WallVertical(vertical = np.rot90(np.array(o['wall_vertical']['open_vertical']), 2), ),
                wall_horizontal = WallHorizontal(horizontal = np.rot90(np.array(o['wall_horizontal']['open_horizontal']), 2), ),
                wall = Wall(vertical = np.rot90(np.array(o['wall']['vertical']), 2), horizontal = np.rot90(np.array(o['wall']['horizontal']), 2), ),
                walls_self = o['walls_other'],
                walls_other = o['walls_self'],
                turn = o['turn'],
            )
            return board

        if o['_type'] == 'Board':
            board = Board(
                pawn_self = Pawn(position = np.array(o['pawn_self']['position']), ),
                pawn_other = Pawn(position = np.array(o['pawn_other']['position']), ),
                wall_vertical = WallVertical(vertical = np.array(o['wall_vertical']['open_vertical']), ),
                wall_horizontal = WallHorizontal(horizontal = np.array(o['wall_horizontal']['open_horizontal']), ),
                wall = Wall(vertical = np.array(o['wall']['vertical']), horizontal = np.array(o['wall']['horizontal']), ),
                walls_self = o['walls_self'],
                walls_other = o['walls_other'],
                turn = o['turn'],
            )

            return board

        return o
