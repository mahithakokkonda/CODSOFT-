import tkinter as tk
from tkinter import messagebox
import math

# Initialize the game board
def initialize_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Check for a winner
def check_winner(board, player):
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check if the game is a draw
def is_draw(board):
    return all([cell != ' ' for row in board for cell in row])

# Minimax algorithm to find the best move
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# Find the best move for the AI
def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Update the button text and make a move
def make_move(row, col):
    if board[row][col] == ' ' and not game_over:
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state="disabled", disabledforeground="blue")
        if check_winner(board, 'X'):
            end_game("You win!")
            return
        if is_draw(board):
            end_game("It's a draw!")
            return

        ai_move = best_move(board)
        board[ai_move[0]][ai_move[1]] = 'O'
        buttons[ai_move[0]][ai_move[1]].config(text='O', state="disabled", disabledforeground="red")
        if check_winner(board, 'O'):
            end_game("AI wins!")
        elif is_draw(board):
            end_game("It's a draw!")

# End the game
def end_game(message):
    global game_over
    game_over = True
    messagebox.showinfo("Game Over", message)
    root.after(2000, reset_board)

# Reset the game board
def reset_board():
    global board, game_over
    board = initialize_board()
    game_over = False
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', state="normal")

# GUI setup
root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = [[None for _ in range(3)] for _ in range(3)]
board = initialize_board()
game_over = False

for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text='', font=('Arial', 40), width=5, height=2,
                                      command=lambda r=row, c=col: make_move(r, c))
        buttons[row][col].grid(row=row, column=col)

# Start the GUI loop
root.mainloop()
