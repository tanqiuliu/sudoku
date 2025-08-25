import random
import copy
from typing import List, Tuple, Optional


class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid_move(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid"""
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, board: List[List[int]]) -> bool:
        """Solve sudoku using backtracking"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(board, i, j, num):
                            board[i][j] = num
                            if self.solve_sudoku(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def generate_complete_board(self) -> List[List[int]]:
        """Generate a complete valid Sudoku board"""
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill diagonal 3x3 boxes first
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box + i][box + j] = nums[i * 3 + j]
        
        # Solve the rest
        self.solve_sudoku(board)
        return board
    
    def remove_numbers(self, board: List[List[int]], difficulty: str = "medium") -> List[List[int]]:
        """Remove numbers from complete board to create puzzle"""
        difficulty_levels = {
            "easy": 40,
            "medium": 50,
            "hard": 60
        }
        
        cells_to_remove = difficulty_levels.get(difficulty, 50)
        puzzle = copy.deepcopy(board)
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[:cells_to_remove]:
            puzzle[i][j] = 0
        
        return puzzle
    
    def new_game(self, difficulty: str = "medium"):
        """Generate a new Sudoku puzzle"""
        complete_board = self.generate_complete_board()
        self.solution = copy.deepcopy(complete_board)
        self.board = self.remove_numbers(complete_board, difficulty)
    
    def make_move(self, row: int, col: int, num: int) -> bool:
        """Make a move on the board"""
        if 0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9:
            if self.board[row][col] == 0 and self.is_valid_move(self.board, row, col, num):
                self.board[row][col] = num
                return True
        return False
    
    def is_complete(self) -> bool:
        """Check if the puzzle is complete"""
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def get_hint(self) -> Optional[Tuple[int, int, int]]:
        """Get a hint (row, col, number)"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            return (row, col, self.solution[row][col])
        return None
    
    def print_board(self):
        """Print the current board"""
        print("   " + " ".join([str(i) if i % 3 != 0 or i == 0 else "| " + str(i) for i in range(9)]))
        print("  " + "_" * 23)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("  |" + "-" * 21 + "|")
            row_str = str(i) + " |"
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                row_str += str(self.board[i][j] if self.board[i][j] != 0 else ".") + " "
            row_str += "|"
            print(row_str)
        print("  " + "_" * 23)


def main():
    """Main game loop"""
    game = SudokuGame()
    
    print("Welcome to Sudoku!")
    print("Commands:")
    print("  new [easy/medium/hard] - Start new game")
    print("  move <row> <col> <num> - Make a move (0-8 for row/col, 1-9 for num)")
    print("  hint - Get a hint")
    print("  show - Show current board")
    print("  quit - Exit game")
    print()
    
    while True:
        command = input("Enter command: ").strip().lower().split()
        
        if not command:
            continue
            
        if command[0] == "quit":
            print("Thanks for playing!")
            break
        
        elif command[0] == "new":
            difficulty = command[1] if len(command) > 1 and command[1] in ["easy", "medium", "hard"] else "medium"
            game.new_game(difficulty)
            print(f"New {difficulty} game started!")
            game.print_board()
        
        elif command[0] == "move" and len(command) == 4:
            try:
                row, col, num = int(command[1]), int(command[2]), int(command[3])
                if game.make_move(row, col, num):
                    print("Move made!")
                    game.print_board()
                    if game.is_complete():
                        print("Congratulations! You solved the puzzle!")
                else:
                    print("Invalid move!")
            except ValueError:
                print("Invalid input! Use: move <row> <col> <num>")
        
        elif command[0] == "hint":
            hint = game.get_hint()
            if hint:
                row, col, num = hint
                print(f"Hint: Try placing {num} at position ({row}, {col})")
            else:
                print("No hints available!")
        
        elif command[0] == "show":
            game.print_board()
        
        else:
            print("Unknown command! Type 'quit' to exit.")


if __name__ == "__main__":
    main()