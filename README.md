# Connect4 AI

A Python Connect 4 game with a minimax AI opponent and a Pygame GUI.

## Features

- Human vs AI gameplay
- Minimax with alpha-beta pruning
- Smooth drop animation and win highlighting

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
python main.py
```

## Controls

- Mouse move: choose column
- Mouse click: drop piece
- R: restart
- Esc: quit

## Project Structure

- ai.py: minimax AI and board evaluation
- board.py: game rules and board state
- gui.py: rendering and animation
- main.py: game loop
- constants.py: configuration values

## Notes

If you want to tweak difficulty, adjust `AI_DEPTH` in constants.py.
