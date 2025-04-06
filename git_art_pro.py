import os
import sys
import subprocess
from datetime import datetime, timedelta

START_DATE = datetime(2025, 4, 6)
CANVAS_WEEKS = 52
HEIGHT = 7
REPO_PATH = "."

INTENSITY = {
    " ": 0,
    ".": 2,
    ":": 5,
    "*": 9,
    "#": 14,
}

FRAME_WEEK_SPACING = 2

FONT = {
"A":[" ### ","#   #","#   #","#####","#   #","#   #","#   #"],
"B":["#### ","#   #","#   #","#### ","#   #","#   #","#### "],
"C":[" ####","#    ","#    ","#    ","#    ","#    "," ####"],
"D":["#### ","#   #","#   #","#   #","#   #","#   #","#### "],
"E":["#####","#    ","#    ","#####","#    ","#    ","#####"],
"F":["#####","#    ","#    ","#####","#    ","#    ","#    "],
"G":[" ####","#    ","#    ","#  ##","#   #","#   #"," ####"],
"H":["#   #","#   #","#   #","#####","#   #","#   #","#   #"],
"I":["#####","  #  ","  #  ","  #  ","  #  ","  #  ","#####"],
"J":["#####","    #","    #","    #","    #","#   #"," ### "],
"K":["#   #","#  # ","# #  ","##   ","# #  ","#  # ","#   #"],
"L":["#    ","#    ","#    ","#    ","#    ","#    ","#####"],
"M":["#   #","## ##","# # #","#   #","#   #","#   #","#   #"],
"N":["#   #","##  #","# # #","#  ##","#   #","#   #","#   #"],
"O":[" ### ","#   #","#   #","#   #","#   #","#   #"," ### "],
"P":["#### ","#   #","#   #","#### ","#    ","#    ","#    "],
"Q":[" ### ","#   #","#   #","#   #","# # #","#  # "," ## #"],
"R":["#### ","#   #","#   #","#### ","# #  ","#  # ","#   #"],
"S":[" ####","#    ","#    "," ### ","    #","    #","#### "],
"T":["#####","  #  ","  #  ","  #  ","  #  ","  #  ","  #  "],
"U":["#   #","#   #","#   #","#   #","#   #","#   #"," ### "],
"V":["#   #","#   #","#   #","#   #","#   #"," # # ","  #  "],
"W":["#   #","#   #","#   #","# # #","# # #","## ##","#   #"],
"X":["#   #","#   #"," # # ","  #  "," # # ","#   #","#   #"],
"Y":["#   #","#   #"," # # ","  #  ","  #  ","  #  ","  #  "],
"Z":["#####","    #","   # ","  #  "," #   ","#    ","#####"],

"0":[" ### ","#   #","#  ##","# # #","##  #","#   #"," ### "],
"1":["  #  "," ##  ","  #  ","  #  ","  #  ","  #  ","#####"],
"2":[" ### ","#   #","    #","   # ","  #  "," #   ","#####"],
"3":[" ### ","#   #","    #"," ### ","    #","#   #"," ### "],
"4":["   # ","  ## "," # # ","#  # ","#####","   # ","   # "],
"5":["#####","#    ","#    ","#### ","    #","#   #"," ### "],
"6":[" ### ","#   #","#    ","#### ","#   #","#   #"," ### "],
"7":["#####","    #","   # ","  #  "," #   "," #   "," #   "],
"8":[" ### ","#   #","#   #"," ### ","#   #","#   #"," ### "],
"9":[" ### ","#   #","#   #"," ####","    #","#   #"," ### "],

".":["     ","     ","     ","     ","     "," ### "," ### "],
",":["     ","     ","     ","     ","     "," ### ","  ## "],
"!":["  #  ","  #  ","  #  ","  #  ","  #  ","     ","  #  "],
"?":[" ### ","#   #","    #","   # ","  #  ","     ","  #  "],
"-":["     ","     ","     ","#####","     ","     ","     "],
"_":["     ","     ","     ","     ","     ","     ","#####"],
":":["     ","  #  ","     ","     ","     ","  #  ","     "],
"/":["    #","   # ","   # ","  #  "," #   "," #   ","#    "],

" ":["     "]*7
}

def get_char(c):
    return FONT.get(c.upper(), FONT[" "])

def build_text_grid(text):
    grid = [""] * HEIGHT
    for char in text:
        char_grid = get_char(char)
        for i in range(HEIGHT):
            grid[i] += char_grid[i] + "  "
    return grid

def center_grid(grid):
    width = len(grid[0])
    total = CANVAS_WEEKS
    if width >= total:
        return grid
    left = (total - width) // 2
    right = total - width - left
    return [(" " * left) + row + (" " * right) for row in grid]

def stylize(grid):
    styled = []
    for r, row in enumerate(grid):
        new_row = ""
        for c, ch in enumerate(row):
            if ch == "#":
                if r == 0 or r == len(grid) - 1:
                    new_row += "#"
                else:
                    p = (r * 3 + c * 5) % 5
                    if p == 0:
                        new_row += "#"
                    elif p == 1:
                        new_row += "*"
                    elif p == 2:
                        new_row += ":"
                    elif p == 3:
                        new_row += "."
                    else:
                        new_row += "#"
            else:
                new_row += " "
        styled.append(new_row)
    return styled

def make_commit(date, count):
    for i in range(count):
        date_str = date.strftime(f"%Y-%m-%dT12:00:{i:02d}")
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str
        with open("pixel.txt", "a") as f:
            f.write(date_str + "\n")
        subprocess.run(["git","add","."],cwd=REPO_PATH,stdout=subprocess.DEVNULL)
        subprocess.run(["git","commit","-m","pixel"],cwd=REPO_PATH,env=env,stdout=subprocess.DEVNULL)

def draw(grid, offset=0):
    for col in range(len(grid[0])):
        for row in range(HEIGHT):
            ch = grid[row][col]
            count = INTENSITY.get(ch, 0)
            if count > 0:
                date = START_DATE + timedelta(days=(col + offset)*7 + row)
                make_commit(date, count)

def animate(text):
    frames = []
    for i in range(1, len(text)+1):
        g = stylize(center_grid(build_text_grid(text[:i])))
        frames.append(g)
    base = build_text_grid(text)
    for s in range(10):
        g = stylize(center_grid([" "*s + r for r in base]))
        frames.append(g)
    for i,f in enumerate(frames):
        draw(f, i*FRAME_WEEK_SPACING)

def preview(grid):
    print()
    for r in grid:
        print(r)

def main():
    if len(sys.argv) < 2:
        return
    text = sys.argv[1]
    anim = "--animate" in sys.argv
    grid = stylize(center_grid(build_text_grid(text)))
    preview(grid)
    if input("\nProceed? (y/n): ").lower() != "y":
        return
    if anim:
        animate(text)
    else:
        draw(grid)
    print("\nDone")

if __name__ == "__main__":
    main()