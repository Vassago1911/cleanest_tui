import sys
sys.dont_write_bytecode = True

import os
import curses
from curses import wrapper, window
from lib.input_handling.input_character_handler import InputHandler

def main(stdscr: window):
    # Einmaliges Clear vor dem Start von Curses ist okay
    os.system('cls||clear')
    input_handler = InputHandler(stdscr)

    while True:
        # Jede Iteration das UI frisch zeichnen
        input_handler.draw()

        # Auf Input / Resize warten
        if input_handler.check_user_input():
            break

    os.system('cls||clear')

if __name__ == "__main__":
    wrapper(main)
