"""
    main_gui.py  
    Responsible for all GUI setup.

"""

import sys, threading, Queue

from ui_mainwindow import Ui_MainWindow
from dialog_custom import CustomDialog
from server import ServerThread
from client import Client, ClientThread, data

from PySide.QtCore import (QFile)
from PySide.QtUiTools import (QUiLoader)
from PySide.QtGui import (QApplication, QMainWindow, QMessageBox)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.mode = None        # signals 'server'/'client' mode
        self.input_values = []  # input values retrieve from UI
        self.io_handlers()      # initialize UI components

        # communication/network variables
        self.condition = threading.Condition()
        self.queue = Queue.Queue()
        self.data = "meaningless"
        

    # links buttons to event handlers
    def io_handlers(self):
        self.btn_start_server.clicked.connect(self.startServer)
        self.btn_start_client.clicked.connect(self.startClient)
        self.btn_stop.clicked.connect(self.stopSimulation)
        self.btn_random_ball.clicked.connect(self.randomBall)
        self.btn_custom_ball.clicked.connect(self.customBall)


    def startServer(self):
        self.btn_start_client.setEnabled(False)     # disable 'client' button
        self.mode = ServerThread()
        self.mode.daemon = True
        self.mode.start()


    def startClient(self):
        self.btn_start_server.setEnabled(False)     # disable 'server' button
        self.mode = ClientThread(self.data,self.condition,self.queue)
        self.mode.daemon = True
        self.mode.start()


    def stopSimulation(self):
        self.mode = None    # signal stop of simulation

        # reenable both 'server'/'client' buttons
        self.btn_start_server.setEnabled(True)
        self.btn_start_client.setEnabled(True)


    def randomBall(self): pass
    

    def customBall(self):
        # create dialog for input
        dialog = CustomDialog()

        # retrieve input from dialog
        if (dialog.exec_()):
            self.input_values = dialog.results
        
        params = ['x','y','xv','yv','m','r']
        self.data = ''
        # print retrieved values
        for i in range(0,len(self.input_values)):
            self.data += params[i] + str(self.input_values[i])

        # input in queue for tcp thread
        self.queue.put(self.data)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())