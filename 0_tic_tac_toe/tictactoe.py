"""
Tic Tac Toe Player
"""

import copy
import sys
from typing import List, Optional, Set, Tuple

X = "X"
O = "O"
EMPTY = None

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

Action = Tuple[int, int]
Board = List[List[Optional[str]]]


def initial_state() -> Board:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: Board) -> str:
    """
    Returns player who has the next turn on acts board.
    """
    num_x = sum(row.count(X) for row in board)
    num_o = sum(row.count(O) for row in board)
    return X if num_x == num_o else O


def actions(board: Board) -> Set[Action]:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                acts.add((i, j))
    return acts


def result(board: Board, action: Action) -> Board:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    if (i < 0) or (i > 2) or (j < 0) or (j > 2):
        raise IndexError("Action out of bounds")
    if board[i][j] != EMPTY:
        raise RuntimeError(f"Invalid board change requested: {i}, {j}")
    board[i][j] = player(board)
    return board


def winner(board: Board) -> Optional[str]:
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] and all([board[i][j] == board[i][0] for j in range(1, 3)]):
            return board[i][0]
        if board[0][i] and all([board[j][i] == board[0][i] for j in range(1, 3)]):
            return board[0][i]
    if board[1][1] and (all([board[i][i] == board[1][1] for i in range(3)]) or
                        all([board[i][2 - i] == board[1][1] for i in range(3)])):
        return board[1][1]


def terminal(board: Board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    is_full = all([board[i][j] != EMPTY for i in range(3) for j in range(3)])
    return (winner(board) is not None) or is_full


def utility(board: Board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    champ = winner(board)
    return 1 if champ == X else -1 if champ == O else 0


class ValuedAction:
    def __init__(self, init_value: int, action: Optional[Action] = None):
        self.value = init_value
        self.action = action

    def __lt__(self, other: "ValuedAction"):
        return self.value < other.value

    def __gt__(self, other: "ValuedAction"):
        return self.value > other.value


def calc_score(board: Board, depth: int) -> int:
    DEPTH_OFFSET = 10  # max of 9 deep because 3x3, so go one more
    return utility(board) * (DEPTH_OFFSET - depth)


def max_value(board: Board, depth: int) -> ValuedAction:
    if terminal(board):
        return ValuedAction(calc_score(board, depth), None)
    choices = []
    for action in actions(board):
        value = min_value(result(board, action), depth + 1).value
        choices.append(ValuedAction(value, action))
    return max(choices)


def min_value(board: Board, depth: int) -> ValuedAction:
    if terminal(board):
        return ValuedAction(calc_score(board, depth), None)
    choices = []
    for action in actions(board):
        value = max_value(result(board, action), depth + 1).value
        choices.append(ValuedAction(value, action))
    return min(choices)


def minimax(board: Board) -> Optional[Action]:
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    find_best = max_value if player(board) == X else min_value
    return find_best(board, depth=0).action
