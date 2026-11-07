"""
Rung 2: a screen that changes without any key presses.

Run:  python counter.py      (quit with q)

The trick from main.py: stdscr.nodelay(True) makes getch() return -1 instead
of waiting, so one loop can do "read input, update, draw, sleep" about 20
times a second.
"""
import asyncio
import curses
import time

# TODO 4 (the big one): rewrite this as `async def main()` with
#         `await asyncio.sleep(0.05)`, run a second task that prints
#         something else on row 4, and watch both update. That is
#         exactly how main.py lets the radiodish actor run alongside
#         the UI.
async def app(stdscr, running: asyncio.Event):

    pause_toggle = False
    start_time = time.perf_counter()
    elapsed = 0
    total = 0
    frames = 0
    while running.is_set():
        stdscr.erase()

        # 1. input: drain every key that's waiting (-1 means none left)
        key = stdscr.getch()
        if key == ord("q"):
            running.clear()
            break

        # TODO 3: make "p" pause and resume the counter (state, not drawing!).
        if key == ord("p"):
            pause_toggle = not pause_toggle
            if start_time != 0:
                elapsed = time.perf_counter() - start_time
                start_time = 0
            else:
                start_time = time.perf_counter()

        # 2. update state
        if not pause_toggle:
            total = elapsed
            if start_time != 0:
                total += time.perf_counter() - start_time
            frames += 1


        # 3. draw the whole screen from state
        try:
            stdscr.addstr(2, 4, f"frames drawn: {frames}")
        except curses.error:
            pass

        # TODO 1: show seconds elapsed instead (use time.time() at the start),
        #         so the number doesn't depend on how fast your loop runs.
        try:
            stdscr.addstr(3, 4, f"seconds elapsed: {total}")
        except curses.error:
            pass

        stdscr.refresh()

        await asyncio.sleep(0.05)                   # ~20 frames per second



async def side_step(stdscr, running: asyncio.Event):
    count = 0

    while running.is_set():

        try:
            stdscr.addstr(4, 4, f"side task update: {count}")
        except curses.error:
            pass

        stdscr.refresh()
        count += 1
        await asyncio.sleep(0.05)


async def amain(stdscr):
    running = asyncio.Event()
    running.set()

    # Both coroutines run concurrently as asyncio Tasks.
    await asyncio.gather(
        app(stdscr, running),
        side_step(stdscr, running),
    )


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)  # turned off blocking for keypress
    stdscr.keypad(True)  # allow for reading arrow keys correcly

    asyncio.run(amain(stdscr))


if __name__ == "__main__":
    curses.wrapper(main)

# TODO 2: change erase() to clear(), and the sleep to 0.001.
#         Does it flicker? Why does erase() + refresh() not?
# Answer: Yes it flickers and no i have no idea
#
# Corrected:
# erase() blanks curses’ in-memory picture of the screen.
# clear() does that and also tells curses to wipe the whole real terminal on the next refresh().
