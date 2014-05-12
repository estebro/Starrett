"""
    main_gui.py  
    Responsible for all GUI setup and interaction
    between its many different components.

"""

import sys, Queue

from ui_mainwindow import Ui_MainWindow
from dialog_custom import CustomDialog
from server import ServerThread
from client import ClientThread
from scene_ui import SceneManager
#from physics import SimulationThread

from PySide.QtCore import (QTimer, QTimeLine, QPointF)
from PySide.QtGui import *

ANIMATOR_TIMEOUT = 100      # graphics update intveral

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.mode = None        # signals 'server'/'client' mode
        self.input_values = []  # input values retrieve from UI
        self.io_handlers()      # initialize UI components

        # communication/network variables
        self.tcp_main_queue = Queue.Queue()
        # self.setup_physics()
        self.data = "meaningless"

        self.tcp_sim_queue = Queue.Queue()
        self.cm = SceneManager(self.graphicsView, self.tcp_sim_queue)
        # self.cm.populate()

        self.animations = []
        self.animator = QTimer()    # timer paired with main thread
        self.animator.timeout.connect(self.update)  # timeout callback
        self.update()   # initial call
        

    # links buttons to event handlers
    def io_handlers(self):
        self.btn_start_server.clicked.connect(self.startServer)
        self.btn_start_client.clicked.connect(self.startClient)
        self.btn_stop.clicked.connect(self.stopSimulation)
        self.btn_random_ball.clicked.connect(self.randomBall)
        self.btn_custom_ball.clicked.connect(self.customBall)


    # period callback used to animate 'graphicsView'
    def update(self):
        
        # moves item to location smoothly in one second
        def config_animate_to(t,item,x,y):
            # used to animate an item in specific ways
            animation = QGraphicsItemAnimation()

            # create a timeline (1 sec here)
            timeline = QTimeLine(100)
            timeline.setFrameRange(0,200)   # 200 steps

            #item should at 'x,y' by time 't's
            animation.setPosAt(t,QPointF(x,y))
            animation.setItem(item)             # animate this item
            animation.setTimeLine(timeline)     # with this duration/steps

            return animation

        # check for items received via tcp
        if (not self.tcp_sim_queue.empty()):
            item = self.tcp_sim_queue.get() # retrieve value
            self.cm.addItem(item)           # add new item

        del self.animations[:]  # empty list of prev animations


        for item in self.cm.getItems(): # all items in graphicsView

            next_x, next_y = self.cm.next_move(item)    # determine next location
            # create corresponding item animation (given displacement in local coordinates)
            item_animation = config_animate_to(1,item,next_x,next_y)
            self.animations.append(item_animation)      # store item animation

            # update location values of item (global coordiantes)
            item.set_location(next_x+item.x_start,next_y+item.y_start)

        # signal the start of all animations
        [ animation.timeLine().start() for animation in self.animations]
        self.animator.start(ANIMATOR_TIMEOUT)   # reset timeout


    def startServer(self):
        self.btn_start_client.setEnabled(False)     # disable 'client' button
        # initiate server thread and pass GUI/simulation messgae queues
        self.mode = ServerThread(self.tcp_main_queue,self.tcp_sim_queue)
        self.mode.daemon = True
        self.mode.start()


    def startClient(self):
        self.btn_start_server.setEnabled(False)     # disable 'server' button
        # initiate client thread and pass GUI/simulation message queues
        self.mode = ClientThread(self.data,self.tcp_main_queue,self.tcp_sim_queue)
        self.mode.daemon = True     # thread to close when main thread closes
        self.mode.start()


    def stopSimulation(self):
        # reenable both 'server'/'client' buttons
        self.btn_start_server.setEnabled(True)
        self.btn_start_client.setEnabled(True)
        self.mode._Thread__stop()
        print 'Thread stopped'


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
        if (len(self.data) > 0):
            self.tcp_main_queue.put(self.data)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())