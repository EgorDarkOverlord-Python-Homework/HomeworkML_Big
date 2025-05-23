from datetime import datetime
import cv2
from cell_counting import *

class Experiment():
    path = None
    date = None
    counts = [0, 0, 0]

    def __init__(self, path):
        self.path = path
    
    def execute(self):
        self.date = datetime.now().strftime('%m/%d/%y %H:%M:%S')
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        
        self.counts[0] = count_cell_1(image)
        self.counts[1] = count_cell_2(image)
        self.counts[2] = count_cell_3(image)