"""Deterministic per-character colouring for the pad content.

Provides a predictable character-to-colour mapping so that every occurrence
of a given character in the WindowManager's pad is rendered in the same
colour, no matter where it appears. The available colour range is chosen
according to the terminal's advertised colour capacity, queried through
curses/terminfo via ``curses.COLORS`` and ``curses.COLOR_PAIRS``, so the
module degrades gracefully on terminals that only advertise 8 or 16 colours
instead of the full 256-colour extended palette.
"""

import curses
import string
from typing import Final


class ColourManager:
    """Builds and applies a deterministic character -> colour mapping.

    :ivar stdscr: The main curses screen reference. Colour state itself is
        global to curses; this is kept only for parity with the other
        managers and possible future use.
    :vartype stdscr: curses.window
    :ivar has_colour: Whether the terminal advertises colour capacity at all.
    :vartype has_colour: bool
    :ivar capacity: The terminal's reported colour capacity
        (``curses.COLORS``), clamped to the number of colour pairs the
        terminal can actually hold (``curses.COLOR_PAIRS``).
    :vartype capacity: int
    :ivar palette: Ordered ``(name, curses colour index)`` pairs used to
        build colour pairs 1..N.
    :vartype palette: list[tuple[str, int]]
    :ivar char_pair: Mapping of a single character to its curses colour
        pair number.
    :vartype char_pair: dict[str, int]
    """

    # Fallback palette for terminals that only advertise 8/16 colours.
    _BASE_PALETTE: Final[tuple[tuple[str,int],...]] = (
        ("red", curses.COLOR_RED),
        ("green", curses.COLOR_GREEN),
        ("yellow", curses.COLOR_YELLOW),
        ("blue", curses.COLOR_BLUE),
        ("magenta", curses.COLOR_MAGENTA),
        ("cyan", curses.COLOR_CYAN),
        ("white", curses.COLOR_WHITE),
    )

    # Extended xterm-256 palette, used when curses.COLORS >= 256.
    # Numbers are standard xterm-256 colour-cube / greyscale indices.
    _EXTENDED_PALETTE: Final[tuple[tuple[str,int],...]] = (
        ("dark_blue", 18),
        ("lime_green", 46),
        ("dark_red", 88),
        ("gold", 220),
        ("orchid", 170),
        ("teal", 30),
        ("orange", 208),
        ("dark_violet", 92),
        ("spring_green", 48),
        ("deep_pink", 198),
        ("steel_blue", 67),
        ("chartreuse", 118),
        ("salmon", 209),
        ("turquoise", 80),
        ("slate_grey", 102),
        ("hot_pink", 205),
    )

    # A few fixed, human-chosen anchors so specific characters always land
    # on a specific named colour rather than whatever the hash produces.
    # Everything else is still fully deterministic, just derived from the
    # character code instead of pinned by hand.
    _MANUAL_OVERRIDES: Final[dict[str, str]] = {
        "Z": "dark_blue",
        "e": "lime_green",
    }

    def __init__(self, stdscr: curses.window) -> None:
        """Detect the terminal's colour capacity and build the char map.

        :param stdscr: The main screen window instance.
        :type stdscr: curses.window
        """
        self.stdscr: curses.window = stdscr
        self.has_colour: bool = curses.has_colors()
        self.capacity: int = 0
        self.palette: tuple[tuple[str, int],...] = ()
        self.char_pair: dict[str, int] = {}

        if not self.has_colour:
            return

        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass

        # curses.COLORS reflects the terminfo "colors" capability of the
        # current $TERM; curses.COLOR_PAIRS is the matching "pairs" capacity.
        # Clamping against both keeps us from registering pairs the
        # terminal cannot actually address.
        self.capacity = min(curses.COLORS, curses.COLOR_PAIRS - 1)
        self._build_palette()
        self._init_pairs()
        self._assign_characters()

    def _build_palette(self) -> None:
        """Pick the base or extended palette based on reported capacity."""
        source = self._EXTENDED_PALETTE if self.capacity >= 256 else self._BASE_PALETTE
        self.palette = source[: max(1, min(len(source), self.capacity))]

    def _init_pairs(self) -> None:
        """Register one curses colour pair (foreground only) per palette entry."""
        for index, (_, colour) in enumerate(self.palette, start=1):
            try:
                curses.init_pair(index, colour, -1)
            except curses.error:
                # Some terminals reject an out-of-range colour index even
                # after advertising support for it; fall back safely.
                curses.init_pair(index, curses.COLOR_WHITE, -1)

    def _assign_characters(self) -> None:
        """Deterministically map every printable character to a colour pair."""
        name_to_index = {name: i + 1 for i, (name, _) in enumerate(self.palette)}

        interesting_chars = ''.join(sorted(set( string.printable[:string.printable.find(' ')].upper() )))
        for char in interesting_chars:
            override = self._MANUAL_OVERRIDES.get(char)
            if override in name_to_index:
                self.char_pair[char] = name_to_index[override]
            else:
                self.char_pair[char] = (ord(char) % len(self.palette)) + 1

    def attr_for(self, char: str) -> int:
        """Return the curses attribute to use when drawing a character.

        :param char: A single character to look up.
        :type char: str
        :return: The character's colour pair attribute, or
            ``curses.A_NORMAL`` if colour is unsupported or the character
            has no mapping.
        :rtype: int
        """
        char = str.upper(char)
        if not self.has_colour:
            return curses.A_NORMAL
        pair_index = self.char_pair.get(char)
        return curses.color_pair(pair_index) if pair_index else curses.A_NORMAL

    def colourize_pad(self, pad: curses.window, height: int, width: int) -> None:
        """Recolour every cell of an existing pad in place, per character.

        Reads each cell back with ``inch()``, strips the existing attribute,
        and rewrites the same character with its assigned colour attribute.
        Text content is left untouched; only the rendering attribute changes.

        :param pad: The pad whose contents should be recoloured.
        :type pad: curses.window
        :param height: Number of rows to process.
        :type height: int
        :param width: Number of columns to process.
        :type width: int
        """
        if not self.has_colour:
            return

        for y in range(height):
            for x in range(width):
                try:
                    raw = pad.inch(y, x)
                except curses.error:
                    continue
                char = chr(raw & curses.A_CHARTEXT)
                try:
                    pad.addch(y, x, char, self.attr_for(char))
                except curses.error:
                    # Writing to the pad's very last cell raises in curses;
                    # harmless, just skip it.
                    pass
