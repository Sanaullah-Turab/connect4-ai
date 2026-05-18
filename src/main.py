import sys
import math
import pygame

from constants import HUMAN_PIECE, AI_PIECE, EMPTY
from board    import Board
from ai       import get_ai_move
from gui      import GUI

# Game state labels
STATE_HUMAN_TURN  = "human"
STATE_AI_THINKING = "ai_thinking"
STATE_ANIMATING   = "animating"
STATE_GAME_OVER   = "game_over"


def new_game():
    """Return fresh board and initial state."""
    return Board(), STATE_HUMAN_TURN, HUMAN_PIECE, EMPTY, [], None, None


def run():
    board, state, current_piece, winner, winning_cells, pending_row, pending_col = new_game()

    gui = GUI()

    while True:
        # Input handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gui.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gui.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    board, state, current_piece, winner, winning_cells, pending_row, pending_col = new_game()
                    gui.anim_active = False
                    gui.hover_col   = -1

            if event.type == pygame.MOUSEMOTION and state == STATE_HUMAN_TURN:
                col = gui.get_col_from_mouse(event.pos[0])
                gui.set_hover(col if 0 <= col < 7 else -1)

            if (event.type == pygame.MOUSEBUTTONDOWN and
                    state == STATE_HUMAN_TURN):
                col = gui.get_col_from_mouse(event.pos[0])

                if 0 <= col < 7 and board.is_valid_column(col):
                    row = board.get_next_open_row(col)
                    pending_row, pending_col = row, col
                    gui.start_drop_animation(col, row, HUMAN_PIECE)
                    state     = STATE_ANIMATING
                    gui.set_hover(-1)

        # Animation step
        if state == STATE_ANIMATING:
            done = gui.update_animation()
            if done:
                board.drop_piece(pending_row, pending_col, current_piece)

                if board.check_win(current_piece):
                    winning_cells = board.get_winning_cells(current_piece)
                    winner = current_piece
                    state         = STATE_GAME_OVER

                elif board.is_full():
                    winner = EMPTY
                    state  = STATE_GAME_OVER

                else:
                    # Switch turns
                    current_piece = AI_PIECE if current_piece == HUMAN_PIECE \
                                             else HUMAN_PIECE
                    state = STATE_AI_THINKING if current_piece == AI_PIECE \
                                              else STATE_HUMAN_TURN

        elif state == STATE_AI_THINKING:
            # Let the UI show the thinking state before computing
            gui.draw(board, current_piece, False, EMPTY, [])
            gui.tick()

            ai_col = get_ai_move(board)
            ai_row = board.get_next_open_row(ai_col)

            pending_row, pending_col = ai_row, ai_col
            gui.start_drop_animation(ai_col, ai_row, AI_PIECE)
            state = STATE_ANIMATING

        # Render
        game_over = (state == STATE_GAME_OVER)
        gui.draw(board, current_piece,
                 game_over=game_over,
                 winner=winner,
                 winning_cells=winning_cells)

        gui.tick()
if __name__ == "__main__":
    run()
