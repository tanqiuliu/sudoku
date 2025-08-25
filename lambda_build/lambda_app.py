from mangum import Mangum
from flask import Flask, render_template, request, jsonify
import json
import os
from sudoku import SudokuGame

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sudoku_game_secret_key_123')

# Simple in-memory storage for Lambda (since sessions don't work well)
game_state = {}

def get_or_create_game(session_id="default"):
    if session_id not in game_state:
        game = SudokuGame()
        game.new_game('medium')
        game_state[session_id] = {
            'board': game.board,
            'solution': game.solution,
            'original_cells': [[game.board[i][j] != 0 for j in range(9)] for i in range(9)]
        }
    
    game = SudokuGame()
    game.board = game_state[session_id]['board']
    game.solution = game_state[session_id]['solution']
    return game

@app.route('/')
def index():
    session_id = request.args.get('session', 'default')
    game = get_or_create_game(session_id)
    return render_template('sudoku.html', 
                         board=game.board, 
                         original_cells=game_state[session_id]['original_cells'])

@app.route('/new_game/<difficulty>')
def new_game(difficulty):
    session_id = request.args.get('session', 'default')
    game = SudokuGame()
    game.new_game(difficulty)
    
    game_state[session_id] = {
        'board': game.board,
        'solution': game.solution,
        'original_cells': [[game.board[i][j] != 0 for j in range(9)] for i in range(9)]
    }
    
    return jsonify({
        'board': game.board,
        'original_cells': game_state[session_id]['original_cells']
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    row, col, num = data['row'], data['col'], data['num']
    session_id = data.get('session', 'default')
    
    game = get_or_create_game(session_id)
    
    if num == 0:
        game.board[row][col] = 0
        game_state[session_id]['board'] = game.board
        return jsonify({'valid': True, 'complete': False})
    
    if game.is_valid_move(game.board, row, col, num):
        game.board[row][col] = num
        game_state[session_id]['board'] = game.board
        is_complete = game.is_complete()
        return jsonify({'valid': True, 'complete': is_complete})
    else:
        return jsonify({'valid': False, 'complete': False})

@app.route('/get_hint')
def get_hint():
    session_id = request.args.get('session', 'default')
    game = get_or_create_game(session_id)
    hint = game.get_hint()
    if hint:
        return jsonify({'hint': {'row': hint[0], 'col': hint[1], 'num': hint[2]}})
    else:
        return jsonify({'hint': None})

# Use AWS Lambda Web Adapter approach
import awsgi

def lambda_handler(event, context):
    return awsgi.response(app, event, context)

# Set the handler for Lambda
handler = lambda_handler