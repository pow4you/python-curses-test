"""
Rung 1: put text on the screen and wait for a key.

Run:  python hello.py        (quit with q)

curses.wrapper() sets the terminal up and, even if your code crashes, puts it
back afterwards. main.py does that by hand (initscr / endwin) because it also
runs an asyncio loop, but wrapper() is the right tool while you're learning.
"""
import curses


def main(stdscr):
    stdscr.nodelay(True) # turned off blocking for keypress

    curses.curs_set(0)                      # hide the blinking cursor

    # TODO 4: add colour: curses.start_color(), curses.use_default_colors(),
    #         curses.init_pair(1, curses.COLOR_CYAN, -1),
    #         then attr = curses.color_pair(1).
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    stdscr.addstr(0, 0, "RED ALERT!", curses.color_pair(1))

    curses.init_pair(2, curses.COLOR_CYAN, 0)

    stored_key = "no key pressed"
    while True:
        stdscr.clear()
        key = stdscr.getch()  # blocks until a key is pressed

        if key == -1:
            key = stored_key
        else:
            stored_key = key

        if key == ord("q"):
            break


        # TODO 3: center the text. stdscr.getmaxyx() returns (height, width).
        height, width = stdscr.getmaxyx()

        xmiddle = width // 2
        ymiddle = height // 2


        # TODO 2: make "hello, curses" bold (3rd argument: curses.A_BOLD).
        stdscr.addstr(ymiddle-2, xmiddle-6, "hello, curses", curses.A_BOLD | curses.color_pair(2))  # addstr(row, col, text): row first!
        stdscr.addstr(ymiddle, xmiddle-7, "press q to quit")



        # TODO 1: show the key code you pressed on row 6, e.g. "last key: 113".
        #         Press arrows, Enter, Backspace, Esc. What are their codes?
        #         (hint: stdscr.keypad(True) makes arrows arrive as KEY_UP etc.
        #          instead of three raw bytes.)
        stdscr.addstr(ymiddle + 2, xmiddle - 6, "last key: {}".format(key))



        stdscr.refresh()

        curses.napms(50)





curses.wrapper(main)
