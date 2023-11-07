import os
import time

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

# kiểm tra node lá
def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

# kiểm tra win game hay không
def is_winner(board, player):
    for row in board: # kiểm tra hàng
        if all(cell == player for cell in row):
            return True

    for col in range(3): # kiểm tra cột
        if all(board[row][col] == player for row in range(3)):
            return True

    # kiểm tra 2 đường chéo
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Hàm evaluate sử dụng hàm f như đã yêu cầu
def evaluate(board):
    def f(player):
        num_rows = num_cols = num_diag = 0
        opponent = 'X' if player == 'O' else 'O'

        for i in range(3):
            if all(cell == player for cell in board[i]):
                num_rows += 1
            if all(board[row][i] == player for row in range(3)):
                num_cols += 1
            if board[i][i] == player:
                num_diag += 1
            if board[i][2 - i] == player:
                num_diag += 1

        for i in range(3):
            if all(cell == opponent for cell in board[i]):
                num_rows -= 1
            if all(board[row][i] == opponent for row in range(3)):
                num_cols -= 1
            if board[i][i] == opponent:
                num_diag -= 1
            if board[i][2 - i] == opponent:
                num_diag -= 1

        return (num_rows, num_cols, num_diag)

    max_val = f('O')
    min_val = f('X')
    return (max_val[0] - min_val[0], max_val[1] - min_val[1], max_val[2] - min_val[2)

# Hàm minimax với cắt tỉa alpha-beta
def minimax(board, max_depth, alpha, beta, maximizing_player=True):
    if is_winner(board, 'O'):
        return 1
    if is_winner(board, 'X'):
        return -1
    if is_board_full(board):
        return 0
    if max_depth == 0:
        return sum(evaluate(board))
    
    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, max_depth - 1, alpha, beta, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, max_depth - 1, alpha, beta, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Tìm vị trí đi tốt nhất cho computer (MIN)
def best_move(board, max_depth):
    best_val = float('inf')
    alpha = float('inf')
    beta = float('-inf')

    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, max_depth, alpha, beta, True)
                board[i][j] = ' '
                if move_val < best_val or move is None:
                    best_val = move_val
                    move = (i, j)

    return move

# Main game loop
# Player user 'X'
# Computer user 'O'

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_turn = True  # True for player X, False for player O

    print("Welcome to Tic Tac Toe!")
    total_time = 0.0
    res = None
    while not res:
        os.system('clear')
        print_board(board)
        if player_turn:
            row, col = map(int, input("Enter your move (row and column): ").split())
            if board[row][col] == ' ':
                board[row][col] = 'X'
            else:
                print("Invalid move. Try again.")
                continue
        else:
            start = time.time()
            row, col = best_move(board, 10)
            end = time.time()
            total_time += end - start
            board[row][col] = 'O'

        if is_winner(board, 'X'):
            res = "Player X wins!"
        elif is_winner(board, 'O'):
            res = "Player O wins!"
        elif is_board_full(board):
            res = "It's a tie!"

        player_turn = not player_turn
    os.system('clear')
    print_board(board)
    print("Process time: ", total_time)
    print(res)

# Chạy game
main()
