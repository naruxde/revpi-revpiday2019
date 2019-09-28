#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GUI for forklift terminals."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2019 Sven Sager"
__license__ = "GPLv3"
from PyQt5 import QtCore, QtGui, QtWidgets
from revpimodio2 import RevPiNetIODriver
from revpimodio2.netio import ConfigChanged

from ui.main_ui import Ui_frm_main


class PraeziPos(QtWidgets.QMainWindow, Ui_frm_main):

    def __init__(self):
        super(PraeziPos, self).__init__()
        self.setupUi(self)

        # Setup start positions
        take_back = 550
        self.wid_fork.move(self.wid_fork.x(), self.wid_fork.y() + take_back)
        self.wid_lift.move(self.wid_lift.x(), self.wid_lift.y() + take_back)
        self.wid_load.move(self.wid_load.x(), self.wid_load.y() + take_back)
        self.wid_fork_geo = self.wid_fork.geometry()
        self.wid_lift_geo = self.wid_lift.geometry()
        self.wid_load_geo = self.wid_load.geometry()

        # Animation thread
        self.ani = AnimatePosition(self, take_back)
        self.ani.move_forklift.connect(self.on_ani_move_forklift)
        self.ani.move_load.connect(self.on_ani_move_load)
        self.ani.start()

        # Create revpi manager an connect thread save to events
        self.rm = RevPiManager(self)
        self.rm.forklift_changed.connect(self.on_forklift_changed)
        self.rm.load_pos_changed.connect(self.on_load_pos_changed)
        self.rm.program_running_changed.connect(self.on_program_running_changed)

        self.status.showMessage("Verbinde zum Revolution Pi...")
        self.rm.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """Shutdown threads before closing."""
        self.ani.requestInterruption()
        self.rm.requestInterruption()
        while self.rm.isRunning():
            self.rm.wait(100)

    @QtCore.pyqtSlot(int)
    def on_ani_move_forklift(self, y: int):
        """Animate the forklift."""
        self.wid_fork.setVisible(y > 0)
        self.wid_lift.setVisible(y > 0)

        self.wid_fork.move(
            self.wid_fork.x(),
            self.wid_fork_geo.y() - y
        )
        self.wid_lift.move(
            self.wid_lift.x(),
            self.wid_lift_geo.y() - y
        )

    @QtCore.pyqtSlot(int)
    def on_ani_move_load(self, y: int):
        """Animate the load of forklift."""
        self.wid_load.setVisible(y > 0)

        self.wid_load.move(
            self.wid_load.x(),
            self.wid_load_geo.y() - y
        )

    @QtCore.pyqtSlot(str, bool)
    def on_forklift_changed(self, name: str, exists: bool):
        if exists:
            # Forklift is coming

            self.wid_lift.move(
                self.wid_lift_geo.x() + int(self.rm.rpi.io.load_pos.value / 100),
                self.wid_lift.y()
            )

            self.ani.come()
        else:
            # Forklift is going
            self.ani.leave()

    @QtCore.pyqtSlot(str, int)
    def on_load_pos_changed(self, name: str, position: int):
        if not self.rm.rpi.io.program_running.value:
            return

        if not self.rm.rpi.io.forklift.value:
            self.wid_more_left.setVisible(False)
            self.wid_more_right.setVisible(False)
            return

        # Directions
        status = True
        if self.rm.rpi.io.more_left.value:
            status = False
            self.wid_more_left.setPixmap(QtGui.QPixmap(":/global/png/left.png"))

        if self.rm.rpi.io.more_right.value:
            status = False
            self.wid_more_right.setPixmap(QtGui.QPixmap(":/global/png/right.png"))

        if status:
            self.wid_more_left.setPixmap(QtGui.QPixmap(":/global/png/ok.png"))
            self.wid_more_right.setPixmap(QtGui.QPixmap(":/global/png/ok.png"))

        self.wid_more_left.setVisible(self.rm.rpi.io.more_left.value or status)
        self.wid_more_right.setVisible(self.rm.rpi.io.more_right.value or status)

        # Move load and fork
        self.wid_fork.move(
            self.wid_fork_geo.x() + int(position / 100),
            self.wid_fork.y()
        )
        self.wid_load.move(
            self.wid_load_geo.x() + int(position / 100),
            self.wid_load.y()
        )

    @QtCore.pyqtSlot(str, bool)
    def on_program_running_changed(self, name: str, running: bool):
        if running:
            self.status.showMessage("Steuerprogramm läuft...", 2000)
        else:
            self.status.showMessage("Steuerprogramm ist nicht aktiv!")

    @QtCore.pyqtSlot()
    def on_btn_fullscreen_clicked(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


class AnimatePosition(QtCore.QThread):
    move_forklift = QtCore.pyqtSignal(int)
    move_load = QtCore.pyqtSignal(int)

    def __init__(self, parent, pixel_way: int):
        super(AnimatePosition, self).__init__(parent)
        self._come = False
        self._leave = False
        self._load_arrived = False
        self._step_time = 10
        self._step_value = 2
        self._step_wait = 1000

        self._way = 0
        self._y_way = pixel_way

    def come(self):
        self._leave = False
        self._come = True

    def leave(self):
        self._come = False
        self._leave = True

    def requestInterruption(self) -> None:
        self._come = False
        self._leave = False
        super(AnimatePosition, self).requestInterruption()

    def run(self) -> None:
        while not self.isInterruptionRequested():
            while self._come:
                self._way += self._step_value

                # Animation signals
                self.move_forklift.emit(self._way)
                self.move_load.emit(self._way)

                if self._way < self._y_way:
                    self._load_arrived = False
                    self.msleep(self._step_time)
                else:
                    self._load_arrived = True
                    self._come = False
            while self._leave:
                self._way -= self._step_value

                # Animation signals
                self.move_forklift.emit(self._way)
                if not self._load_arrived:
                    self.move_load.emit(self._way)

                if self._way > 0:
                    self.msleep(self._step_wait if self._way <= self._step_value else self._step_time)
                else:
                    self.move_load.emit(self._way)
                    self._leave = False

            if not (self._come or self._leave):
                self.msleep(self._step_time)


class RevPiManager(QtCore.QThread):
    forklift_changed = QtCore.pyqtSignal(str, bool)
    load_pos_changed = QtCore.pyqtSignal(str, int)
    program_running_changed = QtCore.pyqtSignal(str, bool)

    def __init__(self, parent):
        super(RevPiManager, self).__init__(parent)
        self.rpi = None       # type: RevPiNetIODriver

    def _config_rpi(self) -> None:
        """Connect to RevPiPyLoad and register events."""
        self.rpi = RevPiNetIODriver(
            "192.168.1.2",
            "panel01",
            autorefresh=True,
            replace_io_file=":network:",
        )
        self.rpi.cycletime = 25
        self.rpi.setdefaultvalues()
        self.rpi.net_setdefaultvalues()

        # Fire events thread save to GUI elements
        self.rpi.io.forklift.reg_event(self.forklift_changed.emit, prefire=True)
        self.rpi.io.load_pos.reg_event(self.load_pos_changed.emit, prefire=True)
        self.rpi.io.program_running.reg_event(self.program_running_changed.emit, prefire=True)

    def run(self) -> None:
        """Mainloop of thread to connect to RevPi and monitor status."""

        while not self.isInterruptionRequested():
            # Connect RevPi
            if self.rpi is None:
                try:
                    self._config_rpi()
                except Exception as e:
                    self.msleep(250)
                    continue

            # Set values
            self.rpi.io.p_online.value = True

            # Start event system of RevPiModIO
            try:
                self.rpi.mainloop()
            except ConfigChanged:
                # Configuration was changed, try to reconnect
                self.rpi.disconnect()
                self.rpi = None

        # Clean up
        if self.rpi is not None:
            self.rpi.io.p_online.value = False
            self.rpi.disconnect()

    def requestInterruption(self) -> None:
        # Just exit blocking mainloop function.
        super(RevPiManager, self).requestInterruption()
        self.rpi.exit(full=False)

    @property
    def error(self):
        return self.rpi is None or self.rpi.reconnecting


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([])

    frm_main = PraeziPos()
    if "-f" in sys.argv:
        # Show in fullscreen
        frm_main.showFullScreen()

    frm_main.show()

    # Run main app
    rc = app.exec_()
    sys.exit(rc)
