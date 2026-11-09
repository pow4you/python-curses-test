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

    past = []
    trail = 9
    x, y = 10, 1
    hx, hy = 0,1
    dts = 0.3 #delta tick speed
    last_frame = time.monotonic()
    elapsed = 0
    while True:
        key = stdscr.getch()

        # TODO 5: make the @ keep moving in its last direction on its own
        #         (a snake!). Direction becomes state; keys only change it.

        # TODO 1: handle KEY_LEFT, KEY_UP, KEY_DOWN the same way.
        # TODO 3: add "wasd" and "hjkl" as alternatives without duplicating
        #         the movement code (hint: a dict from key to (dx, dy)).
        if key == ord("q"):
            break
        elif key in (curses.KEY_RIGHT, ord("d"), ord("l")):
            hx, hy = 1, 0
        elif key in (curses.KEY_LEFT, ord("a"), ord("h")):
            hx, hy = -1, 0
        elif key in (curses.KEY_UP, ord("w"), ord("k")):
            hx, hy = 0, -1
        elif key in (curses.KEY_DOWN, ord("s"), ord("j")):
            hx, hy = 0, 1


        frame = time.monotonic()
        delta = frame - last_frame
        elapsed += delta
        last_frame = frame

        if elapsed >= dts:
            elapsed -= dts

            # TODO 2: clamp so the @ can't leave the screen. Use getmaxyx()
            #         inside the loop, so it also works after you resize.
            minx, miny = 0, 1
            maxy, maxx = stdscr.getmaxyx()

            tx = max(minx, min(x+hx, maxx-1))
            ty = max(miny, min(y+hy, maxy-1))

            # TODO 4: leave a trail: keep a list of past positions and draw them
            #         as "." before the "@". Cap its length so it fades.

            pos = (tx, ty)
            if pos not in past:
                past.append(pos)
            if len(past) > trail:
                past.pop(0)

            stdscr.erase()

            try:
                stdscr.addstr(0, 0, f"x={tx} y={ty}   arrows move, q quits")
            except curses.error:
                pass

            for pos in past[:-1]:
                try:
                    stdscr.addstr(pos[1], pos[0], ".")
                except curses.error:
                    pass

            try:
                stdscr.addstr(ty, tx, "@")
            except curses.error:
                pass

            x, y = tx, ty

            stdscr.refresh()
        #time.sleep(0.03)





curses.wrapper(main)
