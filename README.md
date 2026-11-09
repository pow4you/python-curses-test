# curses-ladder

Learning Python's `curses` by building small things, one rung at a time.
Each file started as a tiny runnable program with `# TODO` exercises left for
me to fill in. The goal: understand how a terminal UI like `lazygit` is put
together.

**Status: all three rungs complete** (finished 2026-11-09).

## Running

```bash
python hello.py      # quit with q
python counter.py    # q quits, p pauses
python move.py       # arrows / wasd / hjkl steer, q quits
```

- Python 3.9+
- A Unix-like terminal (Linux, macOS). On Windows: `pip install windows-curses`
- Give the terminal some room; tiny windows are a good way to find bugs.

*(Adjust the filenames above to match the ones in this repo.)*

## The ladder

| Rung | File | What I built | Status |
|------|------|--------------|--------|
| 1 | `hello.py` | Centered, bold, coloured text; live display of the last key code; arrow keys via `keypad(True)` | [x] done |
| 2 | `counter.py` | Frame counter and timer with pause, as separate asyncio tasks writing to a render buffer; one render task draws and refreshes at 20 fps | [x] done |
| 3 | `move.py` | An `@` steered with arrows/wasd/hjkl, clamped to the screen, with a fading trail, then a snake: keys only change the heading, a delta-time tick moves it | [x] done |

## Lessons learned

### Drawing

- **Redraw everything every frame.** There is no widget tree: erase, print
  from current state, refresh.
- **`erase()` vs `clear()`.** `erase()` blanks curses' in-memory picture and
  `refresh()` sends only what changed. `clear()` also forces the real terminal
  to be wiped and repainted each frame, which flickers.
- **`getch()` secretly refreshes.** If the window was modified, `getch()` calls
  `refresh()` first. My counters "ran slowly" because that was the only thing
  pushing changes to the screen, and its task slept 0.666 s. Fix: make the
  refresh an explicit job in one render task.
- **`addstr` only overwrites as many characters as the new text has.** Shorter
  text leaves old characters behind (leftover digits in a float). Fix: `erase()`
  each frame, `move()` + `clrtoeol()` per line, or a fixed-width format like `:.1f`.
- **Writing the bottom-right cell raises `curses.error`**, because the cursor
  can't advance past the end of the window. Catch it in one small `put()` helper.
- **One big `try/except` around many draws means the first failure skips
  everything after it.** In the snake, a trail dot in the corner made the `@`
  vanish. Give each `addstr` its own safety net.

### Input and timing

- **`nodelay(True)`** makes `getch()` return `-1` instead of waiting, so one
  loop can read input, update, draw and sleep.
- **A nodelay loop with no sleep spins at ~100% CPU.** Add `curses.napms(10)`,
  or look up `stdscr.timeout(ms)`, which replaces both `nodelay` and the sleep.
- **`keypad(True)`** turns arrows into single codes (`KEY_RIGHT` = 261).
  Without it they arrive as three raw bytes (27, 91, 67).
- **Delta-time ticks:** accumulate elapsed time and step when it passes the
  tick length. Subtract the tick (`elapsed -= dts`) instead of resetting to 0,
  or the speed drifts slower. `time.monotonic()` beats `time.time()` for this.

### Structure

- **State changes on input; drawing only reads state.** Commit the new state
  *before* drawing. I drew the `@` at the old position while the trail already
  held the new one, so a dot ran one cell ahead of it for a frame.
- **Tasks change state, one place draws.** Two tasks drawing at once is how
  curses programs go wrong.
- **Intent, candidate, commit.** `dx, dy` (what the player wants), `tx, ty`
  (where it would land after clamping), `x, y` (where it is) is the same
  structure real games use for collisions.
- **Keys change the heading, a timer moves the head.** That's the whole snake.
- **Tables beat `elif` chains for key bindings.** I had `a`/`h` pointing right
  and `j` in both "up" and "down", and the chain hid it. A `key -> (dx, dy)`
  dict would have shown it at a glance.
- **Check your assumptions about list contents.** `past[:-1]` assumed the last
  entry was the head, but "skip if already in the list" broke that when
  reversing over the trail.

### asyncio

- **Only one thing runs at a time, and control changes hands at each `await`.**
  `time.sleep` and `curses.napms` never hand it over, so they freeze every
  other task. Use `await asyncio.sleep(...)`.
- **Concurrency doesn't change what a line does.** The tasks all ran fine; none
  of them ever pushed the picture to the terminal.
- **Keep a reference to long-lived tasks** (`asyncio.gather`, or store the
  `create_task` result), and use an `asyncio.Event` as the shared "keep
  running" flag.

### Debugging

- Measure instead of guessing: how often does the screen actually change, how
  much CPU does the loop use, what is on the last row after reaching the corner?
- When a program "feels slow", ask what is *really* triggering the visible
  update before touching the code that computes the numbers.

## Where this could go next

- The snake with food, growth, self-collision and a score.
- The snake rebuilt with rung 2's pattern: tasks change state, one render task draws.
- My own small process-launcher TUI: a process list, a log panel, a live
  dashboard and a key bar with mouse support.
- [Textual](https://textual.textualize.io/), now that I know what it hides.

## Resources

- [Curses Programming with Python (HOWTO)](https://docs.python.org/3/howto/curses.html)
- [`curses` module reference](https://docs.python.org/3/library/curses.html)
- [`asyncio` tasks and coroutines](https://docs.python.org/3/library/asyncio-task.html)