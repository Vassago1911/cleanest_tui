"""Window and layout management for the TUI.

Handles terminal resizing, window generation, screen clearing, and rendering
procedures using the standard curses library.
"""

import curses
import subprocess


class WindowManager:
    """Manages creation, layout partitioning, and rendering of terminal windows.

    :ivar stdscr: The main curses screen reference.
    :vartype stdscr: curses.window
    :ivar win_l: Left subwindow partition.
    :vartype win_l: curses.window | None
    :ivar win_r: Right subwindow partition.
    :vartype win_r: curses.window | None
    """

    def __init__(self, stdscr: curses.window) -> None:
        """Initialize the WindowManager and build initial subwindows.

        :param stdscr: The main screen window instance.
        :type stdscr: curses.window
        """
        self.clear_screen()
        self.stdscr: curses.window = stdscr
        self.win_l: curses.window | None = None
        self.win_r: curses.window | None = None
        self.rebuild_windows()

    def rebuild_windows(self) -> None:
        """Recalculate terminal geometry and recreate all subwindows.

        Safely destroys old window instances if they exist, updates internal
        curses dimensions, and splits the screen into proportional sections.
        """
        curses.update_lines_cols()
        max_y, max_x = curses.LINES, curses.COLS
        third_x = max_x // 3

        # Safely discard existing windows to prevent memory leaks
        try:
            del self.win_l
            del self.win_r
        except AttributeError:
            pass

        # Create new subwindows based on updated dimensions
        self.win_l = curses.newwin(max_y, third_x, 0, 0)
        self.win_r = curses.newwin(max_y, max_x - third_x, 0, third_x)
        self.clear_screen()

    def draw(self) -> None:
        """Render all active windows, borders, and content strings."""
        self.clear_screen()
        self.stdscr.clear()
        self.stdscr.refresh()

        if self.win_l:
            self.win_l.erase()
            self.win_l.box()
            self.win_l.addstr(1, 1, "Linkes Fenster")
            self.win_l.refresh()

        if self.win_r:
            self.win_r.erase()
            self.win_r.box()
            self.win_r.addstr(1, 1, "Rechtes Fenster")
            self.win_r.refresh()

    @classmethod
    def clear_screen(cls) -> None:
        """Clear the terminal screen using system-level commands."""
        _ = subprocess.run("cls||clear", shell=True, check=False)
