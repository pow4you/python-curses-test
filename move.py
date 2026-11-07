"""
Rung 3: state changes on input, drawing just reads the state.

Run:  python move.py         (arrow keys move the @, q quits)

Notice the split: handling keys only changes (x, y); drawing only reads
them. main.py keeps the same split in on_key() and draw().
"""
import curses
import time


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)                     # arrows arrive as curses.KEY_*
    stdscr.nodelay(True)

    x, y = 10, 5
    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_RIGHT:
            x += 1
        # TODO 1: handle KEY_LEFT, KEY_UP, KEY_DOWN the same way.
        # TODO 2: clamp so the @ can't leave the screen. Use getmaxyx()
        #         inside the loop, so it also works after you resize.
        # TODO 3: add "wasd" and "hjkl" as alternatives without duplicating
        #         the movement code (hint: a dict from key to (dx, dy)).

        stdscr.erase()
        stdscr.addstr(0, 0, f"x={x} y={y}   arrows move, q quits")
        stdscr.addstr(y, x, "@")             # crashes at the edge: TODO 2 fixes it
        stdscr.refresh()
        time.sleep(0.03)

        # TODO 4: leave a trail: keep a list of past positions and draw them
        #         as "." before the "@". Cap its length so it fades.
        # TODO 5: make the @ keep moving in its last direction on its own
        #         (a snake!). Direction becomes state; keys only change it.


curses.wrapper(main)
