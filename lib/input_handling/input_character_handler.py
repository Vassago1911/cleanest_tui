"""User input and event management module.

Captures keyboard input, handles terminal resize events, and controls
interactive debugging sessions without mixing UI layout responsibilities.
"""

import code
import curses
import subprocess

from lib.window_manager.main_draw_loop import WindowManager


class InputHandler:
    """Handles character input, special function keys, and debugging hooks.

    :ivar stdscr: The main curses screen reference.
    :vartype stdscr: curses.window
    :ivar win_manager: Reference to the active window manager instance.
    :vartype win_manager: WindowManager
    """

    def __init__(self, stdscr: curses.window, win_manager: WindowManager) -> None:
        """Initialize the input handler with screen and window manager references.

        :param stdscr: The main screen window instance.
        :type stdscr: curses.window
        :param win_manager: The window manager instance to notify on resize.
        :type win_manager: WindowManager
        """
        self.stdscr: curses.window = stdscr
        self.win_manager: WindowManager = win_manager
        _ = curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(False)
        self.stdscr.clear()

    def _start_debug_session(self) -> None:
        """Temporarily suspend curses and spawn an interactive Python REPL.

        Allows inspection of runtime variables and state without terminating
        the core process. Restores the curses environment afterwards.
        """
        curses.endwin()
        self._system_clear()
        print("\n--- Python Debug REPL (Exit mit Strg+D / exit()) ---")
        code.interact(local=locals())

        # Restore curses state after exiting REPL
        self._system_clear()
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.doupdate()
        self.win_manager.rebuild_windows()

    def handle_input(self) -> str | None:
        """Capture user input events and dispatch corresponding actions.

        :return: Action command string ('quit', 'resize', etc.) or None.
        :rtype: str | None
        """
        c = self.stdscr.getch()
        self._system_clear()

        action = None

        if c == curses.KEY_RESIZE:
            self.win_manager.rebuild_windows()
            action = "resize"
        elif c in (curses.KEY_F5,):
            self._start_debug_session()
            action = "debug"
        elif c in (curses.KEY_F9,):
            action = "quit"

        self.stdscr.refresh()
        self._system_clear()
        return action

    @classmethod
    def _system_clear(cls) -> None:
        """Execute system-level screen reset."""
        _ = subprocess.run("cls||clear", shell=True, check=False)
