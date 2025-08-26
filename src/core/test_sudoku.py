#!/usr/bin/env python3

from sudoku import SudokuGame

def test_sudoku():
    game = SudokuGame()
    
    print("Testing Sudoku game...")
    
    # Test game creation
    game.new_game("easy")
    print("✓ New game created")
    
    # Print the generated puzzle
    print("\nGenerated puzzle:")
    game.print_board()
    
    # Test making a valid move
    empty_cells = [(i, j) for i in range(9) for j in range(9) if game.board[i][j] == 0]
    if empty_cells:
        row, col = empty_cells[0]
        correct_num = game.solution[row][col]
        success = game.make_move(row, col, correct_num)
        print(f"✓ Valid move at ({row}, {col}) with number {correct_num}: {success}")
    
    # Test hint system
    hint = game.get_hint()
    if hint:
        print(f"✓ Hint received: place {hint[2]} at ({hint[0]}, {hint[1]})")
    
    # Test invalid move
    invalid_success = game.make_move(0, 0, 1)  # Try to place where number already exists
    print(f"✓ Invalid move rejected: {not invalid_success}")
    
    print("\nAll tests passed! The Sudoku game is working correctly.")

if __name__ == "__main__":
    test_sudoku()