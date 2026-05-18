import numpy as np
from constants import ROWS, COLS, EMPTY, HUMAN_PIECE, AI_PIECE


class Board:
    """Represents the Connect-4 game board and all related logic."""

    def __init__(self):
        # 0 = empty, 1 = human, 2 = AI
        self.grid = np.zeros((ROWS, COLS), dtype=int)

    def copy(self):
        # Copy board state for search
        new_board = Board()
        new_board.grid = self.grid.copy()
        return new_board

    def is_valid_column(self, col: int) -> bool:
        """A column is valid if the top cell is still empty."""
        return self.grid[0][col] == EMPTY

    def get_valid_columns(self) -> list:
        # Columns that can accept a piece
        return [c for c in range(COLS) if self.is_valid_column(c)]

    def get_next_open_row(self, col: int) -> int:
        """Returns the lowest empty row in a column (gravity)."""
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                return row
        return -1

    def is_full(self) -> bool:
        # No valid columns left
        return len(self.get_valid_columns()) == 0

    def drop_piece(self, row: int, col: int, piece: int):
        # Place a piece on the grid
        self.grid[row][col] = piece

    def remove_piece(self, row: int, col: int):
        """Used by Minimax to undo a move."""
        self.grid[row][col] = EMPTY

    def check_win(self, piece: int) -> bool:
        """Check all four directions for a four-in-a-row."""
        g = self.grid

        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(g[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(g[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(g[r + i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal up-right
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(g[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def get_winning_cells(self, piece: int):
        """Returns the list of (row, col) cells that form the winning four."""
        g = self.grid

        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                cells = [(r, c + i) for i in range(4)]
                if all(g[r][c + i] == piece for i in range(4)):
                    return cells

        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                cells = [(r + i, c) for i in range(4)]
                if all(g[r + i][c] == piece for i in range(4)):
                    return cells

        # Diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                cells = [(r + i, c + i) for i in range(4)]
                if all(g[r + i][c + i] == piece for i in range(4)):
                    return cells

        # Diagonal up-right
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                cells = [(r - i, c + i) for i in range(4)]
                if all(g[r - i][c + i] == piece for i in range(4)):
                    return cells

        return []

    def is_terminal(self) -> bool:
        # Game is over when win or full board
        return (self.check_win(HUMAN_PIECE) or
                self.check_win(AI_PIECE) or
                self.is_full())
