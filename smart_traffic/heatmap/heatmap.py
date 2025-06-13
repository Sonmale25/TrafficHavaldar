import numpy as np

class HeatmapGenerator:
    def __init__(self, shape):
        self.heatmap = np.zeros(shape, dtype=np.float32)

    def update(self, detections):
        # detections: list of {'box': [x, y, w, h], ...}
        for det in detections:
            x, y, w, h = det['box']
            self.heatmap[y:y+h, x:x+w] += 1

    def get_heatmap(self):
        return self.heatmap
