import cv2
import mss
import platform
import numpy as np

from cam_manager.cam_settings import CamSettingsMixin as Settings

class CamControlMixin:
    """
    A mixin class for managing cameras and capturing video frames, including support for fake cams (screen captures).

    Attributes:
        cams (dict): A dictionary to store opened camera objects.
        fake_cams (dict): A dictionary to store fake cam windows.
        active_cam_id (int or str): The ID or title of the currently active camera.
        load_settings (bool): Whether to load camera settings from a file.
    """

    def add_cam(self, cam_id: int, capture_method = None, fake_window_title: str = None) -> None:
        """
        Add a cam by its ID or a fake cam by a window title.

        Parameters:
            cam_id (int): The ID of the cam to be added.
            capture_method: The method used to capture the video stream.
            fake_window_title (str, optional): The title of the window to be used as a fake cam.
        """

        os_method_map = {
            "Linux": cv2.CAP_V4L,
            "Windows": cv2.CAP_DSHOW }

        if capture_method is None:
            os = platform.system()
            capture_method = os_method_map[os]

        if fake_window_title:
            if fake_window_title not in self.fake_cams:
                window = self.get_window_by_title(fake_window_title)

                if window:
                    self.fake_cams[fake_window_title] = window[0]
                    if self.active_cam_id is None:
                        self.active_cam_id = fake_window_title
                    print(f"Fake cam [{fake_window_title}] added successfully.")
                else: raise Exception(f"Window with title [{fake_window_title}] not found.")
            else: raise Exception(f"Window [{fake_window_title}] is already added as a fake cam.")
        else:
            if cam_id not in self.cams:
                cap = cv2.VideoCapture(cam_id, capture_method)
                if not cap.isOpened(): raise Exception(f"Failed to open cam [{cam_id}].")
                else:
                    self.cams[cam_id] = cap

                    if self.load_settings:
                        cam_settings = Settings(f"cam_settings_{cam_id}.json")
                        cam_settings.load_settings(cap)

                    if self.active_cam_id is None:
                        self.active_cam_id = cam_id
                    print(f"Cam [{cam_id}] added successfully.")
            else: raise Exception(f"Cam [{cam_id}] is already added.")

    def release_cam(self, cam_id: int = None, fake_window_title: str = None) -> None:
        """
        Release a specific cam by its ID or a fake cam by its window title.

        Parameters:
            cam_id (int, optional): The ID of the cam to be released.
            fake_window_title (str, optional): The title of the fake cam window to be released.
        """

        if fake_window_title:
            if fake_window_title in self.fake_cams:
                del self.fake_cams[fake_window_title]
                if self.active_cam_id == fake_window_title:
                    self.active_cam_id = None
                print(f"Fake cam [{fake_window_title}] released successfully.")
            else: raise Exception(f"Fake cam [{fake_window_title}] does not exist.")
        else:
            if cam_id in self.cams:
                self.cams[cam_id].release()
                del self.cams[cam_id]

                if self.active_cam_id == cam_id:
                    self.active_cam_id = None
                print(f"Cam [{cam_id}] released successfully.")
            else: raise Exception(f"Cam [{cam_id}] does not exist.")

    def release_all_cams(self) -> None:
        """Release all cams and fake cams."""

        for cam_id in list(self.cams.keys()):
            self.release_cam(cam_id)
        for fake_window_title in list(self.fake_cams.keys()):
            self.release_cam(fake_window_title=fake_window_title)

        print("All cams and fake cams released successfully.")

    def switch_active_cam(self, cam_id: int = None, fake_window_title: str = None) -> None:
        """
        Switch the active cam to the specified ID or fake cam to the specified window title.

        Parameters:
            cam_id (int, optional): The ID of the cam to be set as active.
            fake_window_title (str, optional): The title of the fake cam window to be set as active.
        """

        if fake_window_title:
            if fake_window_title in self.fake_cams:
                self.active_cam_id = fake_window_title
                print(f"Active cam switched to fake cam [{fake_window_title}].")
            else: raise Exception(f"Fake cam [{fake_window_title}] does not exist.")
        else:
            if cam_id in self.cams:
                self.active_cam_id = cam_id
                print(f"Active cam switched to [{cam_id}].")
            else: raise Exception(f"Cam [{cam_id}] does not exist.")

    def get_frame(self, cam_id: int = None, fake_window_title: str = None) -> any:
        """
        Get a frame from a specific cam or fake cam.

        Parameters:
            cam_id (int, optional): The ID of the cam to get the frame from. Default is None.
            fake_window_title (str, optional): The title of the fake cam window to get the frame from. Default is None.

        Returns:
            any: The captured frame from the specified or active cam/fake cam, or None if failed.
        """

        if cam_id is None and fake_window_title is None:
            if self.active_cam_id is None:
                print("No active cam.")
                return None

            if isinstance(self.active_cam_id, int):
                cam_id = self.active_cam_id
            else: fake_window_title = self.active_cam_id

        if fake_window_title:
            if fake_window_title in self.fake_cams:
                window = self.fake_cams[fake_window_title]

                with mss.mss() as sct:
                    monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
                    frame = np.array(sct.grab(monitor))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                    return frame
            else: raise Exception(f"Fake cam [{fake_window_title}] does not exist.")
        else:
            if cam_id in self.cams:
                ret, frame = self.cams[cam_id].read()
                if not ret: raise Exception(f"Failed to read frame from cam [{cam_id}].")

                return frame
            else: raise Exception(f"Cam [{cam_id}] does not exist.")

    def capture_image(self, cam_id: int = None, fake_window_title: str = None, filename: str = "capture.jpg") -> None:
        """
        Capture an image from a specific cam or fake cam and save it to a file.

        Parameters:
            cam_id (int, optional): The ID of the cam to capture the image from. Default is None.
            fake_window_title (str, optional): The title of the fake cam window to capture the image from. Default is None.
            filename (str, optional): The name of the file to save the captured image. Default is "capture.jpg".
        """

        frame = self.get_frame(cam_id, fake_window_title)
        if frame is not None:
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as [{filename}].")
        else: raise Exception("Failed to capture image from cam.")
