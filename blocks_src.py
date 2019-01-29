import random
from copy import deepcopy
import functools

def pick_random_move(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)

    if board[row][column] != None:
        return pick_random_move(board)

    return [row, column]

def findEmptyCells(board):
    empty_cells = []  # count_freeSpace or depth
    for rowLoop in range(len(board)):
        for columnLoop in range(len(board[rowLoop])):
            if board[rowLoop][columnLoop] == ' ':
                empty_cells.append((rowLoop, columnLoop))
    return empty_cells

def game_turn(turn):

    assert type(turn) == str

    if turn == "X":
        return "O"
    else:
        return "X"


def get_opponent(player):
    """Returns the opposite sign playes by the current agent"""
    if player == 'X':
        return 'O'
    return 'X'

def check_winner(board):
    # check for matches and winner
    winner = None
    for j in range(len(board)):
        # check rows matches
        if board[j][0] == "X":
            if (board[j][1] == "X") and (board[j][2] == "X"):
                winner = "X"
        if board[j][0] == "O":
            if (board[j][1] == "O") and (board[j][2] == "O"):
                winner = "O"

        # Check columns matches
        if board[0][j] == "X":
            if (board[1][j] == "X") and (board[2][j] == "X"):
                winner = "X"

        if board[0][j] == "O":
            if (board[1][j] == "O") and (board[2][j] == "O"):
                winner =  "O"

        # Check Left Diagonal matches
        if board[0][0] == "X":
            if (board[1][1] == "X") and (board[2][2] == "X"):
                winner = "X"
        if board[0][0] == "O":
            if (board[1][1] == "O") and (board[2][2] == "O"):
                winner = "O"

        # Check Right Diagonal matches
        if board[0][2] == "X":
            if (board[1][1] == "X") and (board[2][0] == "X"):
                winner = "X"
        if board[0][2] == "O":
            if (board[1][1] == "O") and (board[2][0] == "O"):
                winner = "O"

    return winner

def minimax2(board, turn):
    # if game is over:
    #     return score
    moves = findEmptyCells(board)
    if turn == "X":
        value = -99999999
        for move in moves:
            value = max(value, minimax2(board, "0"))
    else:
        value = 999999999
        for move in moves:
            value = min(value, minimax2(board, "X"))

    return value
    pass


def minimax(game, turn, coords=None):
    if check_winner(game) == "X":
        return 1, coords
    elif check_winner(game) == "O":
        return -1, coords

    moves = []
    for i in range(3):
        for j in range(3):
            if game[i][j] is None:
                moves.append((i, j))
    # Draw
    if moves == []:
        return 0, coords

    if turn == "X":
        score = -100, coords
        for move in moves:
            new_game = game.copy()
            new_game[move[0]][move[1]] = "X"
            new_score = minimax(new_game, "O", move)
            if new_score[0] > score[0]:
                score = new_score
        return score

    if turn == "O":
        score = 100, coords
        for move in moves:
            new_game = game.copy()
            new_game[move[0]][move[1]] = "O"
            new_score = minimax(new_game, "X", move)
            if new_score[0] < score[0]:
                score = new_score
        return score


