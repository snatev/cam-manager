import cv2
import math
from ultralytics import YOLO

class CamAIMixin:
    def __init__(self, mode: str = "detection") -> None:
        if mode == "detection":
            self.mode = "detection"
            self.model = YOLO("yolov8n.pt")
        elif mode == "segmentation":
            self.mode = "segmentation"
            self.model = YOLO("yolov8n-seg.pt")
        elif mode == "classify":
            self.mode = "classify"
            self.model = YOLO("yolov8n-cls.pt")
        elif mode == "pose":
            self.mode = "pose"
            self.model = YOLO("yolov8n-pose.pt")

    def add_ai_to_frame(self, frame) -> tuple:
        """
        Add AI-based object detection, segmentation, classification, or pose estimation to the frame.
        Parameters: frame (ndarray): The input frame for processing.
        """

        ai_data = []
        names = self.model.names
        results = self.model(frame, stream=True)

        for r in results:
            if self.mode == "detection": self.process_detections(r, frame, names, ai_data)
            elif self.mode == "segmentation": self.process_segmentations(r, frame, names, ai_data)
            elif self.mode == "classify": self.process_classifications(r, frame, names, ai_data)
            elif self.mode == "pose": self.process_pose_estimations(r, frame, names, ai_data)

        return frame, ai_data

    def process_detections(self, result: dict, frame, names: list, ai_data: list) -> None:
        """
        Process detections and draw bounding boxes on the frame.
        Parameters:
            result (dict): The result of the detection.
            frame (ndarray): The frame to draw the bounding boxes on.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

        boxes = result.boxes

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
            font = cv2.FONT_HERSHEY_SIMPLEX
            label = f"{names[cls]} {confidence}"

            cv2.putText(frame, label, org, font, font_scale, color, thickness)
            ai_data.append({"class": cls, "confidence": confidence, "box": [x1, y1, x2, y2]})

    def process_segmentations(self, result: dict, frame, names: list, ai_data: list) -> None:
        """
        Process segmentations and draw masks on the frame.
        Parameters:
            result (dict): The result of the segmentation.
            frame (ndarray): The frame to draw the masks on.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

        try: masks = result.masks.data
        except: return frame

        for i, mask in enumerate(masks):
            mask = mask.cpu().numpy().astype("uint8") * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)

            confidence = math.ceil((result.boxes[i].conf[0] * 100)) / 100
            cls = int(result.boxes[i].cls[0])

            ai_data.append({"class": cls, "confidence": confidence, "mask": mask})

    def process_classifications(self, result: dict, frame, names: list, ai_data: list) -> None:
        """
        Process classifications and add labels to the frame.
        Parameters:
            result (dict): The result of the classification.
            frame (ndarray): The frame to add the labels to.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

        for i, prob in enumerate(result.probs[0]):
            confidence = math.ceil((prob * 100)) / 100
            class_name = names[i]
            label = f"{class_name} {confidence}"
            ai_data.append({"class": i, "confidence": confidence, "label": label})
            cv2.putText(frame, label, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    def process_pose_estimations(self, result: dict, frame, names: list, ai_data: list) -> None:
        """
        Process pose estimations and draw keypoints on the frame.
        Parameters:
            result (dict): The result of the pose estimation.
            frame (ndarray): The frame to draw the keypoints on.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

        keypoints = result.keypoints.xy

        for keypoint in keypoints:
            keypoint = keypoint.cpu().numpy()
            for kp in keypoint:
                if len(kp) >= 2:
                    x, y = kp[:2]
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
            ai_data.append({"pose": keypoint.tolist()})
