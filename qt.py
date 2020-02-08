import sys
import typing

import cv2

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, Qt
from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QGroupBox, QVBoxLayout, QSlider, QCheckBox

import numpy as np
import time

original = (640, 480)
resize = 2
W, H = int(original[0] // resize), int(original[1] // resize)
cam_number = 3


class VideoCaptuteThread(QThread):
    changePixmap = pyqtSignal(list)

    def __init__(self, parent: typing.Optional[QObject] = ..., ports=tuple([0]), sizes=tuple([(W,H), original, (W,H)])):
        super().__init__()
        self.sizes = sizes
        self.ports = ports

    def run(self):
        caps = [cv2.VideoCapture(i) for i in self.ports]

        # for i in range(len(caps)):
        #     caps[i].set(cv2.CAP_PROP_FRAME_WIDTH, self.sizes[i][0])
        #     caps[i].set(cv2.CAP_PROP_FRAME_HEIGHT, self.sizes[i][1])

        while True:
            cam_data = [i.read() for i in caps]
            cam_data = [(cam_data[0][0], np.copy(cam_data[0][1])) for i in range(3)]
            images = []

            for i in range(len(cam_data)):
                ret, frame = cam_data[i]

                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # rgbImage = cv2.resize(rgbImage, self.sizes[i])
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w

                    convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

                    img = convertToQtFormat.scaled(self.sizes[i][0], self.sizes[i][1], QtCore.Qt.KeepAspectRatio)
                    images.append(img)

            # self.changePixmap.emit(images)
            self.changePixmap.emit(images)


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Video'
        self.left = 100
        self.top = 100
        self.width = W * 3
        self.height = H
        self.initUI()
        self.setChildrenFocusPolicy(Qt.NoFocus)

    @pyqtSlot(list)
    def setImage(self, image):
        for i in range(len(self.cams)):
            self.cams[i].setPixmap(QPixmap.fromImage(image[i]))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        windowLayout = QVBoxLayout()

        camerasGroup = QGroupBox("Cameras")
        camerasGroup.setAlignment(Qt.AlignCenter)

        video_layout = QGridLayout()

        # self.setFixedSize(640, 480)

        self.cams = [QLabel(self) for i in range(cam_number)]

        for i in range(len(self.cams)):
            self.cams[i].setAlignment(Qt.AlignCenter)
            video_layout.addWidget(self.cams[i], 0, i)

        self.cams[1].setStyleSheet("margin:10px; border:10px solid rgb(186, 104, 200); ")

        camerasGroup.setLayout(video_layout)
        windowLayout.addWidget(camerasGroup)

        controlGroup = QGroupBox("Control")
        controlGroup.setAlignment(Qt.AlignCenter)

        control_layout = QGridLayout()

        self.mainSpeed = QSlider(Qt.Horizontal, self)
        self.mainLbl = QLabel("Main speed: " + str(self.mainSpeed.value()))
        self.mainLbl.setAlignment(Qt.AlignCenter)
        self.mainSpeed.valueChanged.connect(self.mainSpeedChanged)
        self.mainSpeed.setMaximum(255)
        self.mainSpeed.setMinimum(0)
        self.mainSpeed.setValue(127)

        self.manipSpeed = QSlider(Qt.Horizontal, self)
        self.manipLbl = QLabel("Manipulator speed: " + str(self.manipSpeed.value()))
        self.manipLbl.setAlignment(Qt.AlignCenter)
        self.manipSpeed.valueChanged.connect(self.manipSpeedChanged)
        self.manipSpeed.setMaximum(255)
        self.manipSpeed.setMinimum(0)
        self.manipSpeed.setValue(127)

        self.flashLight = QCheckBox('Flashlight', self)
        self.flashLight.stateChanged.connect(self.flashLightChanged)

        control_layout.addWidget(self.mainLbl, 0, 1)
        control_layout.addWidget(self.mainSpeed, 1, 1)
        control_layout.addWidget(self.manipLbl, 2, 1)
        control_layout.addWidget(self.manipSpeed, 3, 1)
        control_layout.addWidget(self.flashLight, 0, 0)

        controlGroup.setLayout(control_layout)

        windowLayout.addWidget(controlGroup)

        self.setLayout(windowLayout)

        th = VideoCaptuteThread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        self.show()

    def mainSpeedChanged(self, value):
        self.mainLbl.setText(self.mainLbl.text().split(':')[0] + ': ' + str(self.mainSpeed.value()))

    def manipSpeedChanged(self, value):
        self.manipLbl.setText(self.manipLbl.text().split(':')[0] + ': ' + str(self.manipSpeed.value()))

    def flashLightChanged(selfs, state):
        pass

    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        pressed = event.key()
        print('pressed', pressed)

        if event.key() == Qt.Key_Escape:
            self.close()

        event.accept()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        released = event.key()
        print('released', released)
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
