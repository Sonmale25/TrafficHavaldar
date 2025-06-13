# SmartTraffic Vision

**Real-Time Vehicle Detection, Tracking & Analytics**

SmartTraffic Vision is an end-to-end computer vision system for municipalities and city planners to automate traffic studies, optimize signal timing, and gain actionable insights from roadway video feeds. It provides real-time vehicle detection, tracking, speed estimation, and congestion heatmaps, all visualized on a modern web dashboard.

---

## 🚦 What It Does
- **Detects vehicles** (cars, trucks, bikes) in live or recorded video using deep learning (YOLOv5/MobileNet-SSD via OpenCV DNN)
- **Tracks vehicles** across frames, assigning unique IDs
- **Counts vehicles** per lane/direction
- **Estimates speed** using pixel displacement and camera calibration
- **Generates congestion heatmaps** (bird’s-eye occupancy maps)
- **Visualizes analytics** (counts, speeds, hot zones) on a web dashboard (Chart.js)
- **REST API** and real-time updates via Flask + Flask-SocketIO

---

## 🏗️ Architecture
```
Video Source → [Video I/O] → [Detection] → [Tracking] → [Speed Estimation] → [Heatmap] → [API] → [Dashboard]
```
- **Modular Python backend**: Each stage is a separate module for easy customization and extension.
- **Frontend dashboard**: Simple HTML/JS with Chart.js for live analytics.

---

## 📁 Project Structure
```
smart_traffic/
    videoio/         # Video capture and preprocessing
    detection/       # Vehicle detection (YOLOv5/MobileNet-SSD)
    tracking/        # SORT tracker (Kalman + Hungarian)
    speed/           # Speed estimation (homography)
    heatmap/         # Congestion heatmap generation
    api/             # Flask API and routes
    pipeline.py      # Orchestrates the full pipeline

dashboard/
    index.html       # Web dashboard (Chart.js)

requirements.txt    # Python dependencies
README.md           # Project documentation
```

---

## ⚙️ Setup & Installation
1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Download a YOLOv5 ONNX model** (e.g., `yolov5s.onnx`) and place it in the project directory.
4. **Configure video source and calibration** in `smart_traffic/api/app.py` or via environment variables.

---

## 🚀 Running the System
1. **Start the backend API**
   ```sh
   python -m smart_traffic.api.app
   ```
   Or use the VS Code task: **Run SmartTraffic API**
2. **Open the dashboard**
   - Open `dashboard/index.html` in your browser
   - The dashboard will fetch live analytics from the backend

---

## 🛠️ Customization & Deployment
- **Model**: Swap in your own ONNX model (YOLOv5/MobileNet-SSD)
- **Video Source**: Use a camera index or video file path
- **Production**: Deploy with Gunicorn + eventlet/gevent for Flask-SocketIO
- **Serve dashboard**: Use Flask to serve static files or deploy to a web server
- **API Security**: Add authentication, CORS, and HTTPS as needed

---

## 📊 Example API Response
```json
{
  "vehicle_counts": {"total": 15},
  "average_speeds": {"total": 42.3},
  "heatmap": [[0,1,2], [2,3,1], [1,0,4]]
}
```

---

## 🤝 Contributing
Pull requests and suggestions are welcome! Please open an issue for feature requests or bug reports.

---

## 📄 License
MIT License. See `LICENSE` for details.
