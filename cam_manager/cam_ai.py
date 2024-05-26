import cv2
import math
from ultralytics import YOLO

class CamAIMixin:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def add_ai_to_frame(self, frame):
        """Add AI-based object detection to the frame."""

        results = self.model(frame, stream=True)
        ai_data = []

        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                thickness = 2
                font_scale = 1
                org = (x1, y1 - 10)
                color = (255, 0, 0)
                label = f"{cls} {confidence}"
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, label, org, font, font_scale, color, thickness)
                ai_data.append({"class": cls, "confidence": confidence, "box": [x1, y1, x2, y2]})

        return frame, ai_data
