import pickle

mphList = pickle.load(open("mph.pickle", "rb"))
rpmList = pickle.load(open("rpm.pickle", "rb"))

import sys
import os
import PySide2
from time import localtime, strftime
from PySide2 import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import QTimer

class myApplication(QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        self.dir = False #this is a hack for mockup, false is turn forward, true is back

        #---- Prepare a Pixmap for Chevrons ----
        chevron = open("Chevron.png","rb").read()
        self.imgChevron = QImage()
        self.imgChevron.loadFromData(chevron)
        pixmapChevron = QtGui.QPixmap(self.imgChevron)

        #---- Prepare a Pixmap for pointer ----
        pointer = open("pointer.png","rb").read()
        self.imgPointer = QImage()
        self.imgPointer.loadFromData(pointer)
        pixmapPointer = QtGui.QPixmap(self.imgPointer)

        #---- Prepare a Pixmap for arc ----
        arc = open("arc.png","rb").read()
        self.imgArc = QImage()
        self.imgArc.loadFromData(arc)
        pixmapArc = QtGui.QPixmap(self.imgArc)


        #---- Embed Chevron Pixmap in a QLabel ----
        #calculate maximum span, give the image room to spin in the label
        diag = 1.1*((pixmapPointer.width()**2 + pixmapPointer.height()**2)**0.5)
        self.labelChevron = QLabel()
        self.labelChevron.setMinimumSize(diag,diag)
        self.labelChevron.setAlignment(QtCore.Qt.AlignCenter)
        self.labelChevron.setPixmap(pixmapChevron)

        #---- Embed Pointer Pixmap in a QLabel ----
        #calculate maximum span, give the image room to spin in the label
        diag = (pixmapPointer.width()**2 + pixmapPointer.height()**2)**0.5
        self.labelPointer = QLabel()
        self.labelPointer.setMinimumSize(diag, diag)
        self.labelPointer.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPointer.setPixmap(pixmapPointer)

        #---- Embed Arc Pixmap in a QLabel ----
        #calculate maximum span, give the image room to spin in the label
        #diag = (pixmapArc.width()**2 + pixmapArc.height()**2)**0.5
        #use span from pointer, so they are placed the same
        self.labelArc = QLabel()
        self.labelArc.setMinimumSize(diag, diag)
        self.labelArc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelArc.setPixmap(pixmapArc)


        #---- Text Color ----
        textPalette = QPalette()
        textPalette.setBrush(QPalette.Foreground, QColor(255, 255, 255))

        #---- Time Text ----
        self.timeText = QLabel("-----")
        self.timeText.setFont(QFont("Impact", 75))
        self.timeText.setAlignment(QtCore.Qt.AlignBottom)
        self.timeText.setPalette(textPalette)

        #---- ETA Text ----
        self.etaText = QLabel("ETA: --:--")
        self.etaText.setFont(QFont("Impact", 30))
        self.etaText.setAlignment(QtCore.Qt.AlignTop)
        self.etaText.setPalette(textPalette)

        #---- Speed Text ----
        self.speedText = QLabel("------")
        self.speedText.setFont(QFont("Impact", 75))
        self.speedText.setPalette(textPalette)


        #dsfasdfasdfasdf
        t1 = QLabel('0,0')
        t2 = QLabel('0,1')
        t3 = QLabel('0,2')

        t4 = QLabel('1,0')
        t5 = QLabel('1,1')
        t6 = QLabel('1,2')

        t7 = QLabel('2,0')
        t8 = QLabel('2,1')
        t9 = QLabel('2,2')
        #sadfasdfasdfa

        #---- Prepare a Layout ----
        grid = QGridLayout()
 
        grid.addWidget(self.labelPointer, 2, 0)
        grid.addWidget(self.labelArc,     2, 0)
        grid.addWidget(self.labelChevron, 1, 1)
        grid.addWidget(self.timeText,     0, 0)
        grid.addWidget(self.speedText,    2, 2)
        grid.addWidget(self.etaText,      1, 0)


        #grid.addWidget(t1,0,0)
        #grid.addWidget(t2,0,1)
        #grid.addWidget(t3,0,2)
        #grid.addWidget(t4,1,0)
        #grid.addWidget(t5,1,1)
        #grid.addWidget(t6,1,2)
        #grid.addWidget(t7,2,0)
        #grid.addWidget(t8,2,1)
        #grid.addWidget(t9,2,2)



        self.setLayout(grid)

        #set initial position
        self.rotation = 0

        #---- Spin Timer Setup ----
        spinTimer = QTimer(self)
        #Hook timer completion to listener
        spinTimer.timeout.connect(self.spin)
        #Timer trips every msec, probably too much
        spinTimer.start(100)

        #---- Update Speed Text ----
        speedTimer = QTimer(self)
        speedTimer.timeout.connect(self.updateSpeedText)
        speedTimer.start(100)

        #---- Update Time Text ----
        textTimer = QTimer(self)
        textTimer.timeout.connect(self.updateTimeText)
        textTimer.start(1000)

    def updateSpeedText(self):
    	if not mphList:
    		self.speedText.setText("0.0")
    		return
    	self.speedText.setText(str(mphList.pop(0)))

    def spin(self):

        #---- rotate based off engine rpms ----
        # Rotation = (<current rpms>/<Max rpms>) * 180

        # Rotate from initial image to avoid cumulative deformation from
        # transformation
        pixmapPointer = QtGui.QPixmap(self.imgPointer)

        if not mphList:
    		self.rotation = 0
    	else:
        	self.rotation = rpmList.pop(0)


        transform = QtGui.QTransform().rotate(self.rotation)
        pixmapPointer = pixmapPointer.transformed(transform, QtCore.Qt.SmoothTransformation)

        #---- update label ----
        self.labelPointer.setPixmap(pixmapPointer)

    def updateTimeText(self):
        self.timeText.setText(strftime("%H:%M", localtime()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = QPalette()
    p.setBrush(QPalette.Background, QColor(0, 0, 0))
    instance = myApplication()
    #size of our LCD
    instance.setFixedSize(800,480)
    instance.setPalette(p)
    instance.show()
    sys.exit(app.exec_())
