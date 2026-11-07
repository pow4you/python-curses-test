"""
Rung 2: a screen that changes without any key presses.

Run:  python counter.py      (quit with q)

The trick from main.py: stdscr.nodelay(True) makes getch() return -1 instead
of waiting, so one loop can do "read input, update, draw, sleep" about 20
times a second.
"""
import curses
import time


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)  # turned off blocking for keypress
    stdscr.keypad(True)  # allow for reading arrow keys correcly


    start_time = time.time()
    frames = 0
    while True:
        stdscr.clear()


        # 1. input: drain every key that's waiting (-1 means none left)
        key = stdscr.getch()
        if key == ord("q"):
            break

        # 2. update state
        frames += 1

        # 3. draw the whole screen from state

        stdscr.addstr(2, 4, f"frames drawn: {frames}")

        # TODO 1: show seconds elapsed instead (use time.time() at the start),
        #         so the number doesn't depend on how fast your loop runs.
        seconds = time.time() - start_time
        stdscr.addstr(3, 4, f"seconds elapsed: {seconds}")
        stdscr.refresh()

        time.sleep(0.001)                    # ~20 frames per second





        # TODO 2: change erase() to clear(), and the sleep to 0.001.
        #         Does it flicker? Why does erase() + refresh() not?
        # Answer: Yes it flickers and no i have no idea

        # TODO 3: make "p" pause and resume the counter (state, not drawing!).
        # TODO 4 (the big one): rewrite this as `async def main()` with
        #         `await asyncio.sleep(0.05)`, run a second task that prints
        #         something else on row 4, and watch both update. That is
        #         exactly how main.py lets the radiodish actor run alongside
        #         the UI.


curses.wrapper(main)
