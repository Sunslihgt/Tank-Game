import os

import pygame

from constants import TANK_WIDTH, TANK_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT

ROOT_PATH = os.path.dirname(__file__)

TANK_TEXTURE = []

MOVEMENT_ARROWS_TEXTURE = []

SHOOT_SOUND = None
BOUNCE_SOUND = None
HIT_SOUND = None

DEFAULT_FONT = ""



def init():
    global TANK_TEXTURE, MOVEMENT_ARROWS_TEXTURE, SHOOT_SOUND, BOUNCE_SOUND, HIT_SOUND, DEFAULT_FONT

    TANK_TEXTURE = [
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/blue_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/blue_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        },
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/red_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/red_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        },
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/green_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/green_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        },
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/yellow_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/yellow_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        },
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/purple_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/purple_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        },
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/grey_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/grey_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        },
        {
            "tank": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/orange_tank.png")), (TANK_WIDTH, TANK_HEIGHT)),
            "bullet": pygame.transform.scale(pygame.image.load(
                os.path.join(ROOT_PATH, "Assets/Textures/orange_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
        }
    ]

    MOVEMENT_ARROWS_TEXTURE = [
        {
            "forward": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/forward_arrow.png")),
            "backward": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/backward_arrow.png")),
            "turn_left": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/left_arrow.png")),
            "turn_right": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/right_arrow.png"))
        },
        {
            "forward": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/forward_arrow_red.png")),
            "backward": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/backward_arrow_red.png")),
            "turn_left": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/left_arrow_red.png")),
            "turn_right": pygame.image.load(os.path.join(ROOT_PATH, "Assets/Textures/menus/right_arrow_red.png"))
        }
    ]

    SHOOT_SOUND = pygame.mixer.Sound(os.path.join(ROOT_PATH, "Assets/Sounds/shoot.wav"))
    BOUNCE_SOUND = pygame.mixer.Sound(os.path.join(ROOT_PATH, "Assets/Sounds/bounce.wav"))
    HIT_SOUND = pygame.mixer.Sound(os.path.join(ROOT_PATH, "Assets/Sounds/hit.wav"))

    DEFAULT_FONT = os.path.join(ROOT_PATH, "Assets/Fonts/arial.ttf")
