# IFS TUI

A lightweight terminal user interface (TUI) built with Python's built-in `curses` library. It renders a resizable split-window layout, reacts live to terminal resize events, and ships with a built-in debug REPL for inspecting runtime state without killing the process.

## Features

- **Split-window layout** — the terminal is divided into a left pane (1/3 width) and a right pane (2/3 width), each with its own bordered `curses` window.
- **Live resize handling** — listens for `KEY_RESIZE` and rebuilds the window layout automatically when the terminal size changes.
- **Integrated debug console** — press `F5` to suspend the curses UI and drop into an interactive Python REPL (`code.interact`) with access to the current local scope, then resume the UI seamlessly on exit.
- **Clean shutdown** — press `F9` to quit; the screen is properly cleared on exit.
- **Cross-platform screen clearing** — uses `cls||clear` so it works whether run on Windows or Unix-like shells.
- **Convenient automatic documentation** — just run `cd docs; bash gen_documentation.sh` and open `html_docs/index.html` in e.g. Firefox. 

## Requirements

- Python 3.10+ (the codebase uses `X | None` union type hints)
- The `curses` module
  - Included by default in the Python standard library on Linux and macOS
  - On Windows, install the community backport: `pip install windows-curses`

## Project Structure

```
project_root/
├── main.py
└── lib/
    ├── colour_manager.py
    ├── input_manager.py
    └── window_manager.py
```

- **`main.py`** — application entry point; wraps the app in `curses.wrapper` and runs the main draw/input loop.
- **`lib/window_manager.py`** — `WindowManager` class; owns terminal geometry, window creation, resizing, and rendering.
- **`lib/colour_manager.py`** — `ColourManager` class; owns the process that each character has a predictable colour.
- **`lib/input_manager.py`** — `InputManager` class; captures keypresses, dispatches actions, and manages the debug REPL.

## Installation

```bash
git clone <repo-url>
cd <repo-folder>

# optional but recommended
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Windows only
pip install windows-curses
```

## Usage

```bash
python main.py
```

## Controls

| Key             | Action                                              |
|-----------------|------------------------------------------------------|
| `F5`            | Open the debug REPL to inspect runtime state          |
| `F9`            | Quit the application                                  |
| Terminal resize | Automatically rebuilds and redraws the window layout  |

## Debug REPL

At any point during runtime, press `F5` to suspend the curses interface and drop into a standard Python shell (`code.interact`). This is useful for inspecting `win_manager`, `stdscr`, or any other local state. Exit the REPL with `exit()` or `Ctrl+D` — the curses UI will be restored and the windows rebuilt automatically.

## Notes

- The two panes currently render placeholder German labels (`"Linkes Fenster"` / `"Rechtes Fenster"`, i.e. "Left window" / "Right window"). Update the `draw()` method in `main_draw_loop.py` to change this content.
- Type hints follow the modern `X | None` syntax and docstrings use Sphinx-style (`:param:`, `:type:`, `:ivar:`) reStructuredText, making the codebase ready for autodoc-based documentation generation.

## License

No license has been specified yet. I intend to, I'm just not sure, yet.
