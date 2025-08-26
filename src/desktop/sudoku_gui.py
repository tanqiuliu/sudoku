import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from sudoku import SudokuGame


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.resizable(False, False)
        
        self.game = SudokuGame()
        self.cells = []
        self.original_cells = set()
        
        self.setup_ui()
        self.new_game()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Sudoku", font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Button(button_frame, text="New Easy Game", 
                  command=lambda: self.new_game("easy")).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="New Medium Game", 
                  command=lambda: self.new_game("medium")).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="New Hard Game", 
                  command=lambda: self.new_game("hard")).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Hint", 
                  command=self.get_hint).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Check", 
                  command=self.check_solution).grid(row=0, column=4, padx=5)
        
        # Sudoku grid
        self.grid_frame = ttk.Frame(main_frame)
        self.grid_frame.grid(row=2, column=0, columnspan=3)
        
        self.create_grid()
        
    def create_grid(self):
        self.cells = []
        font = tkfont.Font(family='Arial', size=14, weight='bold')
        
        for i in range(9):
            row_cells = []
            for j in range(9):
                # Create frame for cell with border
                cell_frame = tk.Frame(self.grid_frame, width=50, height=50,
                                    highlightbackground="black", highlightthickness=1)
                
                # Add thicker borders for 3x3 boxes
                padx = (3 if j % 3 == 0 else 1, 3 if j % 3 == 2 else 1)
                pady = (3 if i % 3 == 0 else 1, 3 if i % 3 == 2 else 1)
                
                cell_frame.grid(row=i, column=j, padx=padx, pady=pady)
                cell_frame.grid_propagate(False)
                
                # Create entry widget
                cell_var = tk.StringVar()
                cell_entry = tk.Entry(cell_frame, textvariable=cell_var, 
                                    font=font, justify='center',
                                    bd=0, highlightthickness=0,
                                    width=2)
                cell_entry.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                cell_frame.grid_rowconfigure(0, weight=1)
                cell_frame.grid_columnconfigure(0, weight=1)
                
                # Bind events
                cell_var.trace('w', lambda *args, r=i, c=j: self.on_cell_change(r, c))
                cell_entry.bind('<KeyPress>', lambda e, r=i, c=j: self.on_key_press(e, r, c))
                
                row_cells.append({
                    'var': cell_var,
                    'entry': cell_entry,
                    'frame': cell_frame
                })
            
            self.cells.append(row_cells)
    
    def on_key_press(self, event, row, col):
        if event.char.isdigit() and event.char != '0':
            if (row, col) not in self.original_cells:
                event.widget.delete(0, tk.END)
                return True
        elif event.keysym in ['BackSpace', 'Delete']:
            if (row, col) not in self.original_cells:
                return True
        return "break"
    
    def on_cell_change(self, row, col):
        if (row, col) in self.original_cells:
            return
            
        value = self.cells[row][col]['var'].get()
        
        if value == '':
            self.game.board[row][col] = 0
            self.cells[row][col]['entry'].configure(bg='white')
        elif value.isdigit() and '1' <= value <= '9':
            num = int(value)
            if self.game.is_valid_move(self.game.board, row, col, num):
                self.game.board[row][col] = num
                self.cells[row][col]['entry'].configure(bg='lightgreen')
                
                # Check if game is complete
                if self.game.is_complete():
                    messagebox.showinfo("Congratulations!", 
                                      "You solved the puzzle!\nWell done!")
            else:
                self.cells[row][col]['entry'].configure(bg='lightcoral')
                self.game.board[row][col] = 0
        else:
            self.cells[row][col]['var'].set('')
    
    def new_game(self, difficulty="medium"):
        self.game.new_game(difficulty)
        self.original_cells.clear()
        
        for i in range(9):
            for j in range(9):
                if self.game.board[i][j] != 0:
                    self.cells[i][j]['var'].set(str(self.game.board[i][j]))
                    self.cells[i][j]['entry'].configure(bg='lightgray', state='readonly')
                    self.original_cells.add((i, j))
                else:
                    self.cells[i][j]['var'].set('')
                    self.cells[i][j]['entry'].configure(bg='white', state='normal')
    
    def get_hint(self):
        hint = self.game.get_hint()
        if hint:
            row, col, num = hint
            self.cells[row][col]['var'].set(str(num))
            self.cells[row][col]['entry'].configure(bg='lightyellow')
            messagebox.showinfo("Hint", f"Try placing {num} at row {row}, column {col}")
        else:
            messagebox.showinfo("Hint", "No hints available!")
    
    def check_solution(self):
        if self.game.is_complete():
            messagebox.showinfo("Solution Check", "Congratulations! Puzzle solved correctly!")
        else:
            empty_count = sum(row.count(0) for row in self.game.board)
            messagebox.showinfo("Solution Check", 
                              f"Puzzle not complete yet.\n{empty_count} cells remaining.")


def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()