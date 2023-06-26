import random
import time

import pygame

import assets
from constants import *
from menu import MainMenu
from physics import check_collisions_polygons, check_collisions_polygon_rectangle, get_rectangle_vertices
from tank import Tank


class Game:
    def __init__(self, debug=False, score_to_win=50, window_width=1500, window_height=960):
        super(Game).__init__()
        self.running = True
        self.debug = debug

        # Window
        if window_width == 1500 and window_height == 960:  # Use the monitor's resolution
            monitorInfo = pygame.display.Info()
            self.window_width = monitorInfo.current_w
            self.window_height = monitorInfo.current_h - 80
            self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
        else:  # Use the given window size
            self.window_width = window_width
            self.window_height = window_height
            self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # Window size dependant variables
        self.grid_x_offset = (self.window_width / 4 + (self.window_width * 3 / 4) % CELL_WIDTH) // 2
        self.grid_y_offset = (self.window_height / 6 + (self.window_height * 5 / 6) % CELL_HEIGHT) // 2
        self.grid_width = int((self.window_width - self.grid_x_offset * 2) // CELL_WIDTH)
        self.grid_height = int((self.window_height - self.grid_y_offset * 2) // CELL_HEIGHT)

        # Initialize textures
        assets.init()
        self.DEFAULT_FONT = assets.DEFAULT_FONT
        self.obstacle_colors = list([(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for i in range(200)])

        # Sounds
        self.sound_channel = pygame.mixer.Channel(0)
        self.sound_channel.set_volume(0.01)

        # Players
        self.nb_players = 0
        self.players: list[Tank] = []
        self.keybindings = []
        self.joysticks = {}
        self.scores = []

        self.bullets = []
        self.obstacles = []
        self.score_to_win = score_to_win
        self.stop_time = 0
        self.walls = []

        # Menus
        self.menu_running = True
        self.main_menu = MainMenu(self)
        self.current_menu = self.main_menu

    def game_loop(self):
        clock = pygame.time.Clock()

        while self.running:
            if self.menu_running:
                self.current_menu.menu_loop()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
                        self.update_joystick_list()

                self.check_input(pygame.key.get_pressed())

                self.tick()

                self.draw()

                clock.tick(FPS)

    # Start the round
    def start_round(self):
        self.create_maze()
        self.spawn_tanks()

    def end_round(self):
        self.stop_time = 0
        self.bullets = []
        for player in self.players:
            self.scores[player.id] += 1
        print("End of the round, score:", self.scores)

        winner = False
        for i in range(len(self.scores)):
            if self.scores[i] >= self.score_to_win:
                print("Player", i, "wins the game !")
                break

        if not winner:
            self.start_round()

    # Create the maze walls for the round
    def create_maze(self):
        cells = []  # 2D boolean list for visited cells
        connections = []  # 3D empty list (3rd dim is filled with empty lists)
        for x in range(self.grid_width):
            cells.append([])
            connections.append([])
            for y in range(self.grid_height):
                connections[x].append([])
                cells[x].append(False)

        cells[0][0] = True  # Set a starting cell
        nb_visited_cells = 1
        visited_cells_stack = [(0, 0)]

        # DFS algorithm to create maze-like paths
        while nb_visited_cells < self.grid_width * self.grid_height:  # While all cells haven't been visited
            cell = visited_cells_stack[len(visited_cells_stack) - 1]
            x = cell[0]
            y = cell[1]

            # Get all unvisited neighbouring cells as a tuple: (x, y, direction)
            neighboors: list[tuple[int, int, int]] = []
            if x - 1 >= 0 and not cells[x - 1][y]:  # Left: n_dir=3
                neighboors.append((x - 1, y, 3))
            if x + 1 < self.grid_width and not cells[x + 1][y]:  # Right: n_dir=1
                neighboors.append((x + 1, y, 1))
            if y - 1 >= 0 and not cells[x][y - 1]:  # Up: n_dir=0
                neighboors.append((x, y - 1, 0))
            if y + 1 < self.grid_height and not cells[x][y + 1]:  # Down: n_dir=2
                neighboors.append((x, y + 1, 2))

            # Pick a random neighbour to visit
            if len(neighboors) > 0:
                neighboor = neighboors[random.randint(0, len(neighboors) - 1)]
                n_x: int = neighboor[0]
                n_y: int = neighboor[1]
                n_dir = neighboor[2]
                visited_cells_stack.append(neighboor)
                cells[n_x][n_y] = True
                nb_visited_cells += 1

                # Add a connection
                if n_dir == 0:  # Up neighbour: add a down connection to neighbour
                    connections[n_x][n_y].append(2)
                elif n_dir == 3:  # Left neighbour: add a right connection to neighbour
                    connections[n_x][n_y].append(1)
                else:  # Right or down connection: add a right or down to connection to current cell
                    connections[x][y].append(n_dir)
            else:  # If there is no neighbour, remove cell from stack
                visited_cells_stack.pop()

        # Create maze walls using connections
        self.create_maze_walls(connections)

    # Create maze walls using connections
    # connections is a 2D list which stores for each cell a tuple (1, 2)
    # The stored tuple can contain a 1 for a connection to the cell to the right or a 2 to connect to the bottom cell
    # Connection examples: () -> No connection, (1) -> Right connection, (1, 2) -> Right and down connections
    def create_maze_walls(self, connections: list[list[tuple[int]]]):
        v_walls = []
        h_walls = []
        long_v_walls = []
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if len(connections[x][y]) == 0:  # No connection, two walls
                    if y + 1 < self.grid_height and random.random() < WALL_ODDS:
                        h_walls.append((x, y))
                    if x + 1 < self.grid_width and random.random() < WALL_ODDS:
                        if y - 1 >= 0 and ((x, y - 1) not in v_walls and (x, y - 1) not in long_v_walls) and (
                                x + 1, y - 1) not in h_walls:
                            long_v_walls.append((x, y))
                        else:
                            v_walls.append((x, y))
                elif len(connections[x][y]) == 1:  # One connection, one wall the opposite way
                    # Horizontal connection, Horizontal wall
                    if connections[x][y][0] == 1:
                        if y + 1 < self.grid_height and random.random() < WALL_ODDS:
                            h_walls.append((x, y))
                    else:  # Vertical connection, Vertical wall
                        if x + 1 < self.grid_width and random.random() < WALL_ODDS:
                            if y - 1 >= 0 and ((x, y - 1) not in v_walls and (x, y - 1) not in long_v_walls) and (
                                    x + 1, y - 1) not in h_walls:
                                long_v_walls.append((x, y))
                            else:
                                v_walls.append((x, y))
                # There is no else, because 2 connections -> no wall

        # Create walls with their on-screen size
        self.walls = []

        # Merge horizontal walls
        found_wall = False
        wall_x_start = 0
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if (x, y) in h_walls:  # Horizontal wall at (x, y)
                    h_walls.pop(h_walls.index((x, y)))
                    if not found_wall:
                        found_wall = True
                        wall_x_start = x
                else:  # No horizontal wall
                    if found_wall:  # Merge the walls found
                        found_wall = False
                        self.walls.append((wall_x_start * CELL_WIDTH + self.grid_x_offset,
                                           y * CELL_HEIGHT + CELL_HEIGHT - WALL_WIDTH + self.grid_y_offset,
                                           CELL_WIDTH * (x - wall_x_start), WALL_WIDTH))
            if found_wall:  # Line ended, Merge the walls found
                found_wall = False
                self.walls.append((wall_x_start * CELL_WIDTH + self.grid_x_offset,
                                   y * CELL_HEIGHT + CELL_HEIGHT - WALL_WIDTH + self.grid_y_offset,
                                   CELL_WIDTH * (self.grid_width - wall_x_start), WALL_WIDTH))

        # Merge vertical walls
        found_wall = False
        wall_y_start = 0
        wall_start_long = False
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in v_walls:  # Vertical wall at (x, y)
                    v_walls.pop(v_walls.index((x, y)))
                    if not found_wall:
                        found_wall = True
                        wall_y_start = y
                        wall_start_long = False
                elif (x, y) in long_v_walls:  # Long vertical wall at (x, y)
                    long_v_walls.pop(long_v_walls.index((x, y)))
                    if not found_wall:
                        found_wall = True
                        wall_y_start = y
                        wall_start_long = True
                else:  # No horizontal wall
                    if found_wall:  # Merge the walls found
                        found_wall = False
                        if wall_start_long:  # Add a long wall at the top
                            self.walls.append((x * CELL_WIDTH + CELL_WIDTH - WALL_WIDTH + self.grid_x_offset,
                                               wall_y_start * CELL_HEIGHT + self.grid_y_offset - WALL_WIDTH,
                                               WALL_WIDTH, CELL_HEIGHT * (y - wall_y_start) + WALL_WIDTH))
                        else:  # Add standard walls
                            self.walls.append((x * CELL_WIDTH + CELL_WIDTH - WALL_WIDTH + self.grid_x_offset,
                                               wall_y_start * CELL_HEIGHT + self.grid_y_offset,
                                               WALL_WIDTH, CELL_WIDTH * (y - wall_y_start)))
            if found_wall:  # Line ended, Merge the walls found
                found_wall = False
                if wall_start_long:  # Add a long wall at the top
                    self.walls.append((x * CELL_WIDTH + CELL_WIDTH - WALL_WIDTH + self.grid_x_offset,
                                       wall_y_start * CELL_HEIGHT + self.grid_y_offset - WALL_WIDTH,
                                       WALL_WIDTH, CELL_HEIGHT * (self.grid_height - wall_y_start) + WALL_WIDTH))
                else:  # Add standard walls
                    self.walls.append((x * CELL_WIDTH + CELL_WIDTH - WALL_WIDTH + self.grid_x_offset,
                                       wall_y_start * CELL_HEIGHT + self.grid_y_offset,
                                       WALL_WIDTH, CELL_WIDTH * (self.grid_height - wall_y_start)))

        if len(h_walls) > 0 or len(v_walls) > 0 or len(long_v_walls) > 0:
            print("Error in Game.create_maze_walls: some walls haven't been added:")
            print(f"Horizontal walls : {len(h_walls)}, vertical walls : {len(v_walls)}, long vertical walls : {len(long_v_walls)}, ")

        """
        for wall in h_walls:
            self.walls.append((wall[0] * CELL_WIDTH + self.grid_x_offset,
                               wall[1] * CELL_HEIGHT + CELL_HEIGHT - WALL_WIDTH + self.grid_y_offset,
                               CELL_WIDTH, WALL_WIDTH))

        for wall in v_walls:
            self.walls.append((wall[0] * CELL_WIDTH + CELL_WIDTH - WALL_WIDTH + self.grid_x_offset,
                               wall[1] * CELL_HEIGHT + self.grid_y_offset,
                               WALL_WIDTH, CELL_WIDTH))

        for wall in long_v_walls:
            self.walls.append((wall[0] * CELL_WIDTH + CELL_WIDTH - WALL_WIDTH + self.grid_x_offset,
                               wall[1] * CELL_HEIGHT + self.grid_y_offset - WALL_WIDTH,
                               WALL_WIDTH, CELL_HEIGHT + WALL_WIDTH))
        """

        # Borders (4 world borders
        self.walls.append((self.grid_x_offset - BORDER_WIDTH, self.grid_y_offset - BORDER_WIDTH,
                           self.grid_width * CELL_WIDTH + BORDER_WIDTH * 2, BORDER_WIDTH))
        self.walls.append((self.grid_x_offset - BORDER_WIDTH, self.grid_y_offset + self.grid_height * CELL_HEIGHT,
                           self.grid_width * CELL_WIDTH + BORDER_WIDTH * 2, BORDER_WIDTH))
        self.walls.append((self.grid_x_offset - BORDER_WIDTH, self.grid_y_offset - BORDER_WIDTH,
                           BORDER_WIDTH, self.grid_height * CELL_HEIGHT + BORDER_WIDTH * 2))
        self.walls.append((self.grid_x_offset + self.grid_width * CELL_WIDTH, self.grid_y_offset - BORDER_WIDTH,
                           BORDER_WIDTH, self.grid_height * CELL_HEIGHT + BORDER_WIDTH * 2))

    def spawn_tanks(self):
        self.players = []
        used_spots = []
        nb_tank_spawned = 0
        while nb_tank_spawned < self.nb_players:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if not (x, y) in used_spots:
                used_spots.append((x, y))
                spawn_x = self.grid_x_offset + x * CELL_WIDTH + CELL_WIDTH / 2
                spawn_y = self.grid_y_offset + y * CELL_HEIGHT + CELL_HEIGHT / 2
                self.players.append(Tank(self, nb_tank_spawned, self.keybindings[nb_tank_spawned], spawn_x, spawn_y))
                nb_tank_spawned += 1

    def check_input(self, keys_pressed):
        for player in self.players:
            player.check_input(keys_pressed)

    # Method called every frame
    def tick(self):
        # Check if the round should stop using the timer
        if 0 < self.stop_time < time.time():
            self.end_round()

        # Player movements
        player_tick_time_start = time.time()
        for player in self.players:
            player.move()
        player_tick_time = round((time.time() - player_tick_time_start) * 1000, 0)

        # Bullet movements
        bullet_tick_time_start = time.time()
        self.move_bullets()
        bullet_tick_time = round((time.time() - bullet_tick_time_start) * 1000, 0)

        # Game profiling
        if self.debug:
            # print(f"Tick time: Players {player_tick_time} ms\tBullets {bullet_tick_time} ms")

            if len(self.bullets) > 0:  # Each bullet takes about 1.2 to 1.5 ms to tick (avg is 1.3 ms)
                print(f"{len(self.bullets)} bullets ->\t{(bullet_tick_time/len(self.bullets))} ms per bullet")

    def move_bullets(self):
        for bullet in self.bullets:
            if bullet.spawn_time + BULLET_LIFE_TIME < time.time():
                self.bullets.remove(bullet)
            else:
                bullet.move()
                collision = self.check_collision_obstacles(
                    bullet.get_bounds(False), object_center=(bullet.x, bullet.y))
                if collision >= 0:
                    self.sound_channel.play(assets.BOUNCE_SOUND)
                    bullet.bounced_once = True

                    if collision == 0 and bullet.vel_y > 0:  # Top bounce
                        bullet.rotation = 180 - bullet.rotation
                        bullet.vel_y *= -1
                    elif collision == 2 and bullet.vel_y < 0:  # Bottom bounce
                        bullet.rotation = 180 - bullet.rotation
                        bullet.vel_y *= -1
                    elif collision == 1 and bullet.vel_x < 0:  # Right bounce
                        bullet.vel_x *= -1
                        bullet.rotation = 360 - bullet.rotation
                    elif collision == 3 and bullet.vel_x > 0:  # Left bounce
                        bullet.vel_x *= -1
                        bullet.rotation = 360 - bullet.rotation

                for player in self.players:  # Check if a player is touched
                    if player.id != bullet.id or bullet.bounced_once:  # Stop the player from dying from its own bullet
                        collision = check_collisions_polygons(
                            player.get_bounds(0, 0, 0), bullet.get_bounds(False))
                        if collision:
                            self.sound_channel.play(assets.HIT_SOUND)
                            self.players.remove(player)
                            self.bullets.remove(bullet)
                            if len(self.players) <= 1:
                                self.stop_time = time.time() + 3

                if bullet.check_border_collision():
                    self.bullets.remove(bullet)

    # Check collisions between the polygon (eg: player or bullet) and obstacles
    def check_collision_obstacles(self, polygon: list[tuple[float, float]], object_center=(0, 0)):
        for obstacle in self.walls:
            if object_center == (0, 0):
                rect_vertices = get_rectangle_vertices(obstacle)
                collision = check_collisions_polygon_rectangle(
                    polygon, rect_vertices)
                if collision != -1:
                    return collision
            else:  # If an object center is provided, check distance first
                # Calculate bullet-obstacle distance and choose to check for collision if close enough (good optimisation)
                distance = math.sqrt(
                    (obstacle[0] + obstacle[2] / 2 - object_center[0]) ** 2 +
                    (obstacle[1] + obstacle[3] / 2 - object_center[1]) ** 2
                )
                max_distance = max(obstacle[2], obstacle[3]) + max(TANK_DIAGONAL, BULLET_DIAGONAL) * 2
                if distance <= max_distance:
                    rect_vertices = get_rectangle_vertices(obstacle)
                    collision = check_collisions_polygon_rectangle(
                        polygon, rect_vertices)
                    if collision != -1:
                        return collision
        return -1

    def check_collisions_tanks(self, id, bounds):
        for player in self.players:
            if player.id != id:
                if check_collisions_polygons(player.get_bounds(0, 0, 0), bounds):
                    return True
        return False

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)

        # Show cells
        # if self.debug:
        #     for x in range(self.grid_width):
        #         for y in range(self.grid_height):
        #             color = (140, 255, 140)
        #             if (x + y) % 2 == 0:
        #                 color = (140, 140, 255)
        #             pygame.draw.rect(self.window, color, (
        #                 x * CELL_WIDTH + self.grid_x_offset,
        #                 y * CELL_HEIGHT + self.grid_y_offset,
        #                 CELL_WIDTH, CELL_WIDTH
        #             ))

        if self.debug:  # Colorful walls
            for i, obstacle in enumerate(self.walls):
                pygame.draw.rect(self.window, self.obstacle_colors[i], obstacle)
        else:  # Standard black walls
            for i, obstacle in enumerate(self.walls):
                pygame.draw.rect(self.window, (0, 0, 0), obstacle)

        for player in self.players:
            player.draw(self.window)

        for bullet in self.bullets:
            bullet.draw(self.window)

        self.draw_score()

        pygame.display.flip()

    def draw_score(self):
        score_title_font = pygame.font.Font(self.DEFAULT_FONT, 28)
        score_font = pygame.font.Font(self.DEFAULT_FONT, 20)

        score_title_string = "Scores"
        score_title_surface = score_title_font.render(score_title_string, True, (0, 0, 0))
        score_title_rect = score_title_surface.get_rect()
        score_title_rect.topleft = (20, self.grid_y_offset)
        self.window.blit(score_title_surface, score_title_rect)

        for i in range(self.nb_players):
            score_string = TANK_COLOR_NAMES[i].capitalize() + " " + str(self.scores[i])
            score_surface = score_font.render(score_string, True, TANK_TEXT_COLORS[i])
            score_rect = score_surface.get_rect()
            score_rect.topleft = (20, self.grid_y_offset + 40 + i * 30)
            self.window.blit(score_surface, score_rect)

    def set_nb_players(self, nb_players):
        self.nb_players = nb_players
        self.players = []
        self.scores = [0] * nb_players
        self.keybindings = []

        # for i in range(nb_players):
        #     self.keybindings.append({
        #         "keyboard": True,
        #         "joystick_guid": "",
        #         "forward": None,
        #         "backward": None,
        #         "left": None,
        #         "right": None
        #     })

    def get_nb_keyboard_players(self):
        n = 0
        for keybinding in self.keybindings:
            if keybinding["keyboard"]:
                n += 1
        return n

    def get_player_bullet_amount(self, player_id) -> int:
        amount = 0
        for bullet in self.bullets:
            if bullet.id == player_id:
                amount += 1
        return amount

    # Updates the list of all joystick connected
    def update_joystick_list(self):
        print("updating joysticks")
        self.joysticks = {}  # {guid: Joystick}
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            self.joysticks[joystick.get_guid()] = joystick

        print(self.joysticks)
