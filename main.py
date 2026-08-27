import curses
import sys

sys.dont_write_bytecode = True
from lib.input_handling.input_character_handler import InputHandler
from lib.window_manager.main_draw_loop import clear_screen


def main(stdscr: curses.window):
    input_handler = InputHandler(stdscr)

    while True:
        # Jede Iteration das UI frisch zeichnen
        input_handler.draw()

        # Auf Input / Resize warten
        if input_handler.check_user_input():
            break

    clear_screen()


if __name__ == "__main__":
    curses.wrapper(main)
