import code
import curses

from lib.window_manager.main_draw_loop import WindowManager


class InputHandler:
    def __init__(self, stdscr: curses.window, window_manager: WindowManager):
        self.stdscr: curses.window = stdscr
        _ = curses.curs_set(0)
        self.stdscr.nodelay(False)
        self.window_manager: WindowManager = window_manager
        self.window_manager.clear_screen()

    def handle_input(self):
        """Verarbeitet den Input und gibt ein Action-Flag zurück ('quit', 'resize', 'debug', etc.)"""
        c = self.stdscr.getch()

        if c == curses.KEY_RESIZE:
            self.window_manager.rebuild_windows()
            return "resize"
        elif c == ord("d"):
            self._start_debug_session()
            return "debug"
        elif c == ord("q"):
            return "quit"

        return None

    def _start_debug_session(self):
        curses.endwin()
        self.window_manager.clear_screen()
        print("\n--- Python Debug REPL (Exit mit Strg+D / exit()) ---")
        code.interact(local=locals())

        # Nach REPL Curses-Zustand retten
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.doupdate()
        self.window_manager.rebuild_windows()
