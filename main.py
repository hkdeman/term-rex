import sys,os
import curses
import time
import threading
from enum import Enum

class Time(Enum):
    IDEAL = 0.01
    JUMP = 0.012

k = 0
global_stdscr = None

JUMP_HEIGHT = 14
IDLE_FRAMES = [(28,25,7),(29,24,2),(29,27,6),(30,24,9),(31,24,3),(32,24,7),
        (33,23,3),(34,22,5),(35,20,8),(36,19,13),(37,18,10),(37,31,1),(38,18,9),
        (39,12,15),(38,12,3),(37,12,2),(36,12,1),
        (40,13,13),(41,14,11),
        (42,16,3),(42,21,3),(43,17,2),(43,22,2),
        (44,18,2),(44,23,2)]
WALK_ONE_FRAMES = [(28,25,7),(29,24,2),(29,27,6),(30,24,9),(31,24,3),(32,24,7),
        (33,23,3),(34,22,5),(35,20,8),(36,19,13),(37,18,10),(37,31,1),(38,18,9),
        (39,12,15),(38,12,3),(37,12,2),(36,12,1),
        (40,13,13),(41,14,11),
        (42,16,3),(42,21,3),(43,17,2),(43,22,3),
        (44,18,2)]
WALK_TWO_FRAMES = [(28,25,7),(29,24,2),(29,27,6),(30,24,9),(31,24,3),(32,24,7),
        (33,23,3),(34,22,5),(35,20,8),(36,19,13),(37,18,10),(37,31,1),(38,18,9),
        (39,12,15),(38,12,3),(37,12,2),(36,12,1),
        (40,13,13),(41,14,11),
        (42,16,3),(42,21,3),(43,17,3),(43,22,2),
        (44, 23, 2)]

GAME_OVER = False
JUMP_SENSITIVITY = 0.002
WALK_ANIMATE_SENSITIVITY = 5
JUMP_ANIMATE_SENSITIVITY = 1


idle = True
SLEEP_TIME = Time.IDEAL.value

def get_input():
    global k,global_stdscr,idle,GAME_OVER
    while k!=ord('q') and not GAME_OVER:
        k = global_stdscr.getch()
        if not idle and k==curses.KEY_UP:
            k=0

def setup_foreground(stdscr,height,width):
    stdscr.hline(height-11, 0, "_", width)


def create_obstacles(obstacle_index,stdscr,height):
    #stem
    stdscr.chgat(height - 11, obstacle_index, 1, curses.A_REVERSE)
    stdscr.chgat(height - 12, obstacle_index, 1, curses.A_REVERSE)
    stdscr.chgat(height - 13, obstacle_index, 1, curses.A_REVERSE)
    stdscr.chgat(height - 14, obstacle_index, 1, curses.A_REVERSE)
    stdscr.chgat(height - 15, obstacle_index, 1, curses.A_REVERSE)

    #right branch
    stdscr.chgat(height - 13, obstacle_index+1, 1, curses.A_REVERSE)
    stdscr.chgat(height - 13, obstacle_index+2, 1, curses.A_REVERSE)
    stdscr.chgat(height - 14, obstacle_index+2, 1, curses.A_REVERSE)

    #left branch
    stdscr.chgat(height - 12, obstacle_index-1, 1, curses.A_REVERSE)
    stdscr.chgat(height - 12, obstacle_index-2, 1, curses.A_REVERSE)
    stdscr.chgat(height - 13, obstacle_index-2, 1, curses.A_REVERSE)


def check_collision(obstacle_index,jump_height):
    global GAME_OVER
    for frame in IDLE_FRAMES[13:16]:
        if frame[1]+frame[2] == obstacle_index and jump_height < 3:
            GAME_OVER= True


def draw_menu(stdscr):
    global k,global_stdscr,idle,SLEEP_TIME,GAME_OVER
    global_stdscr = stdscr
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    height, width = global_stdscr.getmaxyx()
    obstacle_index = width - 5
    index = 0
    jump = going_down = going_up = on_ground = False

    type_idle = 3
    idle_animate_count = 0
    jump_animate_count = 0

    curses.start_color()
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    cleared = False

    # Loop where k is the last character pressed
    while (k != ord('q')):
        # Initialization
        height, width = stdscr.getmaxyx()

        if not GAME_OVER:
            stdscr.clear()
            if k == curses.KEY_UP:
                if idle:
                    jump = going_up = True
                    idle = False
                    k=0

            setup_foreground(stdscr,height,width)
            create_obstacles(obstacle_index, stdscr, height)

            if obstacle_index >= 5:
                obstacle_index -= 1
            else:
                obstacle_index = width-5

            if idle:
                if type_idle == 1:
                    for part in IDLE_FRAMES:
                        stdscr.chgat(part[0], part[1], part[2], curses.A_REVERSE)
                    if idle_animate_count>WALK_ANIMATE_SENSITIVITY:
                        type_idle=2
                        idle_animate_count=0
                elif type_idle == 2:
                    for part in WALK_ONE_FRAMES:
                        stdscr.chgat(part[0], part[1], part[2], curses.A_REVERSE)
                    if idle_animate_count > WALK_ANIMATE_SENSITIVITY:
                        type_idle = 3
                        idle_animate_count = 0
                elif type_idle == 3:
                    for part in WALK_TWO_FRAMES:
                        stdscr.chgat(part[0], part[1], part[2], curses.A_REVERSE)
                    if idle_animate_count>WALK_ANIMATE_SENSITIVITY:
                        type_idle=1
                        idle_animate_count=0
                idle_animate_count += 1

            elif jump:
                if going_up:
                    if index<=JUMP_HEIGHT:
                        for part in IDLE_FRAMES:
                            stdscr.chgat(part[0]-index,part[1],part[2],curses.A_REVERSE)

                        if jump_animate_count > JUMP_ANIMATE_SENSITIVITY:
                            index+=1
                            jump_animate_count=0
                        jump_animate_count+=1
                    else:
                        going_down = True
                        going_up = False
                elif going_down:
                    if index>=0:
                        for part in IDLE_FRAMES:
                            stdscr.chgat(part[0]-index, part[1], part[2], curses.A_REVERSE)
                        if jump_animate_count > JUMP_ANIMATE_SENSITIVITY:
                            index-=1
                            jump_animate_count=0
                        jump_animate_count += 1
                    else:
                        going_down = False
                        jump = False
                        idle = True

            stdscr.move(0,0)
            check_collision(obstacle_index,index)

            stdscr.refresh()
            # Wait for next input
            time.sleep(SLEEP_TIME)

        else:
            if not cleared: stdscr.clear()
            title = "Game Over"[:width - 1]
            start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
            # Turning on attributes for title
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)

            # Rendering title
            stdscr.addstr(height//2, start_x_title, title)

            # Turning off attributes for title
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)
            if not cleared:
                stdscr.refresh()
                cleared = True


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    t1 = threading.Thread(target=main, args=[])
    t2 = threading.Thread(target=get_input, args=[])
    t1.start()
    t2.start()