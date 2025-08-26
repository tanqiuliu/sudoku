from flask import Flask, render_template, request, jsonify, session
import json
from sudoku import SudokuGame

app = Flask(__name__)
app.secret_key = 'sudoku_game_secret_key_123'

def get_game():
    if 'game_board' not in session:
        game = SudokuGame()
        game.new_game('medium')
        session['game_board'] = game.board
        session['game_solution'] = game.solution
        session['original_cells'] = [[game.board[i][j] != 0 for j in range(9)] for i in range(9)]
    
    game = SudokuGame()
    game.board = session['game_board']
    game.solution = session['game_solution']
    return game

@app.route('/')
def index():
    game = get_game()
    return render_template('sudoku.html', 
                         board=game.board, 
                         original_cells=session['original_cells'])

@app.route('/new_game/<difficulty>')
def new_game(difficulty):
    game = SudokuGame()
    game.new_game(difficulty)
    session['game_board'] = game.board
    session['game_solution'] = game.solution
    session['original_cells'] = [[game.board[i][j] != 0 for j in range(9)] for i in range(9)]
    
    return jsonify({
        'board': game.board,
        'original_cells': session['original_cells']
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    row, col, num = data['row'], data['col'], data['num']
    
    game = get_game()
    
    if num == 0:
        game.board[row][col] = 0
        session['game_board'] = game.board
        return jsonify({'valid': True, 'complete': False})
    
    if game.is_valid_move(game.board, row, col, num):
        game.board[row][col] = num
        session['game_board'] = game.board
        is_complete = game.is_complete()
        return jsonify({'valid': True, 'complete': is_complete})
    else:
        return jsonify({'valid': False, 'complete': False})

@app.route('/get_hint')
def get_hint():
    game = get_game()
    hint = game.get_hint()
    if hint:
        return jsonify({'hint': {'row': hint[0], 'col': hint[1], 'num': hint[2]}})
    else:
        return jsonify({'hint': None})

if __name__ == '__main__':
    app.run(debug=True, port=5000)