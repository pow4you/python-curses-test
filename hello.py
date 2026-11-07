"""
Rung 1: put text on the screen and wait for a key.

Run:  python hello.py        (quit with q)

curses.wrapper() sets the terminal up and, even if your code crashes, puts it
back afterwards. main.py does that by hand (initscr / endwin) because it also
runs an asyncio loop, but wrapper() is the right tool while you're learning.
"""
import curses


def main(stdscr):
    curses.curs_set(0)                      # hide the blinking cursor
    stdscr.addstr(2, 4, "hello, curses")    # addstr(row, col, text): row first!
    stdscr.addstr(4, 4, "press q to quit")

    while True:
        key = stdscr.getch()                # blocks until a key is pressed
        if key == ord("q"):
            break

        # TODO 1: show the key code you pressed on row 6, e.g. "last key: 113".
        #         Press arrows, Enter, Backspace, Esc. What are their codes?
        #         (hint: stdscr.keypad(True) makes arrows arrive as KEY_UP etc.
        #          instead of three raw bytes.)
        # TODO 2: make "hello, curses" bold (3rd argument: curses.A_BOLD).
        # TODO 3: center the text. stdscr.getmaxyx() returns (height, width).
        # TODO 4: add colour: curses.start_color(), curses.use_default_colors(),
        #         curses.init_pair(1, curses.COLOR_CYAN, -1),
        #         then attr = curses.color_pair(1).


curses.wrapper(main)
