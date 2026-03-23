<div align="center">

```
 ██████  ██ ████████      █████  ██████  ████████
██       ██    ██        ██   ██ ██   ██    ██
██   ███ ██    ██        ███████ ██████     ██
██    ██ ██    ██        ██   ██ ██   ██    ██
 ██████  ██    ██        ██   ██ ██   ██    ██
```

**Turn your GitHub contribution graph into a canvas.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-f59e0b?style=flat-square)](https://github.com/itsZapp/git-art/pulls)
[![Stars](https://img.shields.io/github/stars/itsZapp/git-art?style=flat-square&color=ef4444)](https://github.com/itsZapp/git-art/stargazers)

</div>

---

## What is this?

Your GitHub contribution graph is a 7×52 pixel grid of green squares. `git-art` lets you write text on it — or animate it — by backdating commits with pixel-perfect intensity.

People fake contributions to look active for recruiters. Why fake it when you can **hack it** to say whatever you want?

> **⚠️ Disclaimer:** This tool is purely for fun. Use it on a dedicated repo — don't nuke your actual work history. You've been warned.

---

## Preview

```
░░░█░░░█░░█████░░░
░░░█░░░█░░░░█░░░░░
░░░█░░░█░░░░█░░░░░      <- your contribution graph
░░░█████░░░░█░░░░░
░░░█░░░█░░░░█░░░░░      looks something like this
░░░█░░░█░░░░█░░░░░
░░░█░░░█░░█████░░░
```

Each `█` is a cluster of backdated commits. The more commits, the more intense (greener) the square appears on GitHub.

---

## Features

- **Text rendering** — Full A–Z, 0–9 and common punctuation drawn in a built-in bitmap pixel font
- **Intensity shading** — Letters use variable commit density to create depth and contrast within each character
- **Animation mode** — `--animate` builds text character-by-character with a scroll-in effect across weeks
- **Live preview** — See exactly what the graph will look like before a single commit is made
- **Zero dependencies** — Pure Python 3, uses only `git` and the standard library

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git installed and on your `PATH`
- A GitHub repo configured as your working directory (or a fresh one)

### Installation

```bash
git clone https://github.com/itsZapp/git-art.git
cd git-art
```

That's it. No pip installs. No virtualenvs. Just Python.

---

## Usage

### Basic — write text to the graph

```bash
python git_art_pro.py "HELLO"
```

git-art will print a preview of how it'll look on your contribution graph and ask for confirmation before making any commits.

### Animated — text scrolls in character by character

```bash
python git_art_pro.py "HELLO" --animate
```

In animate mode, each letter spawns its own frame offset by a few weeks, giving the illusion of text building up over time when viewed on your profile.

### Preview only — see without committing

Just say `n` when prompted:

```
Proceed? (y/n): n
```

---

## Configuration

All settings live at the top of `git_art_pro.py`:

| Variable             | Default                | Description                                   |
| -------------------- | ---------------------- | --------------------------------------------- |
| `START_DATE`         | `datetime(2026, 1, 4)` | The Sunday to start drawing from              |
| `CANVAS_WEEKS`       | `50`                   | How many weeks wide the canvas is             |
| `HEIGHT`             | `7`                    | Rows per column (always 7 for GitHub's graph) |
| `REPO_PATH`          | `"."`                  | Path to the target git repo                   |
| `FRAME_WEEK_SPACING` | `2`                    | Week gap between animation frames             |

### Intensity Map

Commit counts per cell are driven by the character used in the internal pixel map:

| Symbol      | Commits | Appearance        |
| ----------- | ------- | ----------------- |
| ` ` (space) | 0       | Empty / no square |
| `.`         | 2       | Light green       |
| `:`         | 5       | Medium green      |
| `*`         | 9       | Dark green        |
| `#`         | 14      | Maximum green     |

The stylizer automatically varies intensity within letter bodies for a natural, gradient-like shading effect.

---

## How It Works

1. **Font rendering** — `git-art` contains a hand-crafted 7-row bitmap font for every supported character. Each character is a list of 7 strings made of `#` and space.

2. **Grid construction** — Characters are concatenated into a full-width text grid, then centered on the `CANVAS_WEEKS`-wide canvas.

3. **Stylization** — The `stylize()` function replaces raw `#` marks with varying intensity symbols (`.`, `:`, `*`, `#`) based on position, creating depth.

4. **Commit generation** — For each non-empty cell, `make_commit()` writes to `pixel.txt` and runs backdated `git commit` calls with `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` set to the target date.

5. **Push** — After the script finishes, a regular `git push` sends everything to GitHub and your contribution graph updates.

---

## Supported Characters

```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
0 1 2 3 4 5 6 7 8 9
. , ! ? - _ : /   (space)
```

---

## Tips

**Pick a start date carefully.** `START_DATE` should be a Sunday that falls within the past year — GitHub only shows the last 52 weeks on your profile.

**Use a dedicated repo.** Running this on a repo you actually develop in will mix fake commits with real ones. Cleaner to keep them separate.

**Push after the script exits.** git-art only makes local commits. Don't forget `git push` to make the art appear on your profile.

**To clear it,** just delete the repo or hard-reset — all commits are in `pixel.txt` additions, so history is easy to identify and nuke.

---

## Roadmap

- [ ] Custom intensity maps / themes
- [ ] Image/PNG input mode (draw arbitrary 7×N bitmaps)
- [ ] GUI preview in the terminal (using `curses`)
- [ ] Per-frame delay control for animations
- [ ] `--undo` flag to reverse generated commits

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## License

MIT — do whatever you want, just don't blame me when your recruiter asks why your GitHub says `HIRE ME`.

---

<div align="center">

Made with 🟩 and questionable commit ethics by [itsZapp](https://github.com/itsZapp)

</div>
