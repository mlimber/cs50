import pytest

import tictactoe as ttt

X = ttt.X
O = ttt.O
EMPTY = ttt.EMPTY


def test_player():
    board = ttt.initial_state()
    assert X == ttt.player(board)

    board[0][0] = X
    assert O == ttt.player(board)

    board[1][1] = O
    assert X == ttt.player(board)

    board[2][2] = X
    assert O == ttt.player(board)


def test_actions():
    def check(board, actions):
        for i in range(len(board)):
            for j in range(len(board[i])):
                is_action = (i, j) in actions
                if board[i][j] == EMPTY:
                    assert is_action
                else:
                    assert not is_action

    board = ttt.initial_state()

    actions = ttt.actions(board)
    assert len(actions) == 9
    check(board, actions)

    board[0][:] = X
    actions = ttt.actions(board)
    assert len(actions) == 6
    check(board, actions)

    board[1][1] = O
    board[2][2] = O
    actions = ttt.actions(board)
    assert len(actions) == 4
    check(board, actions)

    board[1][:] = O
    board[2][:] = X
    actions = ttt.actions(board)
    assert len(actions) == 0


def test_result():
    board = ttt.initial_state()
    board2 = ttt.result(board, (0, 0))
    assert X == board2[0][0]
    assert all([b == EMPTY for b in board2[0][1:]])
    assert all([b == EMPTY for b in board2[1][:]])
    assert all([b == EMPTY for b in board2[2][:]])

    board3 = ttt.result(board2, (1, 2))
    assert X == board3[0][0]
    assert O == board3[1][2]
    assert all([b == EMPTY for b in board3[0][1:]])
    assert all([b == EMPTY for b in board3[1][:2]])
    assert all([b == EMPTY for b in board3[2][:]])

    board4 = ttt.result(board3, (2, 1))
    assert X == board4[0][0]
    assert O == board4[1][2]
    assert X == board4[2][1]
    assert all([b == EMPTY for b in board4[0][1:]])
    assert all([b == EMPTY for b in board4[1][:2]])
    assert all([b == EMPTY for b in [board4[2][n] for n in [0, 2]]])


@pytest.mark.parametrize("i, j", [
    (1, 3),
    (3, 2),
    (-1, 1),
    (3, -3),
])
def test_result_index_errors(i, j):
    board = ttt.initial_state()
    with pytest.raises(IndexError):
        ttt.result(board, (i, j))


def test_result_already_set():
    board = ttt.initial_state()
    board = ttt.result(board, (1, 1))
    with pytest.raises(RuntimeError):
        ttt.result(board, (1, 1))


N = EMPTY  # shorthand


@pytest.mark.parametrize("board, winner, is_terminal, utility, name", [
    # --- No Winner / Ongoing ---
    ([[N, N, N],
      [N, N, N],
      [N, N, N]], N, False, 0, "Empty board"),

    ([[X, N, X],
      [N, O, N],
      [O, N, N]], N, False, 0, "Mid-game, no winner"),

    # --- Horizontal Wins ---
    ([[X, X, X],
      [N, O, N],
      [O, N, N]], X, True, 1, "Top row"),

    ([[O, O, N],
      [X, X, X],
      [N, N, O]], X, True, 1, "Middle row"),

    ([[N, N, O],
      [X, X, N],
      [O, O, O]], O, True, -1, "Bottom row"),

    # --- Vertical Wins ---
    ([[O, N, X],
      [O, N, N],
      [O, X, X]], O, True, -1, "Left column"),

    ([[N, X, N],
      [O, X, N],
      [N, X, O]], X, True, 1, "Middle column"),

    ([[N, N, O],
      [X, N, O],
      [X, X, O]], O, True, -1, "Right column"),

    # --- Diagonal Wins ---
    ([[X, O, N],
      [N, X, O],
      [N, N, X]], X, True, 1, "Main diagonal (top-left to bottom-right)"),

    ([[N, X, O],
      [N, O, X],
      [O, N, X]], O, True, -1, "Anti-diagonal (top-right to bottom-left)"),

    # --- Cat's Game (Draw) ---
    ([[X, O, X],
      [X, O, O],
      [O, X, X]], N, True, 0, "Full board with no winner"),

    ([[X, X, O],
      [O, O, X],
      [X, O, X]], N, True, 0, "Another variation of a draw"),
])
def test_endings(board, winner, is_terminal, utility, name):
    assert winner == ttt.winner(board), name
    assert is_terminal == ttt.terminal(board), name
    assert utility == ttt.utility(board)


@pytest.mark.parametrize("board", [
    [[N, X, O],  # Diagonal O wins
     [N, O, X],
     [O, N, X]],

    [[X, O, X],  # Cat's game
     [X, O, O],
     [O, X, X]],
])
def test_minimax_terminal(board):
    assert not ttt.minimax(board)


@pytest.mark.parametrize("board, expected_actions, name", [
    # --- Empty / Early Game ---
    # Accept ANY of the 9 squares, because they all lead to a Draw (0)
    ([[N, N, N],
      [N, N, N],
      [N, N, N]], set((i, j) for i in range(3) for j in range(3)), "Any opening move results in a draw"),

    ([[N, N, N],
      [N, X, N],
      [N, N, N]], {(0, 0), (0, 2), (2, 0), (2, 2)}, "X in center - O should take corner"),

    # --- Block Opponent Win ---
    ([[X, X, N],
      [O, N, N],
      [N, N, N]], {(0, 2)}, "X about to win top row - O must block"),

    ([[X, N, N],
      [N, X, N],
      [O, N, N]], {(2, 2)}, "X about to win diagonal - O must block"),

    ([[O, N, X],
      [N, O, N],
      [N, N, N]], {(2, 2)}, "O about to win anti-diagonal - X must block"),

    ([[X, N, N],
      [X, O, N],
      [N, N, N]], {(2, 0)}, "X about to win left column - O must block"),

    # --- Take Winning Move ---
    ([[X, X, N],
      [O, O, N],
      [N, N, N]], {(0, 2)}, "X can win top row - should take it"),

    ([[O, X, X],
      [N, O, N],
      [N, N, N]], {(2, 2)}, "O can win diagonal - should take it"),

    # X has two in the left column, (2, 0) is empty
    ([[X, O, N],
      [X, N, N],
      [N, O, N]], {(2, 0)}, "X can win left column - should take it"),

    # --- Fork / Strategic ---
    ([[X, O, X],
      [N, N, N],
      [O, N, N]], {(1, 1), (1, 2), (2, 1), (2, 2)}, "X must pick a move that maintains the Draw"),

    ([[O, N, X],
      [N, X, N],
      [N, N, N]], {(2, 0)}, "O must block X diagonal and prevent fork"),
])
def test_minimax(board, expected_actions, name):
    action = ttt.minimax(board)
    assert action in expected_actions, f"{name}: got {action}, expected one of {expected_actions}"
