import curses
import sys
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
    stdscr.nodelay(1)
    curses.curs_set(0)

    termSize = getTerminalSize()
    argsSize = len(sys.argv)
    WIDTH = min((int(sys.argv[1]) if argsSize > 1 else 64), termSize[0] * 2)
    HEIGHT = min((int(sys.argv[2]) if argsSize > 2 else 64), termSize[1] * 4)
    FRAMES = 4
    display = Canvas()
    grid = getGrid(WIDTH, HEIGHT)

    addPentomino(grid, int(WIDTH / 2), int(HEIGHT / 2))
    drawGrid(display, grid, stdscr)
    time.sleep(1. / FRAMES)

    while True:
        grid = updateGrid(grid, WIDTH, HEIGHT)
        drawGrid(display, grid, stdscr)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('s'):
            addPentomino(grid, int(WIDTH / 2), int(HEIGHT / 2))
        elif key == curses.KEY_UP:
            FRAMES += 1 if FRAMES < 60 else 0            
        elif key == curses.KEY_DOWN:
            FRAMES -= 1 if FRAMES > 2 else 0
        time.sleep(1. / FRAMES)


# The R-pentomino shape
def addPentomino(grid, x=0, y=0):
    grid[y][x + 1] = 1
    grid[y][x + 2] = 1
    grid[y + 1][x] = 1
    grid[y + 1][x + 1] = 1
    grid[y + 2][x + 1] = 1


if __name__ == '__main__':
    curses.wrapper(main)
