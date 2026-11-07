# curses-ladder

Learning Python's `curses` by building small things, one rung at a time.
Each file starts as a tiny runnable program with `# TODO` exercises left for
me to fill in. The goal is to understand how a terminal UI like `lazygit` is
put together, and eventually to rebuild the launcher from the radiodish
`thermo` example myself.

## Running

```bash
python hello.py      # quit with q
python counter.py
python move.py
```

- Python 3.9+
- A Unix-like terminal (Linux, macOS). On Windows: `pip install windows-curses`
- Tip: run in a terminal with some room (60x12 or more); tiny windows make
  `addstr` raise errors, which is itself one of the lessons below.

*(Adjust the filenames above to match the ones in this repo.)*

## The ladder

| Rung | File | What it teaches | Status |
|------|------|-----------------|--------|
| 1 | `hello.py` | Drawing text, bold and colour, centering, reading key codes, `keypad(True)` | [x] done |
| 2 | `counter.py` | Non-blocking input loop, `erase()` vs `clear()`, pause as state, asyncio tasks running beside the UI | [x] done (TODO 5 open) |
| 3 | `move.py` | State changes on input, drawing only reads state; clamping, trails, snake | [ ] not started |

### Open exercises

- **Rung 2, TODO 5: separate state from drawing.** Tasks only change a shared
  state object; one `Renderer` class (with a clipped `put()` helper) is the
  only thing that touches the screen. Then move input handling into
  `on_key()`, and as a stretch add bordered panels and a log panel.
- **Rung 3:** all TODOs (other arrow keys, edge clamping, wasd/hjkl via a dict,
  trail, snake).

## Concepts I've picked up

- **Redraw everything every frame.** No widget tree: erase, print from
  current state, refresh.
- **`nodelay(True)`** makes `getch()` return `-1` instead of waiting, so one
  loop can read input, update, draw and sleep about 20 times a second.
- **`erase()` vs `clear()`.** `erase()` blanks curses' in-memory picture, and
  `refresh()` then sends only what changed. `clear()` also forces the real
  terminal to be wiped and repainted each frame, which flickers.
- **`keypad(True)`** turns arrow keys into single codes (`KEY_RIGHT` = 261).
  Without it they arrive as three raw bytes (27, 91, 67).
- **asyncio:** only one thing runs at a time, and control changes hands at
  each `await`. `time.sleep` / `curses.napms` never hand it over, so they
  freeze every other task. Use `await asyncio.sleep(...)`.
- **Tasks change state, one place draws.** Two tasks drawing at once is how
  curses programs go wrong.

## Gotchas I've hit

- `addstr` raises `curses.error` when text doesn't fit (small terminal, edge
  of the screen). Handle it once, in a `put()` helper.
- `addstr` only overwrites as many characters as the new text has. If the
  text gets shorter, old characters stay behind (e.g. leftover digits in a
  float). Fix: `erase()` each frame, or use a fixed-width format like `:.1f`.
- Operator precedence in centering: `x - len(t) // 2` means `x - (len(t) // 2)`,
  which is what I want, but it is worth knowing why.

## Where this is heading

- A snake game (rung 3 stretch).
- Rebuilding a small process launcher TUI: a process list, a log panel, a
  live dashboard, and a key bar with mouse support.
- Maybe comparing with [Textual](https://textual.textualize.io/), which hides
  the redraw loop, once I know what it's hiding.

## Resources

- [Curses Programming with Python (HOWTO)](https://docs.python.org/3/howto/curses.html)
- [`curses` module reference](https://docs.python.org/3/library/curses.html)
- [`asyncio` tasks and coroutines](https://docs.python.org/3/library/asyncio-task.html)
