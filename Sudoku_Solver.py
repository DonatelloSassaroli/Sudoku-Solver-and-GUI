# Sudoku_Solver.py
# Donatello Sassaroli
# 8/10/23
# An implementation of a sudoku solver using a backtracking algorithm. The
# initial state of the (solvable) board should be entered in the "board" 2D
# array directly below and the solved state of the sudoku will be printed to
# the console as a 2D array.

board = [
    [3,0,1,0,8,0,5,0,0],
    [0,0,0,0,0,7,0,2,0],
    [9,2,0,0,0,0,8,6,0],
    [0,0,0,1,2,0,0,5,0],
    [0,1,0,0,0,0,3,0,0],
    [6,0,2,7,0,5,0,0,0],
    [4,6,3,2,9,0,0,8,5],
    [2,5,0,8,7,3,0,4,1],
    [0,0,0,0,0,6,0,3,9]
]

# Prints out the sudoku board
def print_board(b):
    for i in range(0,9):
        if (i % 3 == 0):
            print("-------------------------")
        for j in range(0,9):
            if (j % 3 == 0):
                print("|", end = " ")
            print(b[i][j], end = " ")
            if (j == 8):
                print("|")
    print("-------------------------")

# Check if the number n is a valid move on board b at the location specified
# by row r and column c
def check_move(r,c,b,n):
    #Check if n conflicts with any values in the same row
    for i in range(0,9):
        if (n == b[r][i] and c != i):
            return False
        
    # Check if n conflicts with any values in the same column   
    for i in range(0,9):
        if (n == b[i][c]) and r != i:
            return False
    
    # Find the upper-left corner of the 3-by-3 box and use this to check if
    # n conflicts with any values in the same square
    box_r = r - (r % 3)
    box_c = c - (c % 3)
    for i in range(box_r, box_r + 3):
        for j in range(box_c, box_c + 3):
            if (n == b[i][j]):
                return False
    return True

# Find the coordinates (row, column) of the first zero searching from left to
# right then top to bottom from the upper left-hand corner
def find_zero(b):
    for i in range(0,9):
        for j in range(0,9):
            if (b[i][j] == 0):
                return (i,j)
    return (-1,-1)

# Solve the provided sudoku puzzle by predicting and backtracking
def solve(b, r, c):
    (r,c) = find_zero(b)
    if (r == -1 and c == -1):
        print_board(b)
        return True
    
    for i in range(1,10):
        if (check_move(r, c, b, i)):
            b[r][c] = i
            if (solve(b, r, c + 1)):
                return True
        b[r][c] = 0
    return False

# Print the initial state of the puzzle, solve it, then print the solved state
# the puzzle
print_board(board)
solve(board, 0, 0)