# ─────────────────────────────────────────────
#  gui.py  –  All Pygame rendering & animation
#  No game logic or AI decisions here
# ─────────────────────────────────────────────

import pygame
import math
from constants import (
    ROWS, COLS, CELL_SIZE, RADIUS, WIDTH, HEIGHT,
    BG_COLOR, BOARD_COLOR, CELL_BORDER, EMPTY_COLOR,
    HUMAN_COLOR, HUMAN_GLOW, AI_COLOR, AI_GLOW,
    TEXT_COLOR, ACCENT_COLOR, WIN_BG,
    HUMAN_PIECE, AI_PIECE, EMPTY, DROP_SPEED, FPS
)


def _piece_color(piece: int):
    return HUMAN_COLOR if piece == HUMAN_PIECE else AI_COLOR


def _piece_glow(piece: int):
    return HUMAN_GLOW if piece == HUMAN_PIECE else AI_GLOW


class GUI:
    """Handles all drawing and animation — separated from game logic."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect-4  ·  Human vs AI")
        self.clock  = pygame.time.Clock()

        # Fonts
        self.font_large  = pygame.font.SysFont("consolas", 42, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 28)
        self.font_small  = pygame.font.SysFont("consolas", 20)

        # Animation state
        self.anim_active  = False
        self.anim_piece   = EMPTY
        self.anim_col     = 0
        self.anim_target_row = 0
        self.anim_y       = 0.0        # current pixel y (top of board area)
        self.anim_target_y = 0.0

        # Hover state
        self.hover_col    = -1

    # ══════════════════════════════════════════
    #  Drawing helpers
    # ══════════════════════════════════════════

    def _draw_circle_glow(self, surface, color, glow_color, cx, cy, radius):
        """Draw a circle with a soft glow ring."""
        # Outer glow (slightly larger, translucent)
        glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*glow_color, 60),
                           (radius * 2, radius * 2), radius + 6)
        surface.blit(glow_surf, (cx - radius * 2, cy - radius * 2))
        # Main circle
        pygame.draw.circle(surface, color, (cx, cy), radius)
        # Inner highlight (top-left arc for 3-D feel)
        pygame.draw.circle(surface, tuple(min(c + 60, 255) for c in color),
                           (cx - radius // 5, cy - radius // 5),
                           radius // 4)

    def _board_top(self):
        """Pixel y of the first board row (below the preview area)."""
        return CELL_SIZE

    def _cell_center(self, row, col):
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = self._board_top() + row * CELL_SIZE + CELL_SIZE // 2
        return cx, cy

    # ══════════════════════════════════════════
    #  Main draw routine
    # ══════════════════════════════════════════

    def draw(self, board, current_piece: int,
             game_over: bool = False, winner: int = EMPTY,
             winning_cells: list = None):

        self.screen.fill(BG_COLOR)

        # ── Top preview bar ───────────────────
        self._draw_preview_bar(current_piece, game_over)

        # ── Board background ──────────────────
        board_rect = pygame.Rect(0, self._board_top(), WIDTH, ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect, border_radius=12)

        # ── Grid cells ────────────────────────
        for r in range(ROWS):
            for c in range(COLS):
                cx, cy = self._cell_center(r, c)
                # Cell border
                pygame.draw.circle(self.screen, CELL_BORDER, (cx, cy), RADIUS + 4)
                piece = board.grid[r][c]
                if piece == EMPTY:
                    pygame.draw.circle(self.screen, EMPTY_COLOR, (cx, cy), RADIUS)
                else:
                    color = _piece_color(piece)
                    glow  = _piece_glow(piece)
                    # Highlight winning cells
                    if winning_cells and (r, c) in winning_cells:
                        pygame.draw.circle(self.screen, glow, (cx, cy), RADIUS + 8)
                        # Pulsing white core
                        pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), RADIUS // 3)
                    self._draw_circle_glow(self.screen, color, glow, cx, cy, RADIUS)

        # ── Falling piece animation ───────────
        if self.anim_active:
            cx = self.anim_col * CELL_SIZE + CELL_SIZE // 2
            cy = int(self.anim_y)
            color = _piece_color(self.anim_piece)
            glow  = _piece_glow(self.anim_piece)
            self._draw_circle_glow(self.screen, color, glow, cx, cy, RADIUS)

        # ── Winner banner ─────────────────────
        if game_over:
            self._draw_winner_banner(winner)

        pygame.display.flip()

    # ══════════════════════════════════════════
    #  Sub-components
    # ══════════════════════════════════════════

    def _draw_preview_bar(self, current_piece: int, game_over: bool):
        """Top row: hover ghost piece + turn label."""
        bar_rect = pygame.Rect(0, 0, WIDTH, CELL_SIZE)
        pygame.draw.rect(self.screen, BG_COLOR, bar_rect)

        if game_over:
            return

        # Turn label (right side)
        if current_piece == HUMAN_PIECE:
            label = "YOUR TURN"
            color = HUMAN_COLOR
        else:
            label = "AI THINKING..."
            color = AI_COLOR

        surf = self.font_small.render(label, True, color)
        self.screen.blit(surf, (WIDTH - surf.get_width() - 16,
                                CELL_SIZE // 2 - surf.get_height() // 2))

        # Hover ghost piece
        if self.hover_col >= 0 and not self.anim_active and current_piece == HUMAN_PIECE:
            cx = self.hover_col * CELL_SIZE + CELL_SIZE // 2
            cy = CELL_SIZE // 2
            color = _piece_color(current_piece)
            # Transparent ghost
            ghost = pygame.Surface((RADIUS * 2 + 20, RADIUS * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(ghost, (*color, 130),
                               (RADIUS + 10, RADIUS + 10), RADIUS)
            self.screen.blit(ghost, (cx - RADIUS - 10, cy - RADIUS - 10))

    def _draw_winner_banner(self, winner: int):
        """Semi-transparent overlay with winner message."""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Banner box
        bw, bh = 480, 160
        bx, by = (WIDTH - bw) // 2, (HEIGHT - bh) // 2
        pygame.draw.rect(self.screen, WIN_BG,
                         (bx, by, bw, bh), border_radius=20)

        if winner == HUMAN_PIECE:
            msg   = "YOU WIN!"
            color = HUMAN_COLOR
        elif winner == AI_PIECE:
            msg   = "AI WINS!"
            color = AI_COLOR
        else:
            msg   = "IT'S A DRAW!"
            color = ACCENT_COLOR

        # Glow border
        pygame.draw.rect(self.screen, color,
                         (bx, by, bw, bh), width=3, border_radius=20)

        text_surf = self.font_large.render(msg, True, color)
        self.screen.blit(text_surf,
                         (bx + (bw - text_surf.get_width()) // 2,
                          by + 30))

        sub = self.font_small.render("Press  R  to restart  |  ESC  to quit",
                                     True, TEXT_COLOR)
        self.screen.blit(sub, (bx + (bw - sub.get_width()) // 2,
                               by + 100))

    # ══════════════════════════════════════════
    #  Animation
    # ══════════════════════════════════════════

    def start_drop_animation(self, col: int, row: int, piece: int):
        """Begin the falling-piece animation."""
        self.anim_active   = True
        self.anim_piece    = piece
        self.anim_col      = col
        self.anim_target_row = row
        self.anim_y        = float(CELL_SIZE // 2)   # start at top of board
        _, self.anim_target_y = self._cell_center(row, col)

    def update_animation(self) -> bool:
        """
        Advance the drop animation one frame.
        Returns True when animation is complete.
        """
        if not self.anim_active:
            return True

        self.anim_y += DROP_SPEED
        if self.anim_y >= self.anim_target_y:
            self.anim_y      = self.anim_target_y
            self.anim_active = False
            return True   # finished

        return False      # still falling

    # ══════════════════════════════════════════
    #  Utility
    # ══════════════════════════════════════════

    def get_col_from_mouse(self, x: int) -> int:
        return x // CELL_SIZE

    def set_hover(self, col: int):
        self.hover_col = col

    def tick(self):
        self.clock.tick(FPS)

    def quit(self):
        pygame.quit()
