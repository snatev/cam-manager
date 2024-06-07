import cv2
import numpy as np

class CamEffectsMixin:
    """
    A mixin class for applying various effects to video frames.

    Methods:
        apply_gray(frame): Convert frame to grayscale.
        apply_sepia(frame): Apply sepia effect to the frame.
        apply_emboss(frame): Apply emboss effect to the frame.
        apply_negative(frame): Apply negative effect to the frame.
        apply_canny(frame, threshold1, threshold2): Apply Canny edge detection to the frame.
    """

    def apply_gray(self, frame) -> any:
        """
        Convert frame to grayscale.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The grayscaled frame.
        """

        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def apply_canny(self, frame, threshold1: int = 100, threshold2: int = 200) -> any:
        """
        Apply Canny edge detection to the frame.

        Parameters:
            frame (any): The input frame to be processed.
            threshold1 (int, optional): The first threshold for the hysteresis procedure. Default is 100.
            threshold2 (int, optional): The second threshold for the hysteresis procedure. Default is 200.

        Returns:
            any: The frame with Canny edge detection applied.
        """

        return cv2.Canny(frame, threshold1, threshold2)

    def apply_sepia(self, frame) -> any:
        """
        Apply sepia effect to the frame.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The frame with sepia effect applied.
        """
        sepia_filter = np.array(
            [[0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]])

        sepia_frame = cv2.transform(frame, sepia_filter)
        return cv2.convertScaleAbs(sepia_frame)

    def apply_emboss(self, frame) -> any:
        """
        Apply emboss effect to the frame.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The frame with emboss effect applied.
        """
        kernel = np.array(
            [[0, -1, -1],
            [1, 0, -1],
            [1, 1, 0]])

        return cv2.filter2D(frame, -1, kernel)

    def apply_negative(self, frame) -> any:
        """
        Apply negative effect to the frame.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The frame with negative effect applied.
        """

        return cv2.bitwise_not(frame)
