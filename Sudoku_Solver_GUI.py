# Sudoku_Solver_GUI.py
# Donatello Sassaroli
# 8/11/23
# An implementation of a sudoku solver using a backtracking algorithm. The
# initial state of the (solvable) board should be entered in the "board" 2D 
# array directly below. The current state of the board is displayed to a new
# window through Pygame's GUI module. The user can interact with the puzzle by 
# clicking on squares and attempting to enter numbers which will flash red if
# incorrect and stay on the board if correct. 
# If at any point the user would like to see the solution, press the "s" key to
# view visualization of solution. This also demonstrates how the solver works.

# Import pygame to visualize sudoku solver
import pygame

# Pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Sudoku Solver")

# 2D array of the original board along with the to be solved board (to check 
# when user imputs numbers)
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

solution = [
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

# Define variables
x = 0
y = 0
dif = 600/9
val = 0
run = True
font = pygame.font.SysFont("Arial", 32, bold = True)
font1 = pygame.font.SysFont("Arial", 60, bold = True)

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

# Solves the solution matrix in 2D array form to store the solution to refer to
# later
def solution_b(b, r, c):
    (r,c) = find_zero(b)
    if (r == -1 and c == -1):
        return True
    
    for i in range(1,10):
        if (check_move(r, c, b, i)):
            b[r][c] = i
            if (solution_b(b, r, c + 1)):
                return True
        b[r][c] = 0
    return False

# Modify the solution matrix so that it is the solution of the sudoku puzzle
solution_b(solution, 0, 0)

# Check if the user-input value is correct
def valid(i, j, k):
    if (board[i][j] == 0):
        if (solution[i][j] == k):
            return True
    return False

# Returns the coordinates in the board array given the position array
def get_cord(pos):
    global x
    x = int(pos[0]//dif)
    global y
    y = int(pos[1]//dif)

# Check if the game is over and display a message if so
def check_win(b):
    if (find_zero(b) == (-1, -1)):
        pygame.draw.line(screen, (0,255,0), (0, 300), (600, 300), 200)
        text = font1.render("You did it! (wooooo)", 10, (0,0,0))
        screen.blit(text, (100, 250))
    return False

# Draws the board onto the screen
def draw_board(select):
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), 1, (0,0,0))
                screen.blit(text, (j * dif + 25, i * dif + 15))

    for i in range(0,10):
        if (i % 3 == 0):
            thick = 7
        else:
            thick = 2
        pygame.draw.line(screen, (0,0,0), (0, i * dif), (600, i * dif), thick)
        pygame.draw.line(screen, (0,0,0), (i * dif, 0), (i * dif, 600), thick)
    if select:
        highlight_box((255,229,180), y, x)
        check_win(board)

# Outline the specified box with the given color
def highlight_box(color, x, y):
    pygame.draw.lines(screen, color, True, [(y*dif, x*dif), (y*dif+dif, x*dif),
    (y * dif + dif, x * dif +  dif), (y * dif, x * dif +  dif)], width = 5)
    pygame.display.flip()

# Check if the user pressed 'p' to pause the solver's animation
def check_pause():
    pause = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True

    while pause == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False

# Solve the sudoku puzzle and display the process of its backtracking algorithm
def solve(b, r, c, s):
    check_pause()

    (r,c) = find_zero(b)
    if (r == -1 and c == -1):
        draw_board(False)
        return True
    
    for i in range(1,10):
        global x, y
        x = r
        y = c
        if (check_move(r, c, b, i)):
            b[r][c] = i
            screen.fill("White")
            draw_board(False)
            highlight_box((0, 255, 0), x, y)
            pygame.time.delay(s)
            check_pause()
            if (solve(b, r, c + 1, s)):
                return True
        b[r][c] = 0
    highlight_box((255, 0, 0), x, y)
    pygame.time.delay(s)
    check_pause()
    return False

# Main code that takes user input to play or solve the sudoku puzzle       
while running:

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    val = 0
    flag1 = 0
    draw_board(run)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    solve(board, x, y, 0)
                    run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x-= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x+= 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y-= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y+= 1
                flag1 = 1   
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2   
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9 

    if flag1 == 1:
        highlight_box((255,229,180), y, x) 
    
    if (val != 0 and board[int(y)][int(x)] == 0):
        if valid(int(y), int(x), val):
            board[int(y)][int(x)] = val
            draw_board(False)
            highlight_box((0,255,0), y, x)
            pygame.time.delay(200)
            flag1 = 0
        else:
            board[int(y)][int(x)] = val
            draw_board(False)
            highlight_box((255,0,0), y, x)
            pygame.time.delay(200)
            board[int(y)][int(x)] = 0
        val = 0


    # flip() the display to put work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60) 

# Terminate pygame
pygame.quit()