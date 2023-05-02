import time
from constants import *
import assets


class Bullet:
    def __init__(self, game, id, spawn_x, spawn_y, vel_x, vel_y, rotation):
        super(Bullet, self).__init__()
        self.game = game
        self.id = id  # Player's id
        self.x = spawn_x
        self.y = spawn_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.rotation = rotation
        self.spawn_time = time.time()
        self.bounced_once = False

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def check_border_collision(self):
        if self.x + BULLET_HEIGHT * 2 < 0 or self.x - BULLET_HEIGHT * 2 > self.game.window_width:
            return True
        if self.y + BULLET_HEIGHT * 2 < 0 or self.y - BULLET_HEIGHT * 2 > self.game.window_height:
            return True

    # next_move is True if we want to get the position after the next move
    def get_bounds(self, next_move):
        bounds = []
        angles = [-55, 55, 125, -125]
        for angle in angles:
            x = self.x + math.cos(
                math.radians(angle + self.rotation)) * BULLET_DIAGONAL / 2
            y = self.y - math.sin(
                math.radians(angle + self.rotation)) * BULLET_DIAGONAL / 2
            if next_move:
                x += self.vel_x
                y += self.vel_y
            bounds.append((x, y))
        return bounds

    def draw(self, window):
        rotated_image = pygame.transform.rotate(assets.TANK_TEXTURE[self.id]["bullet"], self.rotation)
        new_rect = rotated_image.get_rect(
            center=assets.TANK_TEXTURE[self.id]["bullet"].get_rect(center=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect)
