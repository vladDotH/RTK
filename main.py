import numpy as np
import cv2
from rtk import *
from qt import *

app = QApplication(sys.argv)

bot = Bot(
    'COM10',
    (12, 10, 8),
    (11, 13, 15),
    (22, 24, 26),
    (31, 29, 27),
    (36, 38, 40),
    [15, 2, 4, 16, 17, 5, 18],
    3,
    ([0]),
    ((W, H), middle, (W, H))
)

sys.exit(app.exec_())
