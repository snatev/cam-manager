import math

import cv2
from ultralytics import YOLO

class CamAIMixin:
    """
    A mixin class for integrating AI-based functionalities into the camera manager using YOLO models.

    Attributes:
        mode (str): The mode of AI processing ('detection', 'segmentation', 'classify', 'pose').
        model (YOLO): The YOLO model used for AI processing.
    """

    def __init__(self, mode: str = "detection") -> None:
        """
        Initialize the CamAIMixin class with a specified AI processing mode.

        Parameters:
            mode (str): The mode of AI processing.
        """

        mode_mmodel_map = {
            "detection": "yolov8n.pt",
            "segmentation": "yolov8n-seg.pt",
            "classify": "yolov8n-cls.pt",
            "pose": "yolov8n-pose.pt" }

        if mode in mode_mmodel_map:
            self.mode = mode
            self.model = YOLO(mode_mmodel_map[mode])
        else:
            self.mode = "detection"
            self.model = YOLO("yolov8n.pt")

    def add_ai_to_frame(self, frame) -> tuple:
        """
        Add AI-based object detection, segmentation, classification, or pose estimation to the frame.

        Parameters:
            frame (ndarray): The input frame for processing.

        Returns:
            tuple: The processed frame and AI data.
        """

        ai_data = []
        names = self.model.names
        results = self.model(frame, stream=True)

        mode_func_map = {
            "detection": self.process_detections,
            "segmentation": self.process_segmentations,
            "classify": self.process_classifications,
            "pose": self.process_pose_estimations }

        for r in results:
            try: mode_func_map[self.mode](r, frame, names, ai_data)
            except Exception as e: raise Exception(f"Error processing AI data - {e}") from e

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

            org = (x1, y1 - 10)
            label = f"{names[cls]} {confidence}"
            cv2.putText(frame, label, org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            ai_data.append({
                "class": cls,
                "confidence": confidence,
                "box": [x1, y1, x2, y2] })

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
        except AttributeError: return

        for i, mask in enumerate(masks):
            mask = mask.cpu().numpy().astype("uint8") * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)

            confidence = math.ceil((result.boxes[i].conf[0] * 100)) / 100
            cls = int(result.boxes[i].cls[0])

            ai_data.append({
                "class": cls,
                "confidence": confidence,
                "mask": mask })

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
            class_name = names[i]
            confidence = math.ceil((prob * 100)) / 100

            label = f"{class_name} {confidence}"
            cv2.putText(frame, label, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            ai_data.append({
                "class": i,
                "confidence": confidence,
                "label": label })

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
