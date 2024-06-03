import cv2
import platform
if platform.system() == "Windows": import pygetwindow as gw
if platform.system() == "Linux": from Xlib import X, display

class CamInfoMixin:
    def __init__(self):
        if platform.system() == "Linux": self.user_os = "Linux"
        if platform.system() == "Windows": self.user_os = "Windows"

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

    def get_all_window_titles(self):
        if self.user_os == "Linux":
            d = display.Display()
            root = d.screen().root
            window_ids = root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value

            titles = []
            for window_id in window_ids:
                window = d.create_resource_object('window', window_id)
                titles.append(window.get_wm_name())
            return titles
        if self.user_os == "Windows":
            titles = []
            for window in gw.getAllWindows():
                titles.append(window.title)
            return titles

    def get_window_by_title(self, title):
        if self.user_os == "Linux":
            d = display.Display()
            root = d.screen().root

            windowIDs = root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value
            for windowID in windowIDs:
                window = d.create_resource_object('window', windowID)
                if window.get_wm_name() == title: return window
            return None
        if self.user_os == "Windows":
            return gw.getWindowsWithTitle(title)

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
