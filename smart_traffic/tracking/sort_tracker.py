from sort import Sort
import numpy as np

class Tracker:
    def __init__(self):
        self.tracker = Sort()

    def update(self, detections):
        # detections: list of [x, y, w, h, score]
        dets = np.array(detections)
        tracks = self.tracker.update(dets)
        # tracks: [x1, y1, x2, y2, id]
        return tracks
