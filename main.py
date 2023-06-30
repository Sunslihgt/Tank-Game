import pstats

from game import Game
from constants import *


# DONE : 4 balles par personne
# DONE : Ajouter titre menu jeu
# DONE : Combiner murs
# DONE : Limiter le nombre de tests de collisions en vérifiant la distance
# DONE : Refaire la physique et pleurer


# Should profile the main function ?
PROFILE = False


def main():
    # Init pygame
    pygame.init()
    pygame.joystick.init()

    # Create window
    pygame.display.set_caption("Tank Game v1.0 - Sunslihgt")

    # Create and start game
    game = Game(debug=False)
    # game = Game(debug=False, window_width=1920, window_height=1080)
    game.game_loop()


# Create 2 files in folder "profiling" -> output_calls.txt and output_time.txt
# These files can be used to understand which part of the code is too slow
def profile_main():
    import cProfile

    cProfile.run("main()", "profiling/output.dat")

    with open("profiling/output_time.txt", "w") as f:
        p = pstats.Stats("profiling/output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("profiling/output_calls.txt", "w") as f:
        p = pstats.Stats("profiling/output.dat", stream=f)
        p.sort_stats("calls").print_stats()

    with open("profiling/output_cumulative_time.txt", "w") as f:
        p = pstats.Stats("profiling/output.dat", stream=f)
        p.sort_stats("cumulative").print_stats()


if __name__ == "__main__":
    if PROFILE:
        profile_main()
    else:
        main()
