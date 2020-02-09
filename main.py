import numpy as np
import cv2
from rtk import *

bot = Bot(
    'COM10',
    (12, 10, 8),
    (11, 13, 15),
    (22, 24, 26),
    (31, 29, 27),
    (36, 38, 40)
)
