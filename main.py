"""
    main.py  
    Responsible for all GUI setup.

"""

import sys

from ui_mainwindow import Ui_MainWindow
from dialog_custom import CustomDialog

from PySide.QtCore import (QFile)
from PySide.QtUiTools import (QUiLoader)
from PySide.QtGui import (QApplication, QMainWindow, QMessageBox)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.io_handlers()


    # links buttons to event handlers
    def io_handlers(self):
        self.btn_start_server.clicked.connect(self.startServer)
        self.btn_start_client.clicked.connect(self.startClient)
        self.btn_stop.clicked.connect(self.stopSimulation)
        self.btn_random_ball.clicked.connect(self.randomBall)
        self.btn_custom_ball.clicked.connect(self.customBall)

    def startServer(self): pass
    def startClient(self): pass
    def stopSimulation(self): pass
    def randomBall(self): pass
    
    def customBall(self):
        # create dialog for input
        dialog = CustomDialog()
        results = []

        # retrieve input from dialog
        if (dialog.exec_()):
            results = dialog.results
        
        # print retrieved values
        for value in results:
            print(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())