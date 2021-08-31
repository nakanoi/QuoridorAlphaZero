from flask import Flask, render_template, jsonify, request
import sys
sys.path.append('..')
sys.path.append('../quoridor')
import json
from copy import deepcopy
from build_json import Encoder, Decoder
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
    board_json = request.get_json()
    cwd = './../quoridor'
    network_first = board_json['network_first']

    if 'pawn_self' not in board_json:
        new_board = Board()
        over = False
        point = None
        if network_first:
            board = deepcopy(new_board)
            over, new_board, point = match.play_with(board, actions, None, cwd=cwd)

    else:
        if not board_json['network_first']:
            actions = actions[::-1]

        str_board = json.dumps(board_json)
        board = json.loads(str_board, cls=Decoder)
        # Player
        over, new_board, point = match.play_with(board, actions, int(board_json['take_action']), cwd=cwd)
        board = deepcopy(new_board)
        # Network
        over, new_board, point = match.play_with(board, actions, None, cwd=cwd)

        if over:
            new_board_dic = json.dumps(new_board, cls=Encoder)
            new_board_dic = json.loads(new_board_dic)
            new_board_dic['over'] = True
            new_board_json = json.dumps(new_board_dic)
            new_board = json.loads(new_board_json, cls=Decoder)
            point = 1
        elif new_board.is_over():
            over = True
            point = 0

    new_board_dic = json.dumps(new_board, cls=Encoder)
    new_board_json = json.loads(new_board_dic)

    new_board_json.setdefault('over', over)
    new_board_json.setdefault('point', point)
    new_board_json.setdefault('network_first', network_first)

    return jsonify(new_board_json)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, )
