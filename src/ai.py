import math
from constants import (
    ROWS, COLS, EMPTY, AI_PIECE, HUMAN_PIECE, AI_DEPTH,
    SCORE_FOUR, SCORE_THREE, SCORE_TWO, SCORE_CENTER,
    BLOCK_THREE, BLOCK_TWO
)

def _score_window(window: list, piece: int) -> int:
    """
    Evaluate a window of 4 cells and return a score for `piece`.

    Scoring logic:
      +100,000  → 4 in a row (win)
      +50       → 3 of ours + 1 empty
      +10       → 2 of ours + 2 empty
      -80       → opponent has 3 + 1 empty (urgent block)
      -5        → opponent has 2 + 2 empty
    """
    opponent = HUMAN_PIECE if piece == AI_PIECE else AI_PIECE

    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opponent)

    score = 0

    # Score our patterns
    if piece_count == 4:
        score += SCORE_FOUR
    elif piece_count == 3 and empty_count == 1:
        score += SCORE_THREE
    elif piece_count == 2 and empty_count == 2:
        score += SCORE_TWO

    # Penalize opponent threats
    if opp_count == 3 and empty_count == 1:
        score += BLOCK_THREE
    elif opp_count == 2 and empty_count == 2:
        score += BLOCK_TWO

    return score


def evaluate_board(board, piece: int) -> int:
    """
    Full board heuristic: sum scores from all horizontal, vertical,
    and diagonal windows of size 4, plus center column preference.
    """
    grid = board.grid
    score = 0

    # Center column preference
    center = [grid[r][COLS // 2] for r in range(ROWS)]
    score += center.count(piece) * SCORE_CENTER

    # Horizontal windows
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [grid[r][c + i] for i in range(4)]
            score += _score_window(window, piece)

    # Vertical windows
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [grid[r + i][c] for i in range(4)]
            score += _score_window(window, piece)

    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [grid[r + i][c + i] for i in range(4)]
            score += _score_window(window, piece)

    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [grid[r - i][c + i] for i in range(4)]
            score += _score_window(window, piece)

    return score

def minimax(board, depth: int, alpha: float, beta: float, is_max: bool) -> tuple:
    """
    Minimax algorithm with Alpha-Beta Pruning.

    Parameters
    ----------
    board       : Board  – current game state (we work on copies)
    depth       : int    – remaining search depth
    alpha       : float  – best already-explored option for maximizer
    beta        : float  – best already-explored option for minimizer
    maximizing  : bool   – True when it's AI's turn

    Returns
    -------
    (best_col, best_score) : tuple
      best_col is None at terminal/leaf nodes.
    """
    valid_cols = board.get_valid_columns()
    is_terminal = board.is_terminal()

    # Terminal and depth limits
    if is_terminal:
        if board.check_win(AI_PIECE):
            return (None,  math.inf)
        elif board.check_win(HUMAN_PIECE):
            return (None, -math.inf)
        else:
            return (None, 0)

    if depth == 0:
        return (None, evaluate_board(board, AI_PIECE))

    # Try center columns first to improve pruning
    ordered_cols = sorted(valid_cols, key=lambda c: -abs(c - COLS // 2) * -1)

    # Maximizing player (AI)
    if is_max:
        best_score = -math.inf
        best_col   = valid_cols[0]

        for col in ordered_cols:
            row = board.get_next_open_row(col)
            temp_board = board.copy()
            temp_board.drop_piece(row, col, AI_PIECE)

            _, score = minimax(temp_board, depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_col   = col

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return (best_col, best_score)

    # Minimizing player (human)
    else:
        best_score = math.inf
        best_col   = valid_cols[0]

        for col in ordered_cols:
            row = board.get_next_open_row(col)
            temp_board = board.copy()
            temp_board.drop_piece(row, col, HUMAN_PIECE)

            _, score = minimax(temp_board, depth - 1, alpha, beta, True)

            if score < best_score:
                best_score = score
                best_col   = col

            beta = min(beta, best_score)
            if alpha >= beta:
                break

        return (best_col, best_score)


def get_ai_move(board, search_depth: int) -> int:
    """
    Public interface: returns the best column for the AI to play.
    Called from main.py — no AI internals leak outside this file.
    """
    # Use the selected depth for this session
    col, _ = minimax(board, search_depth, -math.inf, math.inf, True)
    # Fallback when no valid columns are found
    if col is None:
        valid = board.get_valid_columns()
        col = valid[0] if valid else 0
    return col
