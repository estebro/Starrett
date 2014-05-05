# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon May 05 14:59:06 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setEnabled(True)
        self.centralWidget.setObjectName("centralWidget")
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 581, 51))
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.btn_start_client = QtGui.QPushButton(self.groupBox)
        self.btn_start_client.setGeometry(QtCore.QRect(80, 20, 71, 23))
        self.btn_start_client.setObjectName("btn_start_client")
        self.btn_start_server = QtGui.QPushButton(self.groupBox)
        self.btn_start_server.setGeometry(QtCore.QRect(10, 20, 71, 23))
        self.btn_start_server.setFlat(False)
        self.btn_start_server.setObjectName("btn_start_server")
        self.btn_stop = QtGui.QPushButton(self.groupBox)
        self.btn_stop.setGeometry(QtCore.QRect(150, 20, 51, 23))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_random_ball = QtGui.QPushButton(self.groupBox)
        self.btn_random_ball.setGeometry(QtCore.QRect(200, 20, 101, 23))
        self.btn_random_ball.setObjectName("btn_random_ball")
        self.btn_custom_ball = QtGui.QPushButton(self.groupBox)
        self.btn_custom_ball.setGeometry(QtCore.QRect(300, 20, 101, 23))
        self.btn_custom_ball.setObjectName("btn_custom_ball")
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 60, 581, 311))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start_client.setText(QtGui.QApplication.translate("MainWindow", "Start Client", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start_server.setText(QtGui.QApplication.translate("MainWindow", "Start Server", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stop.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_random_ball.setText(QtGui.QApplication.translate("MainWindow", "Shoot Random", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_custom_ball.setText(QtGui.QApplication.translate("MainWindow", "Shoot Custom", None, QtGui.QApplication.UnicodeUTF8))

