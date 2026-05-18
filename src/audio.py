import os
import pygame

_AUDIO_READY = False
_SOUNDS = {}


def _init_audio():
    global _AUDIO_READY
    if _AUDIO_READY:
        return

    try:
        pygame.mixer.init()
    except Exception as exc:
        print(f"Audio disabled: {exc}")
        return

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
    sound_files = {
        "game_draw": "game_draw.ogg",
        "gameover": "gameover.ogg",
        "game_win": "game_win.ogg",
        "piece_drop": "piece_drop.ogg",
        "piece_hit": "piece_hit.ogg",
        "ui_hover": "ui_hover.ogg",
        "ui_select": "ui_select.ogg",
    }

    for key, filename in sound_files.items():
        path = os.path.join(base_dir, filename)
        try:
            _SOUNDS[key] = pygame.mixer.Sound(path)
        except Exception:
            print(f"Warning: missing audio file {path}")

    if "ui_hover" in _SOUNDS:
        _SOUNDS["ui_hover"].set_volume(0.25)
    if "ui_select" in _SOUNDS:
        _SOUNDS["ui_select"].set_volume(0.45)
    if "piece_drop" in _SOUNDS:
        _SOUNDS["piece_drop"].set_volume(0.45)
    if "piece_hit" in _SOUNDS:
        _SOUNDS["piece_hit"].set_volume(0.6)
    if "game_win" in _SOUNDS:
        _SOUNDS["game_win"].set_volume(0.75)
    if "game_draw" in _SOUNDS:
        _SOUNDS["game_draw"].set_volume(0.7)
    if "gameover" in _SOUNDS:
        _SOUNDS["gameover"].set_volume(0.6)

    _AUDIO_READY = True


def _play(key: str):
    _init_audio()
    sound = _SOUNDS.get(key)
    if sound is not None:
        sound.play()


def play_hover():
    """Play UI hover when entering a menu button."""
    _play("ui_hover")


def play_select():
    """Play UI select for valid clicks and restarts."""
    _play("ui_select")


def play_drop():
    """Play the piece drop sound when animation starts."""
    _play("piece_drop")


def play_hit():
    """Play the impact sound when a piece lands."""
    _play("piece_hit")


def play_win():
    """Play the win sound on game over."""
    _play("game_win")


def play_draw():
    """Play the draw sound on game over."""
    _play("game_draw")


def play_gameover():
    """Play a general game over stinger."""
    _play("gameover")
