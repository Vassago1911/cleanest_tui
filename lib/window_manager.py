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
        sidebar_r = max_x // 4

        # Safely discard existing windows to prevent memory leaks
        try:
            del self.win_l
            del self.win_r
            del self.max_x
            del self.max_y
            del self.sidebar_r
        except AttributeError:
            pass

        self.max_x : int = max_x
        self.max_y : int = max_y
        self.sidebar_r : int = sidebar_r
        # Create new subwindows based on updated dimensions
        self.win_l = curses.newwin(self.max_y, self.sidebar_r, 0, 0)
        self.win_r = curses.newwin(self.max_y, self.max_x - self.sidebar_r, 0, self.sidebar_r)
        self.clear_screen()

    def draw(self) -> None:
        """Render all active windows, borders, and content strings."""
        self.clear_screen()
        self.stdscr.clear()
        self.stdscr.refresh()

        if self.win_l:
            self.win_l.erase()
            self.win_l.addstr(1, 1,  "Linkes Fe:")
            self.win_l.addstr(2, 1, f"  {self.max_y} lines")
            self.win_l.addstr(3, 1, f"x {self.sidebar_r} cols")
            self.win_l.box()
            self.win_l.refresh()

        if self.win_r:
            self.win_r.erase()
            self.win_r.addstr(1, 1, f"Rechtes F: \n   {self.max_y} lines \n x {self.max_x - self.sidebar_r} cols")
            self.win_r.box()
            self.win_r.refresh()

    @classmethod
    def clear_screen(cls) -> None:
        """Clear the terminal screen using system-level commands."""
        _ = subprocess.run("cls||clear", shell=True, check=False)
