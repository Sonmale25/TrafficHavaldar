import cv2
import numpy as np

class VehicleDetector:
    def __init__(self, model_path, config_path=None, class_names=None):
        self.net = cv2.dnn.readNet(model_path)
        self.class_names = class_names or ['car', 'truck', 'bus', 'motorbike', 'bicycle']

    def detect(self, frame, conf_threshold=0.4):
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (640, 640), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
        h, w = frame.shape[:2]
        boxes, confidences, class_ids = [], [], []
        for output in outputs:
            for det in output:
                scores = det[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    box = det[0:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype('int')
                    x = int(centerX - width / 2)
                    y = int(centerY - height / 2)
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, 0.4)
        results = []
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            results.append({
                'box': [x, y, w, h],
                'confidence': confidences[i],
                'class_id': class_ids[i],
                'class_name': self.class_names[class_ids[i]] if class_ids[i] < len(self.class_names) else 'unknown'
            })
        return results
