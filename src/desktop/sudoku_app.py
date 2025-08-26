#!/usr/bin/env python3
"""
Sudoku Game - Windows Desktop Application
A complete Sudoku game with GUI interface
"""

import sys
import os
import webbrowser
import threading
import time
import socket
from flask import Flask, render_template, request, jsonify
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))
from sudoku import SudokuGame

# Add the current directory to the path for template resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set template folder to the web templates
template_dir = os.path.join(os.path.dirname(__file__), '..', 'web', 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'sudoku_desktop_app_secret_key'

# Global game state
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

@app.route('/quit')
def quit_app():
    """Endpoint to quit the application"""
    def shutdown():
        time.sleep(1)  # Give time for response to be sent
        os._exit(0)
    
    threading.Thread(target=shutdown).start()
    return jsonify({'message': 'Application shutting down...'})

def find_free_port():
    """Find a free port to use for the Flask app"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def open_browser(port):
    """Open the default web browser to the app URL"""
    time.sleep(1.5)  # Give Flask time to start
    webbrowser.open(f'http://localhost:{port}')

def main():
    # Find an available port
    port = find_free_port()
    
    print("🎮 Starting Sudoku Desktop Application...")
    print("🌐 Opening browser window...")
    print(f"📝 To quit the application, close this console window or visit http://localhost:{port}/quit")
    print(f"🌍 Running on: http://localhost:{port}")
    
    # Start browser opening in a separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    try:
        # Run Flask app
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Sudoku application closed!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()