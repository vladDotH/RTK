import threading
import time

import cv2
import numpy as np

import RPi.GPIO as GPIO

from controller import Esp

GPIO.setmode(GPIO.BOARD)


def limit(_min, _max, val):
    return min(_max, max(_min, val))


class Motor:
    FREQ = 1024

    def __init__(self, speed_pin, dir1, dir2):
        self.dir1 = dir1
        self.dir2 = dir2
        self.speed_pin = speed_pin
        self.speed = 0

        _ = [
            GPIO.setup(i, GPIO.OUT) for i in [speed_pin, dir1, dir2]
        ]

        self.speed_pwm = GPIO.PWM(speed_pin, Motor.FREQ)

    def start(self, speed):
        speed = limit(-100, 100, speed)

        if speed == self.speed:
            return

        self.speed = speed

        if speed > 0:
            GPIO.output(self.dir1, GPIO.HIGH)
            GPIO.output(self.dir2, GPIO.LOW)

        if speed < 0:
            GPIO.output(self.dir1, GPIO.LOW)
            GPIO.output(self.dir2, GPIO.HIGH)

        if speed == 0:
            GPIO.output(self.dir1, GPIO.LOW)
            GPIO.output(self.dir2, GPIO.LOW)

        self.speed_pwm.start(abs(speed))


class Bot(Esp):
    def __init__(self, portName, left_motor, right_motor, front_axis, back_axis, manip_motor):
        super().__init__(portName)
        self.manip = Motor(*manip_motor)
        self.back = Motor(*back_axis)
        self.front = Motor(*front_axis)
        self.left = Motor(*left_motor)
        self.right = Motor(*right_motor)

        self.motors = [self.manip, self.back, self.front, self.left, self.right]

    def move(self, l, r):
        self.left.start(l)
        self.right.start(r)

    def __del__(self):
        self.close()

    def close(self):
        for i in self.motors:
            i.start(0)

        GPIO.cleanup()
