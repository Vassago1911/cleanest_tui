import curses
import sys

sys.dont_write_bytecode = True
from lib.input_handling.input_character_handler import InputHandler
from lib.window_manager.main_draw_loop import WindowManager


def main(stdscr: curses.window):
    # initialise window and input manager
    win_manager: WindowManager = WindowManager(stdscr)
    input_handler: InputHandler = InputHandler(stdscr, win_manager)
    win_manager.clear_screen()
    while True:
        # 1. draw UI
        win_manager.draw()
        # 2. wait for input and get requested action
        action = input_handler.handle_input()
        # 3. if action is quit, break loop
        if action == "quit":
            break


if __name__ == "__main__":
    curses.wrapper(main)
    # clear the terminal finally
    WindowManager.clear_screen()
