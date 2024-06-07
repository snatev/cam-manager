import platform

import cv2
if platform.system() == "Windows":import pygetwindow as gw
if platform.system() == "Linux": from Xlib import X, display

class CamInfoMixin:
    """
    A mixin class for managing and retrieving information about camera devices and windows.

    Attributes:
        user_os (str): The operating system of the user ('Linux' or 'Windows').
        active_cam_id (int or None): The ID of the currently active camera.
        cams (dict): A dictionary to store opened camera objects.
    """

    def __init__(self):
        """Initialize the CamInfoMixin class and set the user operating system."""

        if platform.system() == "Linux":
            self.user_os = "Linux"
        if platform.system() == "Windows":
            self.user_os = "Windows"

    def get_available_cams(self, capture_method=cv2.CAP_DSHOW) -> list:
        """
        Get all available cam devices.

        Parameters:
            capture_method: The method used to capture the video stream. Default is cv2.CAP_DSHOW.

        Returns:
            list: A list of indices of available cam devices.
        """

        arr = []
        index = 0

        while True:
            cap = cv2.VideoCapture(index, capture_method)
            if not cap.isOpened():
                break

            arr.append(index)
            cap.release()
            index += 1

        if not arr: print("No cams available.")
        return arr

    def get_all_window_titles(self) -> list:
        """
        Get titles of all open windows.

        Returns:
            list: A list of titles of all open windows.
        """

        titles = []
        if self.user_os == "Linux":
            d = display.Display()
            root = d.screen().root
            window_ids = root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value

            for window_id in window_ids:
                window = d.create_resource_object('window', window_id)
                titles.append(window.get_wm_name())
        if self.user_os == "Windows":
            for window in gw.getAllWindows():
                titles.append(window.title)

        titles = [title for title in titles if title]
        return titles

    def get_window_by_title(self, title) -> any:
        """
        Get a window by its title.

        Parameters:
            title (str): The title of the window to be retrieved.

        Returns:
            any: The window object matching the title, or None if not found.
        """

        if self.user_os == "Linux":
            d = display.Display()
            root = d.screen().root
            window_ids = root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value

            for window_id in window_ids:
                window = d.create_resource_object('window', window_id)
                if window.get_wm_name() == title: return window
            return None
        if self.user_os == "Windows":
            return gw.getWindowsWithTitle(title)

    def get_active_cam(self) -> int:
        """
        Get the currently active cam ID.

        Returns:
            int: The ID of the currently active cam.
        """

        if self.active_cam_id is None:
            print("No active cam.")
        return self.active_cam_id

    def get_all_added_cams(self) -> list:
        """
        Get a list of all added cam IDs.

        Returns:
            list: A list of all added cam IDs.
        """

        if not self.cams:
            print("No cams added.")
        return list(self.cams.keys())

    def get_all_added_fake_cams(self) -> list:
        """
        Get a list of all added fake cam window titles.

        Returns:
            list: A list of all added fake cam window titles.
        """

        if not self.fake_cams:
            print("No fake cams added.")
        return list(self.fake_cams.keys())
