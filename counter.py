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


# TODO 5: separate state from drawing (the design of main.py)
#
#   Goal: tasks only CHANGE state, one Renderer class DRAWS it.
#   After this, no task other than the renderer ever calls addstr/refresh.
#
#   Stage 1 - shared state.
#     Put everything the screen shows into one object: a dict, or better a
#     small @dataclass State with frames, total, paused, side_count.
#     app() and side_step() now only write to it. Nothing draws yet.
#     Checkpoint: print the state to a log file each second to see it change.
#
#   Stage 2 - the Renderer class.
#     class Renderer:
#         def __init__(self, stdscr, state): ...
#         def put(self, y, x, text, attr=0):   # the clipped addstr helper:
#             ...                              # skip if off-screen, trim text,
#                                              # catch curses.error ONCE, here
#         def draw(self): ...                  # erase(), put() each line from
#                                              # state, refresh(). Nothing else.
#     Checkpoint: replace every stdscr.addstr in your tasks with state writes,
#     and call renderer.draw() from ONE place. Output looks identical.
#
#   Stage 3 - one render task.
#     async def render_loop(renderer, running): draw, then await sleep(0.05).
#     amain() gathers three things now: input/logic, side_step, render_loop.
#     Question to answer: why can erase() safely live in draw() now, when it
#     would have fought the side task before?
#
#   Stage 4 - input in its own place.
#     Move getch()/key handling out of app() into on_key(key, state).
#     It only changes state (pause, quit), same as the tasks do.
#     Checkpoint: pausing still works, and `app` no longer touches stdscr.
#
#   Stage 5 - stretch.
#     Add Renderer.panel(y, x, h, w, title) drawn with box characters,
#     and put the counter in one panel and the side task in another.
#     Then add a task that appends a line to a list in state every second,
#     and show the last few lines in a "Log" panel.
#
#   Done when: you could add a third background task without touching
#   Renderer's drawing code except to show the new field.




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
