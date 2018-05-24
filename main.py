import sys,os
import curses

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # stdscr.chgat(height-1,0,width-1,curses.A_REVERSE)
        # stdscr.chgat(height-2,1,width-3,curses.A_REVERSE)
        # stdscr.chgat(height-3,2,width-5,curses.A_REVERSE)


        #T Rex design


        stdscr.chgat(26,25,8 ,curses.A_REVERSE)
        stdscr.chgat(27,24,2,curses.A_REVERSE)
        stdscr.chgat(27,27,9,curses.A_REVERSE)
        stdscr.chgat(28,24,11,curses.A_REVERSE)
        stdscr.chgat(29,24,11,curses.A_REVERSE)
        stdscr.chgat(30,24,11,curses.A_REVERSE)
        stdscr.chgat(31,24,3,curses.A_REVERSE)
        stdscr.chgat(32,24,7,curses.A_REVERSE)

        #body
        stdscr.chgat(33,23,3,curses.A_REVERSE)
        stdscr.chgat(34,22,5,curses.A_REVERSE)
        stdscr.chgat(35,20,8,curses.A_REVERSE)
        stdscr.chgat(36,19,13,curses.A_REVERSE)
        stdscr.chgat(37,18,10,curses.A_REVERSE)
        stdscr.chgat(37,31,1,curses.A_REVERSE)
        stdscr.chgat(38,18,9,curses.A_REVERSE)

        # tail
        stdscr.chgat(39,12,15,curses.A_REVERSE)
        stdscr.chgat(38,12,3,curses.A_REVERSE)
        stdscr.chgat(37,12,2,curses.A_REVERSE)
        stdscr.chgat(36,12,1,curses.A_REVERSE)

        #down body
        stdscr.chgat(40,13,13,curses.A_REVERSE)
        stdscr.chgat(41,14,11,curses.A_REVERSE)

        #legs
        stdscr.chgat(42,16,3,curses.A_REVERSE)
        stdscr.chgat(42,21,3,curses.A_REVERSE)
        stdscr.chgat(43,17,2,curses.A_REVERSE)
        stdscr.chgat(43,22,2,curses.A_REVERSE)

        #ankles
        stdscr.chgat(44,18,2,curses.A_REVERSE)
        stdscr.chgat(44,23,2,curses.A_REVERSE)



        # stdscr.hline(height-10,0,"_",width//2-4)
        # stdscr.chgat(height-10,width//2-4,1,curses.A_REVERSE)
        # stdscr.chgat(height-11,width//2-3,1,curses.A_REVERSE)
        # stdscr.chgat(height-12,width//2-2,1,curses.A_REVERSE)
        # stdscr.chgat(height-12,width//2-1,1,curses.A_REVERSE)
        # stdscr.chgat(height-12,width//2,1,curses.A_REVERSE)
        # stdscr.chgat(height-12,width//2+1,1,curses.A_REVERSE)
        # stdscr.chgat(height-12,width//2+2,1,curses.A_REVERSE)
        # stdscr.chgat(height-11,width//2+3,1,curses.A_REVERSE)
        # stdscr.chgat(height-10,width//2+4,1,curses.A_REVERSE)
        # stdscr.hline(height-10,width//2+5,"_",width//2-4)




        stdscr.move(0,0)



        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()