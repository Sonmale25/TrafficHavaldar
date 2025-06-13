from flask import Flask, jsonify
from flask_socketio import SocketIO
from .routes import api
from smart_traffic.pipeline import TrafficPipeline
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.register_blueprint(api, url_prefix='/api')

# Example config (replace with real paths and calibration)
VIDEO_SOURCE = 0  # or path to video file
MODEL_PATH = 'yolov5s.onnx'  # You must provide this file
HOMOGRAPHY_MATRIX = np.eye(3)
FPS = 20
REAL_DISTANCE = 0.05  # meters per pixel (example)
HEATMAP_SHAPE = (200, 400)

pipeline = TrafficPipeline(VIDEO_SOURCE, MODEL_PATH, HOMOGRAPHY_MATRIX, FPS, REAL_DISTANCE, HEATMAP_SHAPE)
pipeline.start_background()

@app.route('/api/stats')
def stats():
    return jsonify(pipeline.get_stats())

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
