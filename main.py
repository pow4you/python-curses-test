"""
Rung0: run curses following https://docs.python.org/3/howto/curses.html

Run:  python main.py
"""

import curses

def print_hi(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr(0,0,"Hi, curses!")

    stdscr.refresh()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #initialize curses
    stdscr = curses.initscr()

    #Usually curses applications turn off automatic echoing of keys to the screen, in order to be able to read keys and only display them under certain circumstances.
    curses.noecho()

    print_hi(stdscr)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
