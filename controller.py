import serial
from serial import Serial
import time


class mode(enumerate):
    LOW = 0
    HIGH = 1

    DIGITAL = 2
    PWM = 3

    SERVO = 4


class Esp:
    def digitalWrite(self, pin, val):
        self.port.write(bytes([mode.DIGITAL, pin, val]))

    def analogWrite(self, pin, val):
        self.port.write(bytes([mode.PWM, pin, int(val)]))

    def servo_move(self, servo, val):
        self.port.write(bytes([mode.SERVO, servo, int(val)]))

    def close(self):
        self.port.close()

    def __init__(self, portName):
        try:
            self.port = Serial(portName, baudrate=9600,
                               stopbits=serial.STOPBITS_ONE,
                               parity=serial.PARITY_NONE,
                               bytesize=serial.EIGHTBITS)

        except serial.SerialException:
            print("Could not connect to port " + portName)

        time.sleep(2)

    def __del__(self):
        self.close()