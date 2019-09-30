# -*- coding: utf-8 -*-
"""Forklift load navigator."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2019 Sven Sager"
__license__ = "GPLv3"
import revpimodio2
from random import randint
from revpimodio2.helper import Cycletools


def cycle(ct: Cycletools):
    if ct.first:
        # Init control program variables
        ct.var.center_diff_left = -600
        ct.var.center_diff_right = 600
        ct.var.center_value = 0
        ct.var.mrk_t_forklift = False

        rpi.io.program_running.value = True

    # Flash LED A1 of core module
    rpi.core.a1green.value = ct.flag20c

    if rpi.io.t_forklift.value:
        # Forklift in place
        rpi.io.forklift.value = True

        if not ct.var.mrk_t_forklift:
            ct.var.mrk_t_forklift = True
            ct.var.center_value = rpi.io.position.value + randint(-6000, 6000)

        position = rpi.io.position.value - ct.var.center_value

        # Mirror value to virtual device
        rpi.io.load_pos.value = position

        # Check direction of difference
        rpi.io.more_right.value = position < ct.var.center_diff_left
        rpi.io.more_left.value = position > ct.var.center_diff_right

        # Show lights
        rpi.io.h_red.value = rpi.io.more_left.value or rpi.io.more_right.value
        rpi.io.h_green.value = not rpi.io.h_red.value

    else:
        # No forklift in position
        ct.var.mrk_t_forklift = False

        rpi.io.forklift.value = False
        rpi.io.load_pos.value = 0
        rpi.io.more_left.value = False
        rpi.io.more_right.value = False
        rpi.io.h_red.value = False
        rpi.io.h_green.value = False


def cleanup():
    rpi.io.program_running.value = False


# One global RevPiModIO instance for all modules and classes
rpi = revpimodio2.RevPiModIO(autorefresh=True)

# Configure IO of panel device
rpi.io.p_byte1.replace_io("p_online", "?", bit=0)

rpi.io.r_byte1.replace_io("program_running", "?", bit=0)
rpi.io.r_byte2.replace_io("more_left", "?", bit=0)
rpi.io.r_byte2.replace_io("more_right", "?", bit=1)
rpi.io.r_byte2.replace_io("forklift", "?", bit=2)

rpi.io.r_position1.replace_io("load_pos", "h")

# Export replaced ios for revpipyload and NetIO clients
rpi.export_replaced_ios()

rpi.handlesignalend(cleanup)
rpi.cycleloop(cycle, cycletime=20)
