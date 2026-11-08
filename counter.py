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


class Screen:
    def __init__(self, stdscr, running: asyncio.Event):
        self._render_buffer = ["","","","","","","","",""]

        self.stdscr = stdscr
        self.paused = False

        self.running = running

    def toggle_pause(self):
        self.paused = not self.paused


    def save_to_buffer(self, line, indent, text):
        self._render_buffer[line] = " "*indent + text


    def _drawline(self, line, indent, text):
        try:
            self.stdscr.move(line, indent)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(line, indent, text)
        except curses.error:
            pass



    def _render(self):
        for i, line in enumerate(self._render_buffer):
            self._drawline(i, 0 , line)

    async def render_loop(self):
        while self.running.is_set():
            self._render()

            self.stdscr.refresh()
            await asyncio.sleep(0.05)

    async def key_loop(self):
        while self.running.is_set():
            # 1. input: drain every key that's waiting (-1 means none left)
            key = self.stdscr.getch()
            if key == ord("q"):
                self.running.clear()
                break

            if key == ord("p"):
                self.toggle_pause()

            await asyncio.sleep(0.1)

#count frames
async def frames(screen: Screen):

    counter = 0
    while screen.running.is_set():

        if not screen.paused:
            counter += 1

        screen.save_to_buffer(2, 4, f"frames drawn: {counter}")

        await asyncio.sleep(0.666)

#timer
async def timer(screen: Screen):

    elapsed = 0
    last_frame = time.time()
    while screen.running.is_set():

        new_frame = time.time()
        # 2. update state
        if not screen.paused:
            delta = new_frame - last_frame
            elapsed += delta


        screen.save_to_buffer(3, 4, f"seconds elapsed: {elapsed}")

        last_frame = new_frame

        await asyncio.sleep(0.333)                   # ~20 frames per second


async def amain(stdscr):
    running = asyncio.Event()
    running.set()

    screen = Screen(stdscr, running)

    # Both coroutines run concurrently as asyncio Tasks.
    await asyncio.gather(
        timer(screen),
        frames(screen),
        screen.key_loop(),
        screen.render_loop(),
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
