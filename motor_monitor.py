#!/usr/bin/python3
'''
author: Tobias Weis
'''

import curses
import time
import numpy as np
import sys

from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import proxy_simple

with proxy_simple("192.168.124.16") as via1, proxy_simple("192.168.124.17") as via2:

    screen = curses.initscr()
    screen.nodelay(True)

    speed_vals = []

    while True:
        screen.clear()

        screen.addstr(0,0, "Press any key to exit")

        # First motor
        # Assembly 71
        screen.addstr(2,0,"------ Motor 1")
        screen.addstr(3,0,"Assembly 71")
        data, = via1.read([('@4/71/3', 'UINT')])
        screen.addstr(4,0,"Motor-Speed (RPM): %d"%data[1])

        # Assembly 101
        screen.addstr(6,0,"Assembly 101")
        data, = via1.read([('@4/101/3', 'UINT')])
        screen.addstr(7,0,"Motor-Speed (Hz): %d"%data[1])

        # First motor
        # Assembly 71
        screen.addstr(9,0,"------ Motor 2")
        screen.addstr(10,0,"Assembly 71")
        data, = via2.read([('@4/71/3', 'UINT')])
        screen.addstr(11,0,"Motor-Speed (RPM): %d"%data[1])

        # Assembly 101
        screen.addstr(13,0,"Assembly 101")
        data, = via2.read([('@4/101/3', 'UINT')])
        screen.addstr(14,0,"Motor-Speed (Hz): %d"%data[1])

        c = screen.getch()
        if c != -1:
            break
        screen.refresh()
        time.sleep(.1)
curses.endwin()

