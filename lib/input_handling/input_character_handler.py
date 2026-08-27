import code
import curses

from lib.window_manager.main_draw_loop import clear_screen


class InputHandler:
    def __init__(self, stdscr: curses.window):
        clear_screen()
        self.stdscr: curses.window = stdscr
        _ = curses.curs_set(0)  # Unsichtbarer Cursor
        self.stdscr.nodelay(False)
        self.stdscr.clear()
        self._handle_resize()

    def _create_windows(self):
        max_y, max_x = curses.LINES, curses.COLS
        third_x = max_x // 3
        win_left = curses.newwin(max_y, third_x, 0, 0)
        win_right = curses.newwin(max_y, 2 * third_x, 0, third_x)
        return win_left, win_right

    def _handle_resize(self):
        # Curses informieren, dass sich die Terminalgröße geändert hat
        curses.update_lines_cols()
        try:
            del self.win_l
            del self.win_r
        except AttributeError as _:
            pass

        # Neue Fenster anhand der aktuellen Dimensionen erstellen
        windows: tuple[curses.window, curses.window] = self._create_windows()
        self.win_l: curses.window = windows[0]
        self.win_r: curses.window = windows[1]

    def _start_debug_session(self):
        # 1. Curses temporär beenden für die REPL
        curses.endwin()
        clear_screen()
        print("\n--- Python Debug REPL (Exit mit Strg+D / exit()) ---")
        code.interact(local=locals())

        # 2. Curses nach dem Verlassen wiederherstellen
        clear_screen()
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.doupdate()
        self._handle_resize()

    def draw(self):
        self.stdscr.clear()
        self.stdscr.refresh()

        # Linkes Fenster zeichnen
        self.win_l.erase()
        self.win_l.box()
        self.win_l.addstr(1, 1, "Linkes Fenster")
        self.win_l.refresh()

        # Rechtes Fenster zeichnen
        self.win_r.erase()
        self.win_r.box()
        self.win_r.addstr(1, 1, "Rechtes Fenster")
        self.win_r.refresh()

    def check_user_input(self):
        quit_request = False
        c = self.stdscr.getch()
        clear_screen()
        if c == curses.KEY_RESIZE:
            self._handle_resize()
        elif c in (curses.KEY_F5,):
            self._start_debug_session()
        elif c in (curses.KEY_F9,):
            quit_request = True
        return quit_request
