from game import Game
from constants import *


# DONE: 4 balles par personne
# DONE: Ajouter titre menu jeu
# DONE: Combiner murs
# DONE: Limiter le nombre de tests de collisions en vérifiant la distance
# TODO: Refaire la physique et pleurer


def main():
    # Init pygame
    pygame.init()
    pygame.joystick.init()

    # Create window
    pygame.display.set_caption("Tank Game v1.0 - Sunslihgt")

    # Create and start game
    game = Game(debug=False)
    game.game_loop()


if __name__ == "__main__":
    main()
