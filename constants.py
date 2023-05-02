import pygame
import math

"""
Global variables and constants
"""

# Tank
TANK_WIDTH = 48
TANK_HEIGHT = 48
TANK_COLOR = (66, 141, 245)
TANK_SPEED = 3
TANK_DECELERATION = 0.84
TANK_ROT_SPEED = 5
TANK_DIAGONAL = math.sqrt(TANK_WIDTH ** 2 + TANK_HEIGHT ** 2)
TANK_SHOT_COOLDOWN = 0.5

# Bullet
MAX_TANK_BULLETS = 100  # 5
BULLET_WIDTH = 8
BULLET_HEIGHT = 15
BULLET_SPEED = 6
BULLET_DIAGONAL = math.sqrt(BULLET_WIDTH ** 2 + BULLET_HEIGHT ** 2)
BULLET_INVINCIBILITY_TIME = 0.2
BULLET_LIFE_TIME = 8

# Maze
CELL_WIDTH = 100
CELL_HEIGHT = 100
WALL_WIDTH = 10
WALL_ODDS = 0.75
BORDER_WIDTH = 15


# Keybinds
DEFAULT_KEYBOARD_KEYBINDING = [
    {
        "keyboard": True,
        "joystick_guid": "",
        "forward": pygame.K_z,
        "backward": pygame.K_s,
        "turn_left": pygame.K_q,
        "turn_right": pygame.K_d,
        "shoot": pygame.K_SPACE
    },
    {
        "keyboard": True,
        "joystick_guid": "",
        "forward": pygame.K_UP,
        "backward": pygame.K_DOWN,
        "turn_left": pygame.K_LEFT,
        "turn_right": pygame.K_RIGHT,
        "shoot": pygame.K_RETURN
    },
    {
        "keyboard": True,
        "joystick_guid": "",
        "forward": pygame.K_i,
        "backward": pygame.K_k,
        "turn_left": pygame.K_j,
        "turn_right": pygame.K_l,
        "shoot": pygame.K_m
    },
    {
        "keyboard": True,
        "joystick_guid": "",
        "forward": pygame.K_KP8,
        "backward": pygame.K_KP5,
        "turn_left": pygame.K_KP4,
        "turn_right": pygame.K_KP6,
        "shoot": pygame.K_KP0
    }
]

JOYSTICK_DEADZONE = 0.6  # Joystick deadzone (avoids axis noise)

# Tank colors
TANK_COLOR_NAMES = ["bleu", "rouge", "vert", "jaune", "violet", "gris", "orange"]
TANK_TEXT_COLORS = [(18, 131, 180), (204, 58, 24), (85, 147, 85), (239, 228, 64), (107, 10, 204), (165, 165, 165), (255, 127, 39)]

FPS = 60

BACKGROUND_COLOR = (255, 255, 255)
