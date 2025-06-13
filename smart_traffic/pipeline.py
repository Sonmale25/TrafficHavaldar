import threading
import time
from smart_traffic.videoio.video_reader import VideoReader
from smart_traffic.detection.detector import VehicleDetector
from smart_traffic.tracking.sort_tracker import Tracker
from smart_traffic.speed.speed_estimator import SpeedEstimator
from smart_traffic.heatmap.heatmap import HeatmapGenerator
import numpy as np

class TrafficPipeline:
    def __init__(self, video_source, model_path, homography_matrix, fps, real_distance, heatmap_shape):
        self.reader = VideoReader(video_source)
        self.detector = VehicleDetector(model_path)
        self.tracker = Tracker()
        self.speed_estimator = SpeedEstimator(homography_matrix, fps, real_distance)
        self.heatmap = HeatmapGenerator(heatmap_shape)
        self.track_histories = {}  # id: [(frame_idx, x, y)]
        self.stats = {
            'vehicle_counts': {},
            'average_speeds': {},
            'heatmap': np.zeros(heatmap_shape).tolist()
        }
        self.frame_idx = 0
        self.running = False

    def process_frame(self):
        frame = self.reader.read()
        if frame is None:
            return False
        detections = self.detector.detect(frame)
        # Prepare detections for tracker: [x, y, w, h, score]
        dets = [[*d['box'], d['confidence']] for d in detections]
        tracks = self.tracker.update(dets)
        # Update track histories
        for t in tracks:
            x1, y1, x2, y2, tid = t
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            self.track_histories.setdefault(tid, []).append((self.frame_idx, cx, cy))
        # Speed estimation (per track)
        speeds = {}
        for tid, history in self.track_histories.items():
            speeds[tid] = self.speed_estimator.estimate(history)
        # Count vehicles (by track id)
        self.stats['vehicle_counts'] = {'total': len(tracks)}
        self.stats['average_speeds'] = {'total': np.mean(list(speeds.values())) if speeds else 0}
        # Update heatmap
        self.heatmap.update(detections)
        self.stats['heatmap'] = self.heatmap.get_heatmap().tolist()
        self.frame_idx += 1
        return True

    def run(self):
        self.running = True
        while self.running:
            if not self.process_frame():
                break
            time.sleep(0.05)  # ~20 FPS
        self.reader.release()

    def start_background(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def get_stats(self):
        return self.stats
