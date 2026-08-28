"""Window and layout management for the TUI.

Handles terminal resizing, window generation, screen clearing, and rendering
procedures using the standard curses library.
"""

import curses

from lib.colour_manager import ColourManager


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
        self.stdscr: curses.window = stdscr
        self.colour_manager: ColourManager = ColourManager(self.stdscr)
        self.win_l: curses.window | None = None
        self.win_r: curses.window | None = None
        self.warn : curses.window | None = None
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
            del self.warn
            del self.max_x
            del self.max_y
            del self.sidebar_r
            del self.pad_content
            del self.pad_pos_y
        except AttributeError:
            pass

        self.max_x: int = max_x
        self.max_y: int = max_y
        self.sidebar_r: int = sidebar_r
        self.pad_pos_y: int = 0  # Aktuelle Scroll-Position oben
        self.pad_pos_x: int = 0

        if ( self.sidebar_r >= 10 ) and ( self.max_y >= 10 ):
            # Create new subwindows based on updated dimensions
            self.win_l = curses.newwin(self.max_y, self.sidebar_r, 0, 0)
            self.win_r = curses.newwin(self.max_y, self.max_x - self.sidebar_r, 0, self.sidebar_r)
            self.warn = None
            self.pad_content: curses.window = curses.newpad(100, 100)

            self.pad_content.addstr(0,0,'='+76*'='+'=')

            # Testzeilen in das Pad schreiben
            for i in range(50):
                self.pad_content.addstr(i+1, 0, '='+f"{i:02d}--{self.colour_manager.interesting_chars}--{i:02d}"+'=')
            self.pad_content.addstr(51,0,'='+76*'='+'=')

            self.colour_manager.colourize_pad(self.pad_content,100,100)

        else:
            self.win_l = None
            self.win_r = None
            self.warn = curses.newwin(self.max_y, self.max_x, 0, 0)

    def draw(self) -> None:
        """Render all active windows, borders, and content strings."""
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
            # self.win_r.addstr(1, 1, f"Rechtes F: \n   {self.max_y} lines \n x {self.max_x - self.sidebar_r} cols")
            self.win_r.box()
            self.win_r.refresh()
            # Berechne die verfügbare Höhe und Breite im rechten Fenster (abzüglich Rand)
            h, _ = self.win_r.getmaxyx()
            pad_height = h - 2

            # Das Pad in das rechte Fenster "blitten" (kopieren)
            # Syntax: pad.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
            # p = Pad-Koordinaten (Startpunkt des Ausschnitts)
            # s = Bildschirm-Koordinaten (Zielbereich im win_r)
            self.pad_content.refresh(
                  self.pad_pos_y
                , self.pad_pos_x # Start im Pad (oben links vom Ausschnitt)
                , 1
                , self.sidebar_r + 1
                , pad_height
                , self.sidebar_r * 4 - 2
            )

        if self.warn:
            self.warn.erase()
            self.warn.addstr(1,1,'bitte\nmehr\nplatz!')
            self.warn.refresh()

    def scroll_pad_updown(self, direction: int) -> None:
          """Scrollt das Pad nach oben (-1) oder unten (+1)."""
          self.pad_pos_y += direction
          # Begrenzung einhalten (max Zeilenanzahl minus sichtbarer Fensterhöhe)
          self.pad_pos_y = max(0, min(self.pad_pos_y, 52 - (self.max_y - 2)))
          self.draw()

    def scroll_pad_leftright(self, direction: int) -> None:
          """Scrollt das Pad nach oben (-1) oder unten (+1)."""
          self.pad_pos_x += direction
          # Begrenzung einhalten (max Zeilenanzahl minus sichtbarer Fensterhöhe)
          self.pad_pos_x = max(0, min(self.pad_pos_x, 50 - (self.max_x - 2)))
          self.draw()
