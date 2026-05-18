# Connect4 AI

A Python Connect 4 game with a minimax AI opponent, a cinematic Pygame GUI, and session audio.

## Features

- Human vs AI gameplay with a main menu
- Minimax with alpha-beta pruning and selectable difficulty
- Cinematic 3D-style pieces with gravity-based drops
- Session scoreboard across restarts
- Audio feedback for UI, drops, and game outcomes

## Requirements

- Python 3.10+
- Pygame and NumPy (see requirements.txt)

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

## Controls

- Mouse move: choose column
- Mouse click: drop piece
- R: restart
- Esc: quit

## Project Structure

- src/ai.py: minimax AI and board evaluation
- src/audio.py: audio loading and playback helpers
- src/board.py: game rules and board state
- src/gui.py: rendering and animation
- src/main.py: game loop
- src/constants.py: configuration values
- assets/: sound effects (ogg)

## Notes

If you want to tweak difficulty, adjust `AI_DEPTH` in src/constants.py.
If audio is missing, the game will run without sound and print a warning.
