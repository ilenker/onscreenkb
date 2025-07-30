import numpy as np
import curses
import time
import sys
import random
from wpmfunctions import *

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
    timer_length = 5
    mistakes = 0
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(1)  # Hide the cursor
    lpanechars = "qwertasdfgzxcvb"
    rpanechars = "yuiohjklpnm["

    messages = get_messages()

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
    curses.init_pair(4, curses.COLOR_RED, 9)
    greyed = curses.color_pair(3)
    plain = curses.color_pair(1) 
    hilite = curses.color_pair(2)
    mistake = curses.color_pair(4)

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
    cursor_index = 1
    keyboard_display.refresh()

    sentence = ""
    max_sentence_length = 40
    wordlist = get_words().split("\n")
    wordlist.pop()
    sentence = generate_new_sentence(max_sentence_length, wordlist)
    text_pane.addstr(1, 1, sentence, greyed)

    epoch = 0 
    chr_count = 0
    test_started = 0
                                        # MAIN LOOP #
    while True:
        
        # Spinner and WPM display
        if i_s < 20:
            if i_s % 5 == 0:
                spin_pane.addstr(0, 1, spinner[i_s // 5])
                if not is_test_complete(cursor_index, sentence)[0] and test_started == 1:
                    text_pane.addstr(2, 0, str(get_wpm(chr_count, epoch)) + " ")
            i_s += 1 
        else: 
            i_s = 0

            # Results Screen State
        if is_test_complete(cursor_index, sentence)[0] and test_started == 1:
            test_started = 0
            text_pane.addstr(0, 7, messages[random.randint(0, len(messages)-1)])
            stdscr.addstr(4, 0, "Time: " + str(round(get_test_time_s(epoch), 1)))
            accuracy = ((max_sentence_length - mistakes) / max_sentence_length) * 100
            stdscr.addstr(3, 0, f"Accuracy: {accuracy}%")

        # KEYS + TIMER LOGIC
        try:
            key = stdscr.getkey()  
            for i in range(27):
                if i < 15:
                    if chr(l_keymap[i])== key:

                        if test_started == 0 and cursor_index == 1:
                            test_started = 1
                            mistakes = 0
                            epoch = time.perf_counter()

                        if is_type_error(text_pane, cursor_index, key):
                            text_pane.addch(1, cursor_index, key, mistake)
                            mistakes += 1 
                        else:
                            text_pane.addch(1, cursor_index, key)

                        cursor_index += 1
                        chr_count += 1
                        l_keytimers[i] = timer_length
                else:
                    if chr(r_keymap[i-15])== key:
                        
                        if test_started == 0 and cursor_index == 1:
                            test_started = 1
                            mistakes = 0
                            epoch = time.perf_counter()

                        if is_type_error(text_pane, cursor_index, key):
                            text_pane.addch(1, cursor_index, key, mistake)
                            mistakes += 1 
                        else:
                            text_pane.addch(1, cursor_index, key)

                        cursor_index += 1
                        chr_count += 1
                        r_keytimers[i-15] = timer_length
                        
            if key == "KEY_BACKSPACE":
                if cursor_index > 1:
                    text_pane.chgat(1, cursor_index, 1, text_pane.inch(1, cursor_index) ^ curses.A_UNDERLINE)
                    cursor_index -= 1
                    text_pane.addch(1, cursor_index, sentence[cursor_index - 1], greyed)

            if key == " ":
                text_pane.chgat(1, cursor_index, 1, text_pane.inch(1, cursor_index) ^ curses.A_UNDERLINE)
                cursor_index += 1
                chr_count += 1

            if key == "\t":
                clear_lines(stdscr, [3, 4])
                text_pane.move(1, 1)
                text_pane.clrtoeol()
                cursor_index = 1 
                sentence = generate_new_sentence(max_sentence_length, wordlist)
                text_pane.addstr(1, 1, sentence, greyed)
                chr_count = 0 
                epoch = time.perf_counter()
                text_pane.box()
            set_cursor_visual(text_pane, cursor_index)

        except: key = "#"

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
        # Decrement timers
        for i in range(12):
            if r_keytimers[i] > 0:
                r_keytimers[i] -= 1

        # Render visible keyboard display
        for j in range(3):
            for i in range(5):
                if is_next_chr(text_pane, l_pane, j, i, cursor_index):
                    keyboard_display.addch(j, 1+i*3, l_pane.inch(j, i), 0 | curses.A_REVERSE)
                else:
                    keyboard_display.addch(j, 1+i*3, l_pane.inch(j, i))
        for j in range(3):
            for i in range(4):
                if is_next_chr(text_pane, r_pane, j, i, cursor_index):
                    keyboard_display.addch(j, 17+(i*3), r_pane.inch(j, i), 0 | curses.A_REVERSE)
                else:
                    keyboard_display.addch(j, 17+(i*3), r_pane.inch(j, i))

        keyboard_display.noutrefresh()
        text_pane.noutrefresh() 
        spin_pane.noutrefresh()
        curses.doupdate()
        time.sleep(0.017)

curses.wrapper(main)
