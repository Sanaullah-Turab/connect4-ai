ROWS        = 6
COLS        = 7

AI_DEPTH    = 5
AI_PIECE    = 2
HUMAN_PIECE = 1
EMPTY       = 0

CELL_SIZE   = 100
RADIUS      = CELL_SIZE // 2 - 8
WIDTH       = COLS * CELL_SIZE
HEIGHT      = (ROWS + 1) * CELL_SIZE
WINDOW_SIZE = (WIDTH, HEIGHT)

BG_COLOR        = (13,  17,  23)
BOARD_COLOR     = (22,  33,  62)
CELL_BORDER     = (30,  45,  80)
EMPTY_COLOR     = (10,  14,  20)

HUMAN_COLOR     = (255, 75,  75)
HUMAN_GLOW      = (255, 120, 120)

AI_COLOR        = (255, 210, 50)
AI_GLOW         = (255, 230, 120)

TEXT_COLOR      = (220, 230, 255)
ACCENT_COLOR    = (100, 180, 255)
WIN_BG          = (20,  25,  40)
SHADOW          = (0,   0,   0,  120)

FPS = 60

DROP_SPEED = 18

SCORE_FOUR    =  100_000
SCORE_THREE   =       50
SCORE_TWO     =       10
SCORE_CENTER  =        3
BLOCK_THREE   =      -80
BLOCK_TWO     =       -5
