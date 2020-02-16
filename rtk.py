import threading
import time

import cv2
import numpy as np

# import RPi.GPIO as GPIO

from controller import Esp
from qt import *


# GPIO.setmode(GPIO.BOARD)


def limit(_min, _max, val):
    return min(_max, max(_min, val))


class Motor:
    FREQ = 1024

    class Mode:
        BRAKE = 0
        FLOAT = 1

    def __init__(self, speed_pin, dir1, dir2):
        self.dir1 = dir1
        self.dir2 = dir2
        self.speed_pin = speed_pin
        self.speed = 0

        _ = [
            GPIO.setup(i, GPIO.OUT) for i in [speed_pin, dir1, dir2]
        ]

        self.speed_pwm = GPIO.PWM(speed_pin, Motor.FREQ)

    def set_speed(self, speed):
        speed = limit(-100, 100, speed)
        self.speed = speed

    def start(self):
        if self.speed > 0:
            GPIO.output(self.dir1, GPIO.HIGH)
            GPIO.output(self.dir2, GPIO.LOW)

        if self.speed < 0:
            GPIO.output(self.dir1, GPIO.LOW)
            GPIO.output(self.dir2, GPIO.HIGH)

        self.speed_pwm.start(abs(self.speed))

    def stop(self, mode):
        if mode == Motor.Mode.BRAKE:
            GPIO.output(self.dir1, GPIO.LOW)
            GPIO.output(self.dir2, GPIO.LOW)
            self.speed_pwm.start(abs(self.speed))

        if mode == Motor.Mode.FLOAT:
            self.speed_pwm.start(0)


class Servo:
    MIN = 10
    MAX = 170
    SPEED = 1

    def __init__(self, pin, esp):
        self.pin = pin
        self._pos = None
        self.esp = esp

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        value = limit(Servo.MIN, Servo.MAX, value)
        self._pos = value
        self.esp.servo_move(self.pin, value)


repetable = [Qt.Key_F, Qt.Key_R,
             Qt.Key_G, Qt.Key_T,
             Qt.Key_H, Qt.Key_Y,
             Qt.Key_J, Qt.Key_U,
             Qt.Key_K, Qt.Key_I,
             Qt.Key_Up, Qt.Key_Down,
             Qt.Key_Right, Qt.Key_Left,
             ]


class Bot(Esp, Interface):
    SHIFT = 200
    SLOW = 100

    def __init__(self, portName, left_motor, right_motor, front_axis, back_axis, manip_motor, servo_pins, cam_number,
                 ports, sizes):
        Esp.__init__(self, portName)
        Interface.__init__(self, cam_number, ports, sizes)

        self.main_speed_value = self.mainSpeed.value()

        # self.manip = Motor(*manip_motor)
        # self.back = Motor(*back_axis)
        # self.front = Motor(*front_axis)
        # self.left = Motor(*left_motor)
        # self.right = Motor(*right_motor)
        #
        # self.motors = [self.manip, self.back, self.front, self.left, self.right]
        self.servos = [Servo(servo_pins[i], self) for i in range(len(servo_pins))]

        for i in self.servos:
            i.pos = 0

    def move(self, l, r):
        self.left.start(l)
        self.right.start(r)

    def __del__(self):
        self.close()

    def close(self):
        Esp.close(self)
        Interface.close(self)

        # for i in self.motors:
        #     i.start(0)
        #
        # GPIO.cleanup()

    def mainSpeedChanged(self, value):
        super().mainSpeedChanged(value)
        # self.left.set_speed(value)
        # self.right.set_speed(value)

    def manipSpeedChanged(self, value):
        super().manipSpeedChanged(value)
        # self.manip.set_speed(value)

    def flashLightChanged(selfs, state):
        super().flashLightChanged(state)

    def servoSpeedChanged(self, value):
        super().servoSpeedChanged(value)
        Servo.SPEED = value

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        key = event.key()

        if event.isAutoRepeat() and key not in repetable:
            return

        print('pressed', key)

        if key == Qt.Key_W:
            pass

        if key == Qt.Key_S:
            pass

        if key == Qt.Key_A:
            pass

        if key == Qt.Key_D:
            pass

        if key == Qt.Key_Q:
            pass

        if key == Qt.Key_E:
            pass

        if key == Qt.Key_Z:
            pass

        if key == Qt.Key_X:
            pass

        if key == Qt.Key_1:
            pass

        if key == Qt.Key_2:
            pass

        if key == Qt.Key_3:
            pass

        if key == Qt.Key_4:
            pass

        if key == Qt.Key_Space:
            self.mainLbl.setText('Stop')
            self.mainLbl.setStyleSheet("QLabel {color : red;}")
            # self.left.stop(Motor.Mode.BRAKE)
            # self.rigth.stop(Motor.Mode.BRAKE)

        if key == Qt.Key_Shift:
            self.mainLbl.setText('Shift')
            self.mainLbl.setStyleSheet("QLabel {color : blue;}")
            self.mainSpeed.setSliderPosition(self.SHIFT)
            # self.left.set_spped(self.SHIFT)
            # self.right.set_spped(self.SHIFT)

        if key == Qt.Key_Control:
            self.mainLbl.setText('Slow')
            self.mainLbl.setStyleSheet("QLabel {color : gold;}")
            self.mainSpeed.setSliderPosition(self.SLOW)
            # self.left.set_spped(self.SLOW)
            # self.right.set_spped(self.SLOW)

        if key == Qt.Key_Up:
            pass

        if key == Qt.Key_Down:
            pass

        if key == Qt.Key_Left:
            pass

        if key == Qt.Key_Right:
            pass

        if key == Qt.Key_F:
            self.servos[1].pos = Servo.SPEED + self.servos[1].pos

        if key == Qt.Key_R:
            self.servos[1].pos = -Servo.SPEED + self.servos[1].pos

        if key == Qt.Key_G:
            pass

        if key == Qt.Key_T:
            pass

        if key == Qt.Key_H:
            pass

        if key == Qt.Key_Y:
            pass

        if key == Qt.Key_J:
            pass

        if key == Qt.Key_U:
            pass

        if key == Qt.Key_K:
            pass

        if key == Qt.Key_I:
            pass

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)

        if event.isAutoRepeat():
            return

        key = event.key()
        print('released', key)

        if key == Qt.Key_W:
            pass

        if key == Qt.Key_S:
            pass

        if key == Qt.Key_A:
            pass

        if key == Qt.Key_D:
            pass

        if key == Qt.Key_Q:
            pass

        if key == Qt.Key_E:
            pass

        if key == Qt.Key_Z:
            pass

        if key == Qt.Key_X:
            pass

        if key == Qt.Key_1:
            pass

        if key == Qt.Key_2:
            pass

        if key == Qt.Key_3:
            pass

        if key == Qt.Key_4:
            pass

        if key == Qt.Key_Space:
            # self.left.stop(Motor.Mode.FLOAT)
            # self.rigth.stop(Motor.Mode.FLOAT)
            self.mainLbl.setStyleSheet("QLabel {color : black;}")
            self.mainSpeedChanged(self.main_speed_value)

        if key == Qt.Key_Shift or key == Qt.Key_Control:
            # self.left.set_spped(self.self.mainSpeed.value())
            # self.right.set_spped(self.self.mainSpeed.value())
            self.mainLbl.setStyleSheet("QLabel {color : black;}")
            self.mainSpeedChanged(self.main_speed_value)
            self.mainSpeed.setSliderPosition(self.main_speed_value)
