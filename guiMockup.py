import sys
import os
import math
import PySide2
import obd
from time import localtime, strftime
from PySide2 import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import QTimer

#gps related stuff
from gps3.agps3threaded import AGPS3mechanism
from time import sleep
from math import sin, cos, sqrt, atan2, radians

globalText = ''
conn = obd.OBD()
MAX_SAFE_RPMS = 4000

#oh shit, some volcanoes (junk data)
navpoints = [
[(-178.47,   -30.2),    'slight left'],
[(130.28,    30.78),    'slight left'],
[(-86.161,   11.984),   'slight left'],
[(150.52,    -5.58),    'slight left'],
[(120.993,   14.002),   'slight left'],
[(120.35,    15.13),    'slight left'],
[(147.12,    -5.358),   'slight left'],
[(-158.8,    56.53),    'slight left'],
[(-72.97,    -45.9),    'slight left'],
[(-122.18,   46.2),     'slight left'],
[(-159.38,   56.17),    'slight left'],
[(25.396,    36.404),   'slight left'],
[(-158.17,   56.88),    'slight left'],
[(-152.75,   60.48),    'slight left'],
[(176,-      38.82),    'slight left'],
[(150.52,    -5.58),    'slight left']
]


class gpsAntenna:
    def __init__(self):
        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data()
        self.agps_thread.run_thread()

    def getLoc(self):
        """gets and returns a lat/lon tuple"""
        val = (self.agps_thread.data_stream.lat, self.agps_thread.data_stream.lon)
        while val == ('n/a','n/a'): #if we can't get a fix, keep trying until we can
            sleep(1)
            val = (self.agps_thread.data_stream.lat, self.agps_thread.data_stream.lon)
        return val

    def checkSKY(self):
        """returns the satellites the antenna has a fix on"""
        return self.agps_thread.data_stream.satellites

    def countSKY(self):
        return len(checkSKY())

    def getDist(self, LongLat):
        """expects a long/lat tuple, returns linear distance in km"""

        R = 6373.0 #radius of earth in km
        current = self.getLoc()
        lat1 = radians(current[0])
        lon1 = radians(current[1])
        lat2 = radians(LongLat[1])
        lon2 = radians(LongLat[0])
        
        #delta
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        #haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c




class myApplication(QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        #---- GPS Downlink Handler ----
        self.downlink = gpsAntenna()
        self.turning = False

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
        grid.addWidget(self.labelChevron, 0, 2)
        grid.addWidget(self.timeText,     0, 0)
        grid.addWidget(self.speedText,    2, 2)
        grid.addWidget(self.etaText,      1, 0)

        self.setLayout(grid)

        #set initial position
        self.rotation = 0

        #---- Spin Timer Setup ----
        spinTimer = QTimer(self)
        #Hook timer completion to listener
        spinTimer.timeout.connect(self.spin)
        #Timer trips every msec, probably too much
        spinTimer.start(250)

        #---- Update Speed Text ----
        speedTimer = QTimer(self)
        speedTimer.timeout.connect(self.updateSpeedText)
        speedTimer.start(250)

        #---- Update Time Text ----
        textTimer = QTimer(self)
        textTimer.timeout.connect(self.updateTimeText)
        textTimer.start(1000)


        #---- Poll GPS antenna ----
        gpsTimer = QTimer(self)
        gpsTimer.timeout.connect(self.processLocation)
        textTimer.start(1000)

    def updateSpeedText(self):
        mph = conn.query(obd.commands.SPEED)
        if not mph.is_null():
            mph = mph.value.to('mph')
            self.speedText.setText(str(math.ceil(mph.magnitude))+"mph")

    def spin(self):

        #---- rotate based off engine rpms ----
        # Rotation = (<current rpms>/<Max rpms>) * 180

        # Rotate from initial image to avoid cumulative deformation from
        # transformation
        pixmapPointer = QtGui.QPixmap(self.imgPointer)

        # Query OBD for current RPMs
        rpm = conn.query(obd.commands.RPM)
        if not rpm.is_null():
            self.rotation = (rpm.value.magnitude/MAX_SAFE_RPMS) * 180

        transform = QtGui.QTransform().rotate(self.rotation)
        pixmapPointer = pixmapPointer.transformed(transform, QtCore.Qt.SmoothTransformation)

        #---- update label ----
        self.labelPointer.setPixmap(pixmapPointer)

    def updateTimeText(self):
        self.timeText.setText(strftime("%H:%M", localtime()))

    def processLocation(self):

        pixmapChevron = QtGui.QPixmap(self.imgChevron)

        #todo get q of navpoints
        distToNavpoint = self.downlink.getDist(navpoints[0][0])
        if distToNavpoint < 0.1: #within 100m of a turn
            self.turning = true
            #navpoint get turn type
            turntype = navpoint[0][1]
            if turntype == 'left':
                #chevron 90 deg anticlockwise
                rot = -90
            elif turntype == 'slight left':
                #chevron 45 deg anticlockwise
                rot = -45
            elif turntype == 'right':
                #chevron 90 deg clockwise
                rot = 90
            elif turntype == 'slight right':
                #chevron 45 deg clockwise
                rot = 45
            transform = QtGui.QTransform().rotate(rot)
            pixmapChevron = pixmapChevron.transformed(transform, QtCore.Qt.SmoothTransformation)
            self.labelChevron.setPixmap(pixmapChevron)

        else:
            #wait to pop until we're through the turn
            if self.turning:
                navpoints.pop(0)
                self.turning = False
            transform = QtGui.QTransform().rotate(0)
            pixmapChevron = pixmapChevron.transformed(transform, QtCore.Qt.SmoothTransformation)
            self.labelChevron.setPixmap(pixmapChevron)





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
