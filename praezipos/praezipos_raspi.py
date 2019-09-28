#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Praezipos system for raspberry pi with sense hat."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2019 Sven Sager"
__license__ = "GPLv3"
from enum import Enum
from revpimodio2 import RevPiNetIODriver
from sense_hat import SenseHat


class PixelColor(Enum):
    WHITE = (127, 127, 127)
    RED = (127, 0, 0)
    GREEN = (0, 127, 0)
    BLUE = (0, 0, 127)
    YELLOW = (127, 127, 0)
    BLACK = (0, 0, 0)


class MyDriver:

    def __init__(self, revpi_address: str, virtual_device: str):
        self.hat = SenseHat()
        self.px_connected = [(0, 0)]
        self.px_running = [(2, 0)]
        self.px_error = [(7, 0)]

        self.px_center = [(i, 4) for i in range(8)]
        self.px_left3 = [(i, 1) for i in range(8)]
        self.px_left2 = [(i, 2) for i in range(8)]
        self.px_left1 = [(i, 3) for i in range(8)]
        self.px_right1 = [(i, 5) for i in range(8)]
        self.px_right2 = [(i, 6) for i in range(8)]
        self.px_right3 = [(i, 7) for i in range(8)]

        self.mrk_pos = None

        # Connect to RevPiModIO
        self.rpi = RevPiNetIODriver(
            revpi_address, virtual_device,
            autorefresh=True,
            monitoring=True,
            replace_io_file=":network:",
        )
        self.rpi.handlesignalend(self.stop)

    def _set_px(self, pixels: list, color: PixelColor):
        """Global function to set a pixel map."""
        for pixel in pixels:
            self.hat.set_pixel(*pixel, color.value)

    def on_load_pos(self, name: str, value: int):
        if not self.rpi.io.program_running.value:
            return

        if self.rpi.io.forklift.value:
            status = True
            pos_px = None
            if self.rpi.io.more_left:
                status = False
                if value < 2000:
                    pos_px = self.px_right1
                elif value < 4000:
                    pos_px = self.px_right2
                else:
                    pos_px = self.px_right3

            if self.rpi.io.more_right:
                status = False
                print(value)
                if value < -4000:
                    pos_px = self.px_left3
                elif value < -2000:
                    pos_px = self.px_left2
                else:
                    pos_px = self.px_left1

            if self.mrk_pos != pos_px:
                # Switch off old pixel
                if self.mrk_pos:
                    self._set_px(self.mrk_pos, PixelColor.BLACK)

                # Switch on new pixel
                if pos_px:
                    self._set_px(pos_px, PixelColor.RED)

                self.mrk_pos = pos_px

            # Show center line
            self._set_px(
                self.px_center,
                PixelColor.GREEN if status else PixelColor.BLUE
            )

        else:
            self._set_px(self.px_center, PixelColor.BLACK)
            if self.mrk_pos:
                self._set_px(self.mrk_pos, PixelColor.BLACK)

    def on_program_running(self, name, value):
        self._set_px(self.px_running, PixelColor.GREEN if value else PixelColor.YELLOW)

    def start(self):

        self.rpi.io.program_running.reg_event(self.on_program_running, prefire=True)
        self.rpi.io.load_pos.reg_event(self.on_load_pos, prefire=True)

        self.rpi.mainloop(blocking=False)

        while not self.rpi.exitsignal.wait(0.2):
            self._set_px(
                self.px_connected,
                PixelColor.RED if self.rpi.reconnecting else PixelColor.GREEN
            )

            # Check for errors
            if self.rpi.ioerrors > 0:
                self.rpi.resetioerrors()
                self._set_px(self.px_error, PixelColor.RED)
            else:
                self._set_px(self.px_error, PixelColor.GREEN)

        self.hat.clear()
        self.rpi.disconnect()

    def stop(self):
        self.rpi.setdefaultvalues()


if __name__ == '__main__':
    from time import sleep

    root = None
    while root is None:
        try:
            while True:
                root = MyDriver("192.168.1.2", "panel01")
                root.start()
                if not root.rpi.config_changed:
                    break
        except Exception as e:
            print(e)
            sleep(5)
