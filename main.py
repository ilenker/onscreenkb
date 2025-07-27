import numpy as np
import curses
from curses import wrapper

width = 5
height = 5

screen_buffer = np.zeros((width, height), dtype = int)

cursor_x = 0
cursor_y = 0

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(10, 10, "wassup (^=__=^)")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
