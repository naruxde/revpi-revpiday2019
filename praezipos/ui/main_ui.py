# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        frm_main.setObjectName("frm_main")
        frm_main.resize(1024, 768)
        frm_main.setMinimumSize(QtCore.QSize(1024, 768))
        self.centralwidget = QtWidgets.QWidget(frm_main)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_header = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_header.sizePolicy().hasHeightForWidth())
        self.lbl_header.setSizePolicy(sizePolicy)
        self.lbl_header.setText("")
        self.lbl_header.setPixmap(QtGui.QPixmap(":/global/img/willebg.png"))
        self.lbl_header.setScaledContents(True)
        self.lbl_header.setObjectName("lbl_header")
        self.verticalLayout.addWidget(self.lbl_header)
        self.wid_main = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wid_main.sizePolicy().hasHeightForWidth())
        self.wid_main.setSizePolicy(sizePolicy)
        self.wid_main.setObjectName("wid_main")
        self.frame_center = QtWidgets.QFrame(self.wid_main)
        self.frame_center.setGeometry(QtCore.QRect(350, 20, 324, 200))
        self.frame_center.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center.setLineWidth(15)
        self.frame_center.setObjectName("frame_center")
        self.wid_load = QtWidgets.QLabel(self.wid_main)
        self.wid_load.setGeometry(QtCore.QRect(350, 20, 324, 215))
        self.wid_load.setPixmap(QtGui.QPixmap(":/global/img/load.png"))
        self.wid_load.setObjectName("wid_load")
        self.wid_lift = QtWidgets.QLabel(self.wid_main)
        self.wid_lift.setGeometry(QtCore.QRect(354, 280, 316, 432))
        self.wid_lift.setPixmap(QtGui.QPixmap(":/global/img/lift.png"))
        self.wid_lift.setObjectName("wid_lift")
        self.wid_fork = QtWidgets.QLabel(self.wid_main)
        self.wid_fork.setGeometry(QtCore.QRect(404, -13, 216, 293))
        self.wid_fork.setPixmap(QtGui.QPixmap(":/global/img/fork.png"))
        self.wid_fork.setObjectName("wid_fork")
        self.wid_more_left = QtWidgets.QLabel(self.wid_main)
        self.wid_more_left.setGeometry(QtCore.QRect(100, 50, 128, 128))
        self.wid_more_left.setPixmap(QtGui.QPixmap(":/global/png/left.png"))
        self.wid_more_left.setObjectName("wid_more_left")
        self.wid_more_right = QtWidgets.QLabel(self.wid_main)
        self.wid_more_right.setGeometry(QtCore.QRect(796, 50, 128, 128))
        self.wid_more_right.setPixmap(QtGui.QPixmap(":/global/png/right.png"))
        self.wid_more_right.setObjectName("wid_more_right")
        self.btn_fullscreen = QtWidgets.QPushButton(self.wid_main)
        self.btn_fullscreen.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.btn_fullscreen.setText("")
        self.btn_fullscreen.setFlat(True)
        self.btn_fullscreen.setObjectName("btn_fullscreen")
        self.frame_center.raise_()
        self.wid_lift.raise_()
        self.wid_fork.raise_()
        self.wid_more_left.raise_()
        self.wid_more_right.raise_()
        self.wid_load.raise_()
        self.btn_fullscreen.raise_()
        self.verticalLayout.addWidget(self.wid_main)
        frm_main.setCentralWidget(self.centralwidget)
        self.status = QtWidgets.QStatusBar(frm_main)
        self.status.setObjectName("status")
        frm_main.setStatusBar(self.status)

        self.retranslateUi(frm_main)
        QtCore.QMetaObject.connectSlotsByName(frm_main)

    def retranslateUi(self, frm_main):
        _translate = QtCore.QCoreApplication.translate
        frm_main.setWindowTitle(_translate("frm_main", "PIO"))

from . import main_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frm_main = QtWidgets.QMainWindow()
    ui = Ui_frm_main()
    ui.setupUi(frm_main)
    frm_main.show()
    sys.exit(app.exec_())

