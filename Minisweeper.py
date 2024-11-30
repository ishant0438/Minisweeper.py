import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        
        # Create the board and assign values to it
        self.board = self.make_new_board()
        self.assign_values_to_board()
        
        # Keep track of which locations have been dug
        self.dug = set()
        
    def make_new_board(self):
        """Create a new board with bombs randomly placed."""
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] 
        
        bombs_planted = 0   
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            
            if board[row][col] == '*':
                continue
            
            board[row][col] = '*'
            bombs_planted += 1
            
        return board
        
    def assign_values_to_board(self):
        """Assign numbers to the board based on neighboring bombs."""
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)
            
    def get_num_neighboring_bombs(self, row, col):
        """Calculate the number of bombs in the neighboring cells."""
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs
                    
    def dig(self, row, col):
        """Dig at a location. Return False if you hit a bomb, True otherwise."""
        self.dug.add((row, col))   
        
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # Recursively dig neighboring cells if the cell is empty
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
                    
        return True            
        
    def __str__(self):
        """Render the board with row and column numbers."""
        # Create a visible board to display
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]  
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '    
        
        # Add column numbers at the top
        string_rep = '   ' + '   '.join(str(i) for i in range(self.dim_size)) + '\n'
        string_rep += '   ' + '---' * self.dim_size + '\n'

        # Add row numbers at the beginning of each row
        for row_idx, row in enumerate(visible_board):
            row_string = f"{row_idx} | " + ' | '.join(row) + ' |\n'
            string_rep += row_string
            string_rep += '   ' + '---' * self.dim_size + '\n'
        return string_rep
                
def play(dim_size=10, num_bombs=10):
    """Play the Minesweeper game."""
    board = Board(dim_size, num_bombs)
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',\\s*', input("Where would you like to dig? Input as row,col: "))
        try:
            row, col = int(user_input[0]), int(user_input[1])
        except ValueError:
            print("Invalid input. Try again.")
            continue
            
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location. Try again.")
            continue
            
        safe = board.dig(row, col)
        if not safe:
            break
            
    if safe:
        print("Congratulations! You cleared the board!")
    else:
        print("Game Over! You hit a bomb!")
        # Reveal the entire board at the end
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
            
if __name__ == '__main__':
    play()

       
            
                    
            
            
        
            
        