from flask import Flask, render_template, jsonify, request
import sys
sys.path.append('..')
sys.path.append('../quoridor')
import json
from copy import deepcopy
from build_json import board_to_dict, dict_to_board
from quoridor import config
from quoridor.board import Board
from quoridor.montecarlo import MCTS
from quoridor.match import Match


app = Flask(__name__, static_folder = "./../dist/static", template_folder = "./../dist")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/action', methods=['POST'])
def take_action():
    mcts = MCTS(config.C_PUT)
    match = Match()
    actions = [mcts.take_match_action, mcts.person_action]
    board_dict = request.get_json()
    cwd = './../quoridor'
    network_first = board_dict['network_first']

    if 'pawn_self' not in board_dict:
        board = Board()
        new_board = deepcopy(board)
        over, point = False, None
        if network_first:
            over, new_board, point = match.play_with(new_board, actions, None, cwd=cwd)

    else:
        if not board_dict['network_first']:
            actions = actions[::-1]

        # Player
        board = dict_to_board(board_dict)
        over, new_board, point = match.play_with(board, actions, int(board_dict['take_action']), cwd=cwd)
        # Network
        board = deepcopy(new_board)
        over, new_board, point = match.play_with(board, actions, None, cwd=cwd)

        if over:
            new_board_dic = board_to_dict(new_board)
            new_board_dic['over'] = True
            new_board = dict_to_board(new_board_dic)
            point = 1
        elif new_board.is_over():
            over = True
            point = 0

    new_board_dic = board_to_dict(new_board)
    new_board_dic.setdefault('over', over)
    new_board_dic.setdefault('point', point)
    new_board_dic.setdefault('network_first', network_first)
    new_board_json = json.dumps(new_board_dic)

    return jsonify(new_board_json)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, )
