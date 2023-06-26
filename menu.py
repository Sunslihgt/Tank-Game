import pygame

import assets
from constants import DEFAULT_KEYBOARD_KEYBINDING, JOYSTICK_DEADZONE, TANK_COLOR_NAMES


# Menu parent class (menus overwrite it)
class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.labels = []

        self.mid_x = self.game.window_width / 2
        self.mid_y = self.game.window_height / 2

    def menu_loop(self):
        self.check_input()
        self.draw_menu(self.game.window)

    # Default input check that should be overriden
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game.running = False
                self.game.menu_running = False

    def draw_menu(self, window: pygame.Surface):
        window.fill(BACKGROUND_COLOR, (0, 0, self.game.window_width, self.game.window_height))

        for button in self.buttons:
            button.draw_button(window)

        for label in self.labels:
            label.draw_label(window)

        pygame.display.flip()


# Main title and player count choice
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.title_label = Label(self.game.window_width / 2, self.game.window_height * 0.2, "Tank game", 80, center=True)
        self.labels.append(self.title_label)

        self.nb_buttons = 6
        labels_text = ["2 Joueurs", "3 Joueurs", "4 Joueurs", "5 Joueurs", "6 Joueurs", "7 Joueurs", "8 Joueurs"]
        button_positions = [
            (self.game.window_width / 2 - 120, self.game.window_height * 0.40),
            (self.game.window_width / 2 + 120, self.game.window_height * 0.40),
            (self.game.window_width / 2 - 120, self.game.window_height * 0.50),
            (self.game.window_width / 2 + 120, self.game.window_height * 0.50),
            (self.game.window_width / 2 - 120, self.game.window_height * 0.60),
            (self.game.window_width / 2 + 120, self.game.window_height * 0.60),
            (self.game.window_width / 2 - 120, self.game.window_height * 0.70),
            (self.game.window_width / 2 - 120, self.game.window_height * 0.70),
        ]
        self.player_count_buttons = []

        # Create the buttons to choose the number of players
        for i in range(self.nb_buttons):
            label = Label(button_positions[i][0], button_positions[i][1], labels_text[i], 16, center=True)
            button = Button(button_positions[i][0], button_positions[i][1], 100, 40, label, center=True)
            self.player_count_buttons.append(button)
            self.buttons.append(button)

        self.left_click_pressed = False  # Mouse button currently pressed, not released yet

    def check_input(self):
        left_click_released = False  # Button just released -> activate menu buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game.running = False
                self.game.menu_running = False
            # If in debug mode, press return to skip menu
            elif self.game.debug and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game.menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.left_click_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.left_click_pressed = False
                left_click_released = True
            elif event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
                self.game.update_joystick_list()

        # Check which buttons are hovered by the mouse
        mx, my = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hovered(mx, my, self.left_click_pressed)

        # Check if a button has been pressed
        if left_click_released:
            for i in range(self.nb_buttons):
                if self.player_count_buttons[i].hovered:
                    # print((i + 2), "players")
                    self.game.set_nb_players(i + 2)
                    self.game.current_menu = PlayerInputMenu(self.game, 0)


# Choose keyboard or contraller input
class PlayerInputMenu(Menu):
    def __init__(self, game, player_id):
        Menu.__init__(self, game)

        self.player_label = Label(self.game.window_width / 2, 55, "Tank " + TANK_COLOR_NAMES[player_id], 50, center=True)
        self.labels.append(self.player_label)

        self.shooting = False

        # print("id:", player_id)

        self.player_id = player_id
        self.keybinds = {}

        # Start as keyboard player if there is keybindings left
        if self.game.get_nb_keyboard_players() < 4:
            self.reset_keybinds(keyboard=True)
        else:
            self.reset_keybinds(keyboard=False)

        self.left_click_pressed = False

        self.inputs = {
            "forward": False,
            "backward": False,
            "turn_left": False,
            "turn_right": False,
            "shoot": False
        }

        self.movements_rect = (self.mid_x - 250, 100, 500, 500)

        self.tank_image = pygame.transform.scale(assets.TANK_TEXTURE[self.player_id]["tank"], (130, 130))
        self.tank_rect = self.tank_image.get_rect()
        self.tank_rect.center = (self.mid_x, 350)

        self.arrows_rect = {
            "forward": assets.MOVEMENT_ARROWS_TEXTURE[0]["forward"].get_rect(),
            "backward": assets.MOVEMENT_ARROWS_TEXTURE[0]["backward"].get_rect(),
            "turn_left": assets.MOVEMENT_ARROWS_TEXTURE[0]["turn_left"].get_rect(),
            "turn_right": assets.MOVEMENT_ARROWS_TEXTURE[0]["turn_right"].get_rect(),
        }

        self.arrows_rect["forward"].center = (self.mid_x, 210)
        self.arrows_rect["backward"].center = (self.mid_x, 490)
        self.arrows_rect["turn_left"].center = (self.mid_x - 160, 360)
        self.arrows_rect["turn_right"].center = (self.mid_x + 160, 360)

        # Buttons
        keyboard_label = Label(self.mid_x - 160, self.game.window_height * 0.7, "Clavier", 16, center=True)
        self.btn_keyboard = Button(self.mid_x - 160, self.game.window_height * 0.7, 100, 40,
                                   keyboard_label, center=True)
        self.buttons.append(self.btn_keyboard)

        joystick_label = Label(self.mid_x + 160, self.game.window_height * 0.7, "Manette", 16, center=True)
        self.btn_joystick = Button(self.mid_x + 160, self.game.window_height * 0.7, 100, 40,
                                   joystick_label, center=True)
        self.buttons.append(self.btn_joystick)

        self.choose_joystick_label = Label(self.mid_x, self.game.window_height * 0.70,
                                           "Appuyer sur une touche", 16, center=True)

        next_label = Label(self.mid_x, self.game.window_height * 0.85, "Continuer", 16, center=True)
        self.btn_next = Button(self.mid_x, self.game.window_height * 0.85, 100, 40,
                               next_label, center=True)
        self.buttons.append(self.btn_next)

    def draw_menu(self, window: pygame.Surface):  # Draw player input menu
        window.fill(BACKGROUND_COLOR, (0, 0, self.game.window_width, self.game.window_height))

        # Tank movements visualisation
        window.fill((180, 180, 180), self.movements_rect)

        # Draw input arrows
        if self.inputs["forward"]:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[1]["forward"], self.arrows_rect["forward"])
        else:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[0]["forward"], self.arrows_rect["forward"])

        if self.inputs["backward"]:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[1]["backward"], self.arrows_rect["backward"])
        else:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[0]["backward"], self.arrows_rect["backward"])

        if self.inputs["turn_left"]:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[1]["turn_left"], self.arrows_rect["turn_left"])
        else:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[0]["turn_left"], self.arrows_rect["turn_left"])

        if self.inputs["turn_right"]:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[1]["turn_right"], self.arrows_rect["turn_right"])
        else:
            window.blit(assets.MOVEMENT_ARROWS_TEXTURE[0]["turn_right"], self.arrows_rect["turn_right"])

        # Playing a sound when pressing the shoot button
        if not self.shooting and self.inputs["shoot"]:
            self.shooting = True
            # print("Shooting")
            self.game.sound_channel.play(assets.SHOOT_SOUND)
        if self.shooting and not self.inputs["shoot"]:
            self.shooting = False

        # Draw tank
        window.blit(self.tank_image, self.tank_rect)

        # If joystick mode is selected but no joystick is chosen yet, display "press a button" string
        if not self.keybinds["keyboard"] and self.keybinds["joystick_guid"] not in self.game.joysticks:
            self.choose_joystick_label.draw_label(window)

        for button in self.buttons:
            button.draw_button(window)

        for label in self.labels:
            label.draw_label(window)

        pygame.display.flip()

    def check_input(self):
        left_click_released = False  # Button just released -> activate menu buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game.running = False
                self.game.menu_running = False
            # If in debug mode press return to skip input menu
            elif self.game.debug and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game.menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.left_click_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.left_click_pressed = False
                left_click_released = True
            elif event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
                self.game.update_joystick_list()
            elif event.type == pygame.JOYAXISMOTION:
                # print(event)
                pass
            elif event.type == pygame.JOYHATMOTION:
                # print("joy hat motion", event)
                pass
            elif event.type == pygame.JOYBUTTONDOWN:
                # print("joy button pressed", event)
                # If no joystick is chosen yet (joystick_guid is "" so it is not in the existing joysticks list)
                if not self.keybinds["keyboard"] and self.keybinds["joystick_guid"] not in self.game.joysticks:
                    # Check if the button's joystick is already used by another player
                    # print("id:", event.instance_id, "nb joysticks:", pygame.joystick.get_count())
                    guid = pygame.joystick.Joystick(event.instance_id).get_guid()
                    # print(guid)

                    if guid in self.game.joysticks:  # This joystick exists
                        jostick_used = False
                        for keybinding in self.game.keybindings:
                            if not keybinding["keyboard"]:
                                if keybinding["joystick_guid"] == guid:
                                    jostick_used = True
                                    break
                        # This joystick is not used yet, let's use it
                        if not jostick_used:
                            self.keybinds["joystick_guid"] = guid
                            # print("Joystick chosen !")

        # Check which buttons are hovered by the mouse
        mx, my = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hovered(mx, my, self.left_click_pressed)

        if left_click_released:
            if self.btn_keyboard.hovered and not self.keybinds["keyboard"] and self.game.get_nb_keyboard_players() < 4:  # Switch to keyboard
                self.reset_keybinds(keyboard=True)
            if self.btn_joystick.hovered and self.keybinds["keyboard"]:  # Switch to joystick
                self.reset_keybinds(keyboard=False)
            # Confirm settings
            if self.btn_next.hovered and (self.keybinds["keyboard"] or self.keybinds["joystick_guid"] in self.game.joysticks):
                self.confirm_settings()
            # print(self.keybinds)

        # Show which button is pressed
        if self.keybinds["keyboard"]:  # Keyboard
            pass
        else:  # Joystick
            if self.keybinds["joystick_guid"] not in self.game.joysticks:
                pass

        # Highlight wether the player is using keyboard or joystick (modify pressed property)
        if self.keybinds["keyboard"]:  # Keyboard
            self.btn_keyboard.pressed = True
            self.btn_joystick.pressed = False
        else:  # Joystick
            self.btn_keyboard.pressed = False
            self.btn_joystick.pressed = True

        # Update the inputs to display the movements
        self.check_tank_display_input()

    # Check if the tank should be turning, shooting...
    # By updtating a dict -> inputs = {"direction_str": "bool"}
    def check_tank_display_input(self):
        if self.keybinds["keyboard"]:  # Keyboard
            keys_pressed = pygame.key.get_pressed()

            self.inputs["forward"] = keys_pressed[self.keybinds["forward"]]
            self.inputs["backward"] = keys_pressed[self.keybinds["backward"]]
            self.inputs["turn_left"] = keys_pressed[self.keybinds["turn_left"]]
            self.inputs["turn_right"] = keys_pressed[self.keybinds["turn_right"]]
            self.inputs["shoot"] = keys_pressed[self.keybinds["shoot"]]
        else:  # Joystick
            self.inputs["forward"] = False
            self.inputs["backward"] = False
            self.inputs["turn_left"] = False
            self.inputs["turn_right"] = False
            self.inputs["shoot"] = False

            if self.keybinds["joystick_guid"] in self.game.joysticks:  # A joystick is selected
                joystick = self.game.joysticks[self.keybinds["joystick_guid"]]  # Get joystick
                x_axis, y_axis = joystick.get_axis(0), joystick.get_axis(1)

                # print("axis0:", joystick.get_axis(0), "\taxis1:", joystick.get_axis(1))

                self.inputs["forward"] = y_axis < -JOYSTICK_DEADZONE
                self.inputs["backward"] = y_axis > JOYSTICK_DEADZONE
                self.inputs["turn_left"] = x_axis < -JOYSTICK_DEADZONE
                self.inputs["turn_right"] = x_axis > JOYSTICK_DEADZONE

                self.inputs["shoot"] = joystick.get_button(0)

    # Resets the keybinds and choose between keyboard and joystick
    def reset_keybinds(self, keyboard=True):
        if keyboard:
            nb_keyboard_players = self.game.get_nb_keyboard_players()
            self.keybinds = DEFAULT_KEYBOARD_KEYBINDING[nb_keyboard_players].copy()
        else:
            self.keybinds = {
                "keyboard": keyboard,
                "joystick_guid": "",
                "forward": None,
                "backward": None,
                "turn_left": None,
                "turn_right": None,
                "shoot": None
            }

    # Confirm settings and quit this menu
    def confirm_settings(self):
        self.game.keybindings.append(self.keybinds)
        # Open a new InputMenu if there is players who haven't chosen their keybindings yet
        if self.player_id < self.game.nb_players - 1:
            self.game.current_menu = PlayerInputMenu(self.game, self.player_id + 1)
        else:  # If all players are ready, start the game
            self.game.current_menu = None
            self.game.menu_running = False
            self.game.start_round()


class Button:
    def __init__(self, x, y, w, h, label, center=False):
        self.rect = pygame.Rect(x, y, w, h)
        if center:
            self.rect = pygame.Rect(x - w // 2, y - h // 2, w, h)

        self.label = label

        self.hovered = False
        self.pressed = False

    def draw_button(self, window: pygame.Surface):
        outline_color = (0, 0, 0)
        if self.hovered:
            outline_color = (255, 0, 0)

        # Fill with grey if pressed
        if self.pressed:
            pygame.draw.rect(window, (200, 200, 200), self.rect)

        pygame.draw.rect(window, outline_color, self.rect, width=3)
        self.label.draw_label(window)

    # Updates self.hovered and self.pressed if hovered and/or clicked by the mouse
    def check_hovered(self, mx: int, my: int, left_click: bool):
        self.hovered = self.rect.left <= mx <= self.rect.right and self.rect.top <= my <= self.rect.bottom
        self.pressed = self.hovered and left_click


class Label:
    def __init__(self, x, y, text: str, text_size: int, center=False):
        self.font = pygame.font.Font(assets.DEFAULT_FONT, text_size)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()

        if center:
            self.text_rect.center = (x, y)
        else:
            self.text_rect.topleft = (x, y)

    def draw_label(self, window):
        window.blit(self.text_surface, self.text_rect)


BACKGROUND_COLOR = (255, 255, 255)
