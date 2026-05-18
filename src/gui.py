import pygame
import math
from constants import (
    ROWS, COLS, CELL_SIZE, RADIUS, WIDTH, HEIGHT,
    BG_COLOR, BOARD_COLOR, CELL_BORDER, EMPTY_COLOR,
    HUMAN_COLOR, HUMAN_GLOW, AI_COLOR, AI_GLOW,
    TEXT_COLOR, ACCENT_COLOR, WIN_BG, SHADOW,
    HUMAN_PIECE, AI_PIECE, EMPTY, DROP_SPEED, FPS
)


def _piece_color(piece: int):
    return HUMAN_COLOR if piece == HUMAN_PIECE else AI_COLOR


def _piece_glow(piece: int):
    return HUMAN_GLOW if piece == HUMAN_PIECE else AI_GLOW


class GUI:
    """Handles all drawing and animation — separated from game logic."""

    def __init__(self):
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect-4  ·  Human vs AI")
        self.clock  = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.SysFont("consolas", 42, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 28)
        self.font_small = pygame.font.SysFont("consolas", 20)

        # Animation state
        self.anim_active  = False
        self.anim_piece   = EMPTY
        self.anim_col     = 0
        self.anim_target_row = 0
        self.anim_y       = 0.0
        self.anim_target_y = 0.0

        # Hover state
        self.hover_col    = -1

    def _draw_circle_glow(self, surface, color, glow_color, cx, cy, radius):
        """Draw a circle with a soft glow ring."""
        glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*glow_color, 60),
                           (radius * 2, radius * 2), radius + 6)
        surface.blit(glow_surf, (cx - radius * 2, cy - radius * 2))
        pygame.draw.circle(surface, color, (cx, cy), radius)
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

    def _menu_layout(self):
        title_y = int(HEIGHT * 0.2)
        button_width = min(520, WIDTH - 80)
        button_height = 64
        gap = 18
        start_y = int(HEIGHT * 0.42)
        x = (WIDTH - button_width) // 2

        buttons = []
        for i in range(3):
            y = start_y + i * (button_height + gap)
            buttons.append(pygame.Rect(x, y, button_width, button_height))

        return title_y, buttons

    def _draw_menu_button(self, rect, label, hovered: bool):
        shadow_rect = rect.move(0, 6)
        shadow = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=14)
        self.screen.blit(shadow, shadow_rect.topleft)

        if hovered:
            glow = pygame.Surface((rect.width + 30, rect.height + 30), pygame.SRCALPHA)
            glow_rect = glow.get_rect()
            for i, alpha in enumerate((80, 50, 25)):
                inset = 6 * i
                pygame.draw.rect(
                    glow,
                    (*ACCENT_COLOR, alpha),
                    glow_rect.inflate(-inset * 2, -inset * 2),
                    border_radius=16,
                )
            self.screen.blit(glow, (rect.x - 15, rect.y - 15))

        pygame.draw.rect(self.screen, WIN_BG, rect, border_radius=12)
        border_color = ACCENT_COLOR if hovered else CELL_BORDER
        pygame.draw.rect(self.screen, border_color, rect, width=2, border_radius=12)

        text_color = ACCENT_COLOR if hovered else TEXT_COLOR
        text_surf = self.font_medium.render(label, True, text_color)
        self.screen.blit(
            text_surf,
            (rect.centerx - text_surf.get_width() // 2,
             rect.centery - text_surf.get_height() // 2),
        )

    def draw_menu(self, mouse_pos):
        self.screen.fill(BG_COLOR)

        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*ACCENT_COLOR, 60), (int(WIDTH * 0.2), int(HEIGHT * 0.2)), int(WIDTH * 0.45))
        pygame.draw.circle(glow, (*ACCENT_COLOR, 40), (int(WIDTH * 0.85), int(HEIGHT * 0.15)), int(WIDTH * 0.35))
        self.screen.blit(glow, (0, 0))

        title_y, buttons = self._menu_layout()
        title = self.font_large.render("CONNECT-4 AI", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, title_y))

        subtitle = self.font_small.render("Select difficulty", True, ACCENT_COLOR)
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_y + 48))

        labels = [
            "Play vs AI - Standard",
            "Play vs AI - Hard",
            "Quit",
        ]

        for i, rect in enumerate(buttons):
            hovered = rect.collidepoint(mouse_pos)
            self._draw_menu_button(rect, labels[i], hovered)

        pygame.display.flip()

    def get_menu_action(self, mouse_pos) -> int:
        _, buttons = self._menu_layout()
        for i, rect in enumerate(buttons):
            if rect.collidepoint(mouse_pos):
                return i
        return -1

    def draw(self, board, current_piece: int,
             game_over: bool = False, winner: int = EMPTY,
             winning_cells: list = None):

        # Background
        self.screen.fill(BG_COLOR)

        # Top preview row
        self._draw_preview_bar(current_piece, game_over)

        # Board and pieces
        board_rect = pygame.Rect(0, self._board_top(), WIDTH, ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect, border_radius=12)

        for r in range(ROWS):
            for c in range(COLS):
                cx, cy = self._cell_center(r, c)
                pygame.draw.circle(self.screen, CELL_BORDER, (cx, cy), RADIUS + 4)
                piece = board.grid[r][c]
                if piece == EMPTY:
                    pygame.draw.circle(self.screen, EMPTY_COLOR, (cx, cy), RADIUS)
                else:
                    color = _piece_color(piece)
                    glow  = _piece_glow(piece)
                    if winning_cells and (r, c) in winning_cells:
                        pygame.draw.circle(self.screen, glow, (cx, cy), RADIUS + 8)
                        pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), RADIUS // 3)
                    self._draw_circle_glow(self.screen, color, glow, cx, cy, RADIUS)

        if self.anim_active:
            # Falling piece
            cx = self.anim_col * CELL_SIZE + CELL_SIZE // 2
            cy = int(self.anim_y)
            color = _piece_color(self.anim_piece)
            glow  = _piece_glow(self.anim_piece)
            self._draw_circle_glow(self.screen, color, glow, cx, cy, RADIUS)

        if game_over:
            # End-game banner
            self._draw_winner_banner(winner)

        pygame.display.flip()

    def _draw_preview_bar(self, current_piece: int, game_over: bool):
        """Top row: hover ghost piece + turn label."""
        bar_rect = pygame.Rect(0, 0, WIDTH, CELL_SIZE)
        pygame.draw.rect(self.screen, BG_COLOR, bar_rect)

        if game_over:
            return

        if current_piece == HUMAN_PIECE:
            label = "YOUR TURN"
            color = HUMAN_COLOR
        else:
            label = "AI THINKING..."
            color = AI_COLOR

        surf = self.font_small.render(label, True, color)
        self.screen.blit(surf, (WIDTH - surf.get_width() - 16,
                                CELL_SIZE // 2 - surf.get_height() // 2))

        if self.hover_col >= 0 and not self.anim_active and current_piece == HUMAN_PIECE:
            # Hover ghost piece
            cx = self.hover_col * CELL_SIZE + CELL_SIZE // 2
            cy = CELL_SIZE // 2
            color = _piece_color(current_piece)
            ghost = pygame.Surface((RADIUS * 2 + 20, RADIUS * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(ghost, (*color, 130),
                               (RADIUS + 10, RADIUS + 10), RADIUS)
            self.screen.blit(ghost, (cx - RADIUS - 10, cy - RADIUS - 10))

    def _draw_winner_banner(self, winner: int):
        """Semi-transparent overlay with winner message."""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

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

    def start_drop_animation(self, col: int, row: int, piece: int):
        """Begin the falling-piece animation."""
        # Initialize animation values
        self.anim_active   = True
        self.anim_piece    = piece
        self.anim_col      = col
        self.anim_target_row = row
        self.anim_y        = float(CELL_SIZE // 2)
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
            return True

        return False

    def get_col_from_mouse(self, x: int) -> int:
        return x // CELL_SIZE

    def set_hover(self, col: int):
        self.hover_col = col

    def tick(self):
        self.clock.tick(FPS)

    def quit(self):
        pygame.quit()
