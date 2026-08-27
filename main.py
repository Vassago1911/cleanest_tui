"""Main entry point for the IFS TUI application.

This module initializes the curses environment, sets up the WindowManager and
InputHandler, and runs the primary application and rendering loop.
"""

import curses
import sys

# Prevent Python from creating __pycache__ directories
sys.dont_write_bytecode = True

from lib.input_manager import InputManager
from lib.window_manager import WindowManager


def main(stdscr: curses.window) -> None:
    """Initialize and run the main application loop.

    :param stdscr: The main screen window provided by curses.wrapper.
    :type stdscr: curses.window
    """
    win_manager: WindowManager = WindowManager(stdscr)
    input_manager: InputManager = InputManager(stdscr, win_manager)
    win_manager.clear_screen()

    while True:
        # 1. Draw UI elements via window manager
        win_manager.draw()

        # 2. Handle user input and potential commands
        action = input_manager.manage_input()

        # 3. Check for termination signal
        if action == "quit":
            break


if __name__ == "__main__":
    curses.wrapper(main)
    # Clear the terminal buffer completely upon exit
    WindowManager.clear_screen()
