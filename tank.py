import random as random
import time
from constants import *
from bullet import Bullet
import assets


class Tank:
    def __init__(self, game, id: int, keybindings, spawn_x, spawn_y):
        super(Tank).__init__()
        self.game = game
        self.id = id
        self.x = spawn_x
        self.y = spawn_y
        self.vel = 0
        self.rotation = random.random() * 360
        self.last_shot_time = 0
        self.keybindings = keybindings

    def check_input(self, keys_pressed):
        inputs = self.get_inputs(keys_pressed)

        # If the velocity is almost 0 set it to 0
        if -1 < self.vel < 1:
            self.vel = 0

        if inputs["forward"] and not inputs["backward"]:  # Forward
            self.vel = TANK_SPEED
        if inputs["backward"] and not inputs["forward"]:  # Backward
            self.vel = -TANK_SPEED
        if inputs["turn_left"] and not inputs["turn_right"]:  # Turn left
            # Check collisions
            # print(self.game.check_collision_obstacles(self.get_bounds(0, 0, TANK_ROT_SPEED)))
            if self.game.check_collision_obstacles(self.get_bounds(0, 0, TANK_ROT_SPEED)) == -1 and not self.game.check_collisions_tanks(self.id, self.get_bounds(0, 0, TANK_ROT_SPEED)):
                self.rotation += TANK_ROT_SPEED
        if inputs["turn_right"] and not inputs["turn_left"]:  # Turn right
            # CHeck collisions
            if self.game.check_collision_obstacles(self.get_bounds(0, 0, -TANK_ROT_SPEED)) == -1 and not self.game.check_collisions_tanks(self.id, self.get_bounds(0, 0, -TANK_ROT_SPEED)):
                self.rotation -= TANK_ROT_SPEED

        if inputs["shoot"] and self.last_shot_time + TANK_SHOT_COOLDOWN < time.time() and self.game and self.game.get_player_bullet_amount(self.id) < MAX_TANK_BULLETS:  # Shoot
            self.last_shot_time = time.time()
            self.shoot()

        self.rotation %= 360

        # DEBUG ONLY (rotation axis alignment)
        if self.game.debug:
            if keys_pressed[pygame.K_r]:  # Reset rotation
                self.rotation = 0
            if keys_pressed[pygame.K_a]:  # Turn left 90°
                self.rotation += 90
            if keys_pressed[pygame.K_e]:  # Turn right 90°
                self.rotation -= 90

    # Returns a boolean dict with the inputs name
    def get_inputs(self, keys_pressed):
        if self.keybindings["keyboard"]:  # Keyboard
            return {
                "forward": keys_pressed[self.keybindings["forward"]],
                "backward": keys_pressed[self.keybindings["backward"]],
                "turn_left": keys_pressed[self.keybindings["turn_left"]],
                "turn_right": keys_pressed[self.keybindings["turn_right"]],
                "shoot": keys_pressed[self.keybindings["shoot"]]
            }
        else:  # Joystick
            if self.keybindings["joystick_guid"] in self.game.joysticks:
                joystick = self.game.joysticks[self.keybindings["joystick_guid"]]  # Get joystick
                x_axis, y_axis = joystick.get_axis(0), joystick.get_axis(1)

                # Joystick angle tests
                # if self.id == 0 and x_axis ** 2 + y_axis ** 2 > -1:
                #     joy_angle = (270 - math.degrees(math.atan2(y_axis, x_axis))) % 360  # Convert axis values to angle
                #     print("tank rotation:", self.rotation, "\tjoy angle:", joy_angle)

                return {
                    "forward": y_axis < -JOYSTICK_DEADZONE,
                    "backward": y_axis > JOYSTICK_DEADZONE,
                    "turn_left": x_axis < -JOYSTICK_DEADZONE,
                    "turn_right": x_axis > JOYSTICK_DEADZONE,
                    "shoot": joystick.get_button(0)
                }
            else:  # No joystick found
                print("No joystick with guid:", self.keybindings["joystick_guid"])
                return {
                    "forward": False,
                    "backward": False,
                    "turn_left": False,
                    "turn_right": False,
                    "shoot": False
                }

    # Shoot a new bullet
    def shoot(self):
        bullet_vel_x = math.cos(math.radians(
            self.rotation) + math.pi / 2) * BULLET_SPEED
        bullet_vel_y = math.sin(math.radians(
            self.rotation) + math.pi / 2) * -BULLET_SPEED

        spawn_x = self.x + math.cos(math.radians(
            self.rotation) + math.pi / 2) * (TANK_WIDTH / 2 - BULLET_HEIGHT / 2)
        spawn_y = self.y + math.sin(math.radians(
            self.rotation) + math.pi / 2) * -(TANK_HEIGHT / 2 - BULLET_HEIGHT / 2)

        # Create the bullet
        self.game.bullets.append(Bullet(self.game, self.id, spawn_x, spawn_y, bullet_vel_x, bullet_vel_y, self.rotation))

        self.game.sound_channel.play(assets.SHOOT_SOUND)

    def move(self):
        vel_x = math.cos(math.radians(
            self.rotation) + math.pi / 2) * self.vel
        vel_y = math.sin(math.radians(
            self.rotation) + math.pi / 2) * -self.vel

        obstacle_collision = self.game.check_collision_obstacles(self.get_bounds(vel_x, vel_y, 0))
        if obstacle_collision == -1 and not self.game.check_collisions_tanks(self.id, self.get_bounds(vel_x, vel_y, 0)):
            self.x += vel_x
            self.y += vel_y
        else:  # A wall is stoping the player, try to slide against it
            if obstacle_collision == 0 or obstacle_collision == 2:  # Horizontal wall -> x slide
                if (self.game.check_collision_obstacles(self.get_bounds(vel_x, 0, 0)) == -1 and
                        not self.game.check_collisions_tanks(self.id, self.get_bounds(vel_x, 0, 0))):
                    self.x += vel_x
            if obstacle_collision == 1 or obstacle_collision == 3:  # Vertical wall -> y slide
                if (self.game.check_collision_obstacles(self.get_bounds(0, vel_y, 0)) == -1 and
                        not self.game.check_collisions_tanks(self.id, self.get_bounds(0, vel_y, 0))):
                    self.y += vel_y

        # print("rotation", self.rotation, "x", self.x, "y", self.y, "cos a", vel_x, "sin a", vel_y) # Print infos

        self.vel *= TANK_DECELERATION

    def draw(self, window):
        rotated_image = pygame.transform.rotate(
            assets.TANK_TEXTURE[self.id]["tank"], self.rotation)
        new_rect = rotated_image.get_rect(
            center=assets.TANK_TEXTURE[self.id]["tank"].get_rect(center=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect)

        # pygame.draw.polygon(window, (170, 0, 0), self.get_bounds(0, 0, 0))  # Show outline

    # Get the coordinates of the vertices of the player
    def get_bounds(self, x_offset, y_offset, rotation_offset):
        bounds = []
        angles = [-45, 45, 135, -135]
        for angle in angles:
            x = self.x + x_offset + math.cos(
                math.radians(angle + self.rotation + rotation_offset)) * TANK_DIAGONAL / 2
            y = self.y + y_offset - math.sin(
                math.radians(angle + self.rotation + rotation_offset)) * TANK_DIAGONAL / 2
            bounds.append((x, y))
        return bounds
