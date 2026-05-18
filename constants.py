# ─────────────────────────────────────────────
#  constants.py  –  All magic numbers live here
# ─────────────────────────────────────────────

# Board dimensions
ROWS        = 6
COLS        = 7

# Minimax config
AI_DEPTH    = 5          # Search depth (5 = strong but fast)
AI_PIECE    = 2
HUMAN_PIECE = 1
EMPTY       = 0

# Window / cell sizing
CELL_SIZE   = 100
RADIUS      = CELL_SIZE // 2 - 8
WIDTH       = COLS * CELL_SIZE
HEIGHT      = (ROWS + 1) * CELL_SIZE   # +1 row for the hover preview area
WINDOW_SIZE = (WIDTH, HEIGHT)

# ── Dark-theme palette ──────────────────────
BG_COLOR        = (13,  17,  23)    # near-black background
BOARD_COLOR     = (22,  33,  62)    # deep navy board
CELL_BORDER     = (30,  45,  80)    # subtle cell border
EMPTY_COLOR     = (10,  14,  20)    # hole (empty cell)

HUMAN_COLOR     = (255, 75,  75)    # vivid red  – human
HUMAN_GLOW      = (255, 120, 120)   # highlight ring

AI_COLOR        = (255, 210, 50)    # vivid yellow – AI
AI_GLOW         = (255, 230, 120)   # highlight ring

TEXT_COLOR      = (220, 230, 255)   # soft white-blue
ACCENT_COLOR    = (100, 180, 255)   # neon blue accent
WIN_BG          = (20,  25,  40)    # winner banner bg
SHADOW          = (0,   0,   0,  120)

# Frames-per-second
FPS = 60

# Drop animation speed (pixels per frame)
DROP_SPEED = 18

# Heuristic window scores
SCORE_FOUR    =  100_000
SCORE_THREE   =       50
SCORE_TWO     =       10
SCORE_CENTER  =        3
BLOCK_THREE   =      -80
BLOCK_TWO     =       -5
