import numpy as np

class SpeedEstimator:
    def __init__(self, homography_matrix, fps, real_distance):
        self.H = homography_matrix  # 3x3 matrix
        self.fps = fps
        self.real_distance = real_distance  # meters per pixel or similar

    def estimate(self, track_history):
        # track_history: list of (frame_idx, x, y) for a single object
        if len(track_history) < 2:
            return 0.0
        (f0, x0, y0), (f1, x1, y1) = track_history[-2], track_history[-1]
        p0 = np.array([x0, y0, 1.0])
        p1 = np.array([x1, y1, 1.0])
        wp0 = np.dot(self.H, p0)
        wp1 = np.dot(self.H, p1)
        wp0 /= wp0[2]
        wp1 /= wp1[2]
        dist = np.linalg.norm(wp1[:2] - wp0[:2]) * self.real_distance
        dt = (f1 - f0) / self.fps
        speed = dist / dt if dt > 0 else 0.0
        return speed
