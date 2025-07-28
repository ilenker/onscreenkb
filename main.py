import numpy as np
import curses
import time
import sys

width = 11
height = 4
#       123456789AB
row1 = "qwert  yuio"
row2 = "asdfg  hjkl"
row3 = "zxcvb  pnm["
            #0123456789ABCDEFGHIJKLMNOPQ
lpanechars = "qwertasdfgzxcvb"
rpanechars = "yuiohjklpnm["

#   keymap = np.zeros((width, height), dtype = int)

#   for i in range(width):
#       keymap[i][0] = ord(row1[i])
#       keymap[i][1] = ord(row2[i])
#       keymap[i][2] = ord(row3[i])
#       keymap[i][3] = ord(row4[i])

l_keymap = np.zeros((15), dtype = np.uint8)
l_keytimers = np.zeros((15), dtype = np.uint8)
for i in range(15):
    l_keymap[i] = ord(lpanechars[i])

r_keymap = np.zeros((12), dtype = np.uint8)
r_keytimers = np.zeros((12), dtype = np.uint8)
for i in range(12):
    r_keymap[i] = ord(rpanechars[i])

def init_curses():
    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(1)  # Hide the cursor
    return stdscr
 
def create_pane(stdscr, height, width, y, x):
    # Create a new window l_pane
    pane = stdscr.subwin(height, width, y, x)
    pane.box()  # Draw a border around the l_pane
    pane.refresh()  # Refresh the l_pane to display
    return pane

def main(stdscr):

    init_curses()
    stdscr.clear()
    l_pane = stdscr.subwin(4, 5, 1, 1)
    r_pane = stdscr.subwin(4, 4, 1, 9)
    debug_pane = stdscr.subwin(5, 12, 0, 0)
    debug_pane.box()
    spin_pane = stdscr.subwin(1, 2, 4, 5)

    l_pane.nodelay(True)  # Set l_pane to non-blocking input
    r_pane.nodelay(True)  # Set l_pane to non-blocking input
    spin_pane.nodelay(True)  # Set l_pane to non-blocking input
    debug_pane.nodelay(True)  # Set l_pane to non-blocking input
    
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    plain = curses.color_pair(1) 
    hilite = curses.color_pair(2)
    
    key = "2"

    stdscr.addstr(9, 5, "(^=__=^)")
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

    l_pane.leaveok(True)
    r_pane.leaveok(True)
    spin_pane.leaveok(True)
    l_pane.refresh()
    r_pane.refresh()

    while True:
        
        if i_s < 3:
            i_s += 0.03
        else: 
            i_s = 0
        spin_pane.addstr(0, 0, spinner[int(i_s)])
        spin_pane.noutrefresh()

        key = "2"
        
        # L PANE KEY TIMER LOGIC
        try:
            key = l_pane.getkey()  # Non-blocking input check
            for i in range(15):
                if chr(l_keymap[i])== key:
                    l_keytimers[i] = 5
            for i in range(12):
                if chr(r_keymap[i])== key:
                    r_keytimers[i] = 5
        except: key = "2"


        # Run through all of the lines in the l_pane
        for y in range(3):
            for x in range(5):
                if l_keytimers[(y*5)+x] == 5:
                    l_pane.addch(y, x, chr(l_keymap[(y*5)+x]), hilite)
                if l_keytimers[(y*5)+x] == 1:
                    l_pane.addch(y, x, chr(l_keymap[(y*5)+x]), plain)    

        for i in range(15):
            if l_keytimers[i] > 0:
                l_keytimers[i] -= 1
        
        # Run through all of the lines in the r_pane
        for y in range(3):
            for x in range(4):
                if r_keytimers[(y*4)+x] == 5:
                    r_pane.addch(y, x, chr(r_keymap[(y*4)+x]), hilite)
                if r_keytimers[(y*4)+x] == 1:
                    r_pane.addch(y, x, chr(r_keymap[(y*4)+x]), plain)    
        for i in range(12):
            if r_keytimers[i] > 0:
                r_keytimers[i] -= 1

        l_pane.noutrefresh()
        r_pane.noutrefresh()
        curses.doupdate()
        time.sleep(0.017)
curses.wrapper(main)

'''
    qwert    qwert
    00000    55555
1       When a key is pressed, change the corresponding key's value in the kb map
        to timer value, e.g. 5
1.1     each loop, reduce all the values in kbmap[i][1] by a fixed amount until they reach 0

2   Print the kb map
2.1     If the characters timer is 0, print the plain text 
2.2     else, print the highlighted text

        # Run through all of the lines in the l_pane
        for i in range(43): 
            if key == chr(keymap[i]):
                if l_pane.getyx()[1] < 10:      # Check for edge and wrap manually  
                    newy = l_pane.getyx()[0]    
                    newx = l_pane.getyx()[1] + 1
                else:
                    newy = l_pane.getyx()[0] + 1
                    newx = 0
                l_pane.move(newy, newx)         # Skip the position and don't update l_pane buffer
                #pane.addstr(chr(keymap[i]), hilite)
            else:
                l_pane.addstr(chr(keymap[i]), plain) # Print character, auto wrap with addstr
'''
