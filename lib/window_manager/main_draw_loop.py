import curses
import subprocess


class WindowManager:
    def __init__(self, stdscr: curses.window):
        self.clear_screen()
        self.stdscr: curses.window = stdscr
        self.win_l: curses.window | None = None
        self.win_r: curses.window | None = None
        self.rebuild_windows()

    def rebuild_windows(self):
        # Curses-Dimensionen aktualisieren
        curses.update_lines_cols()
        max_y, max_x = curses.LINES, curses.COLS
        third_x = max_x // 3

        # Alte Fenster verwerfen, falls sie existieren
        try:
            del self.win_l
            del self.win_r
        except AttributeError:
            pass

        # Neue Fenster erstellen
        self.win_l = curses.newwin(max_y, third_x, 0, 0)
        self.win_r = curses.newwin(max_y, max_x - third_x, 0, third_x)
        self.clear_screen()

    def draw(self):
        self.clear_screen()
        self.stdscr.clear()
        self.stdscr.refresh()

        if self.win_l:
            # Linkes Fenster zeichnen
            self.win_l.erase()
            self.win_l.box()
            self.win_l.addstr(1, 1, "Linkes Fenster")
            self.win_l.refresh()

        if self.win_r:
            # Rechtes Fenster zeichnen
            self.win_r.erase()
            self.win_r.box()
            self.win_r.addstr(1, 1, "Rechtes Fenster")
            self.win_r.refresh()

    @classmethod
    def clear_screen(cls):
        _ = subprocess.run("cls||clear", shell=True, check=False)
