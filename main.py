import numpy as np
import curses
import time
import sys
import random
from wpm_functions import *

def get_words():
    with open("/home/ilenker/workspace/github.com/ilenker/onscreenkb/hundredwordlist") as f:
        file_contents = f.read()
    return file_contents                               

 
def create_pane(stdscr, height, width, y, x):
    # Create a new window l_pane
    pane = stdscr.subwin(height, width, y, x)
    pane.box()  # Draw a border around the l_pane
    pane.refresh()  # Refresh the l_pane to display
    return pane

def main(stdscr):
    # Initialisation 
    timer_length = 7
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(1)  # Hide the cursor
    lpanechars = "qwertasdfgzxcvb"
    rpanechars = "yuiohjklpnm["

    l_keymap = np.zeros((15), dtype = np.uint8)
    l_keytimers = np.zeros((15), dtype = np.uint8)
    for i in range(15):
        l_keymap[i] = ord(lpanechars[i])

    r_keymap = np.zeros((12), dtype = np.uint8)
    r_keytimers = np.zeros((12), dtype = np.uint8)
    for i in range(12):
        r_keymap[i] = ord(rpanechars[i])

    stdscr.clear()
    l_pane = stdscr.subwin(4, 5, 10, 4)
    r_pane = stdscr.subwin(4, 4, 10, 13)
    text_pane = stdscr.subwin(3, 42, 0, 0)
    text_pane.box()
    keyboard_display = stdscr.subwin(5, 28, 5, 4)
    spin_pane = stdscr.subwin(1, 10, 0, 1)

    l_pane.nodelay(True)  # Set panes to non-blocking input
    r_pane.nodelay(True)  
    spin_pane.nodelay(True) 
    text_pane.nodelay(True)  
    stdscr.nodelay(True)

    curses.init_color(9, 200, 200, 200)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(3, 9, curses.COLOR_BLACK)
    greyed = curses.color_pair(3)
    plain = curses.color_pair(1) 
    hilite = curses.color_pair(2)

    key = "2"

    stdscr.addstr(7, 4, "(^=__=^)")
    stdscr.refresh()
    spinner = ["-", "\\", "|", "/"]
    i_s = 0 # Spinner timer
    curses.curs_set(0)

                            # Run through all of the lines in the l_pane
    for i in range(15): 
        l_pane.addstr(chr(l_keymap[i]), plain) # Print character, auto wrap with addstr

                            # Run through all of the lines in the r_pane
    for i in range(12): 
        r_pane.addstr(chr(r_keymap[i]), plain) # Print character, auto wrap with addstr

    for i in range(3):
        for i in range(5):
            keyboard_display.addch("[", greyed)
            keyboard_display.addch(" ")
            keyboard_display.addch("]", greyed)
        keyboard_display.addstr(" ")
        for i in range(4):
            keyboard_display.addch("[", greyed)
            keyboard_display.addch(" ")
            keyboard_display.addch("]", greyed)

    l_pane.leaveok(True)
    r_pane.leaveok(True)
    spin_pane.leaveok(True)
    l_pane.refresh()
    r_pane.refresh()
    cursor_index = 1
    keyboard_display.refresh()

    sentence = ""
    wordlist = get_words().split("\n")
    for i in range(5):
        sentence += f"{wordlist[random.randint(0, 100)]} "
    text_pane.addstr(1, 1, sentence, greyed)

    epoch = time.perf_counter()
                                        # MAIN LOOP #
    while True:
        
        if i_s < 3:
            i_s += 0.20
        else: 
            i_s = 0
        spin_pane.addstr(0, 1, spinner[round(i_s)])


        # KEYS + TIMER LOGIC
        try:
            key = stdscr.getkey()  # Non-blocking input check
            for i in range(27):
                if i < 15:
                    if chr(l_keymap[i])== key:
                        text_pane.addch(1, cursor_index, key)
                        cursor_index += 1
                        l_keytimers[i] = timer_length
                else:
                    if chr(r_keymap[i-15])== key:
                        text_pane.addch(1, cursor_index, key)
                        cursor_index += 1
                        r_keytimers[i-15] = timer_length
            if key == "KEY_BACKSPACE":
                cursor_index -= 1
                text_pane.addch(1, cursor_index, sentence[cursor_index - 1], greyed)
            if key == " ":
                cursor_index += 1
            if key == "Q":
                text_pane.move(1, 1)
                text_pane.clrtoeol()
                cursor_index = 1 
                sentence = ""
                for i in range(5):
                    sentence += f"{wordlist[random.randint(0, 100)]} "
                text_pane.addstr(1, 1, sentence, greyed)
        except: key = "2"

        # Run through all of the lines in the l_pane
        for y in range(3):
            for x in range(5):
                if l_keytimers[(y*5)+x] == timer_length:
                    l_pane.addch(y, x, chr(l_keymap[(y*5)+x]), hilite)
                if l_keytimers[(y*5)+x] == 1:
                    l_pane.addch(y, x, chr(l_keymap[(y*5)+x]), plain)    

        for i in range(15):
            if l_keytimers[i] > 0:
                l_keytimers[i] -= 1
        
        # Run through all of the lines in the r_pane
        for y in range(3):
            for x in range(4):
                if r_keytimers[(y*4)+x] == timer_length:
                    r_pane.addch(y, x, chr(r_keymap[(y*4)+x]), hilite)
                if r_keytimers[(y*4)+x] == 1:
                    r_pane.addch(y, x, chr(r_keymap[(y*4)+x]), plain)    

        for i in range(12):
            if r_keytimers[i] > 0:
                r_keytimers[i] -= 1

        for j in range(3):
            for i in range(5):
                keyboard_display.addch(j, 1+i*3, l_pane.inch(j, i))
        for j in range(3):
            for i in range(4):
                keyboard_display.addch(j, 17+(i*3), r_pane.inch(j, i))

        text_pane.addstr(2, 0, get_wpm(get_test_time_s(epoch), chr_count))
        
        keyboard_display.noutrefresh()
        text_pane.noutrefresh() 
        #l_pane.noutrefresh()
        #r_pane.noutrefresh()
        spin_pane.noutrefresh()
        curses.doupdate()
        time.sleep(0.017)

curses.wrapper(main)

