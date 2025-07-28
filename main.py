import numpy as np
import curses
import time
import sys

width = 11
height = 4
#       123456789AB
row1 = "qwert  yuio"
row2 = "asdfg  hjkl"
row3 = "zxcvb  pnm "
row4 = "    =  =   "
row = "qwert  yuioasdfg  hjklzxcvb  pnm     =  =   "
#   keymap = np.zeros((width, height), dtype = int)

#   for i in range(width):
#       keymap[i][0] = ord(row1[i])
#       keymap[i][1] = ord(row2[i])
#       keymap[i][2] = ord(row3[i])
#       keymap[i][3] = ord(row4[i])

keymap = np.zeros((44), dtype = np.uint8)
keytimers = np.zeros((44), dtype = np.uint8)
for i in range(44):
    keymap[i] = ord(row[i])

def init_curses():
    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(1)  # Hide the cursor
    return stdscr
 
def create_pane(stdscr, height, width, y, x):
    # Create a new window pane
    pane = stdscr.subwin(height, width, y, x)
    pane.box()  # Draw a border around the pane
    pane.refresh()  # Refresh the pane to display
    return pane

def disable_blocking(pane):
    # Disable blocking on input
    pane.nodelay(True)

def main(stdscr):

    init_curses()
    stdscr.clear()
    pane = stdscr.subwin(4, 11, 5, 5)
    debug_pane = stdscr.subwin(5, 12, 0, 0)
    debug_pane.box()
    spin_pane = stdscr.subwin(1, 2, 4, 5)
    disable_blocking(pane)  # Set pane to non-blocking input
    disable_blocking(spin_pane)  # Set pane to non-blocking input
    disable_blocking(debug_pane)  # Set pane to non-blocking input
    
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    plain = curses.color_pair(1) 
    hilite = curses.color_pair(2)
    key = "2"
    stdscr.addstr(9, 5, "(^=__=^)")
    stdscr.refresh()
    spinner = ["-", "\\", "|", "/"]
    i_s = 0
    curses.curs_set(0)
    # Run through all of the lines in the pane
    for i in range(43): 
        pane.addstr(chr(keymap[i]), plain) # Print character, auto wrap with addstr
    pane.leaveok(True)
    spin_pane.leaveok(True)
    pane.refresh()

    while True:
        

        if i_s < 3:
            i_s += 0.03
        else: 
            i_s = 0
        spin_pane.addstr(0, 0, spinner[int(i_s)])
        spin_pane.noutrefresh()

        key = "2"

        try:
            key = pane.getkey()  # Non-blocking input check
            for i in range(44):
                if chr(keymap[i])== key:
                    keytimers[i] = 5
        except: key = "2"

        for i in range(44):
            if keytimers[i] > 0:
                keytimers[i] -= 1
             
       #pane.clear()

        # Run through all of the lines in the pane
        for y in range(4):
            for x in range(11):
                if keytimers[(y*11)+x] > 0:
                    pane.addch(y, x, chr(keymap[(y*11)+x]), hilite)
                if keytimers[(y*11)+x] == 1:
                    pane.addch(y, x, chr(keymap[(y*11)+x]), plain) # Print character, auto wrap with addstr


        pane.noutrefresh()

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

        # Run through all of the lines in the pane
        for i in range(43): 
            if key == chr(keymap[i]):
                if pane.getyx()[1] < 10:      # Check for edge and wrap manually  
                    newy = pane.getyx()[0]    
                    newx = pane.getyx()[1] + 1
                else:
                    newy = pane.getyx()[0] + 1
                    newx = 0
                pane.move(newy, newx)         # Skip the position and don't update pane buffer
                #pane.addstr(chr(keymap[i]), hilite)
            else:
                pane.addstr(chr(keymap[i]), plain) # Print character, auto wrap with addstr
'''
