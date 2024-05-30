import cv2
import pygetwindow as gw

class CamInfoMixin:
    def get_available_cams(self, capture_method = cv2.CAP_DSHOW) -> list:
        """
        Get all available cam devices.
        Parameters: capture_method: The method used to capture the video stream.
        Returns: list: A list of indices of available cam devices.
        """

        arr = []
        index = 0

        while True:
            cap = cv2.VideoCapture(index, capture_method)
            if not cap.isOpened(): break

            arr.append(index)
            cap.release()
            index += 1

        if not arr: print("No cams available.")
        return arr

    def get_available_windows(self) -> list:
            """
            Get all available windows.
            Returns: list: A list of all available windows.
            """
            windows = gw.getAllTitles()
            if not windows:
                print("No windows available.")
            return windows

    def get_active_cam(self) -> int:
        """
        Get the currently active cam ID.
        Returns: int: The ID of the currently active cam.
        """

        if self.active_cam_id is None: print("No active cam.")
        return self.active_cam_id

    def get_all_added_cams(self) -> list:
        """
        Get a list of all added cam IDs.
        Returns: list: A list of all added cam IDs.
        """

        if not self.cams: print("No cams added.")
        return list(self.cams.keys())
