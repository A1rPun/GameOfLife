import curses
import time
from drawille import Canvas, getTerminalSize


def getGrid(w, h):
    return [[0 for x in range(w)] for y in range(h)]


def countNeighbors(grid, x, y, w, h):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + j + w) % w
            row = (y + i + h) % h
            sum += grid[row][col]
    sum -= grid[y][x]
    return sum


def updateGrid(grid, w, h):
    next = getGrid(w, h)
    for y in range(h):
        for x in range(w):
            state = grid[y][x]
            neighbors = countNeighbors(grid, x, y, w, h)
            if state == 0 and neighbors == 3:
                state = 1
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                state = 0
            next[y][x] = state
    return next


def drawGrid(canvas, grid, stdscr):
    stdscr.clear()
    canvas.clear()
    h = len(grid)
    w = len(grid[0])
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 1:
                canvas.set(x, y)
    stdscr.addstr(0, 0, canvas.frame(0, 0, w, h))
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    display = Canvas()
    grid = getGrid(WIDTH, HEIGHT)

    addPentomino(grid, int(WIDTH / 2), int(HEIGHT / 2))

    drawGrid(display, grid, stdscr)
    time.sleep(FRAMES)

    while True:
        grid = updateGrid(grid, WIDTH, HEIGHT)
        drawGrid(display, grid, stdscr)
        time.sleep(FRAMES)


# The R-pentomino shape
def addPentomino(grid, x=0, y=0):
    grid[y][x + 1] = 1
    grid[y][x + 2] = 1
    grid[y + 1][x] = 1
    grid[y + 1][x + 1] = 1
    grid[y + 2][x + 1] = 1


termSize = getTerminalSize()
WIDTH = min(100, termSize[0] * 2)
HEIGHT = min(100, termSize[1] * 4)
FRAMES = 1 / 30

if __name__ == '__main__':
    curses.wrapper(main)
