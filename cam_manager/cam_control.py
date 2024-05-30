import cv2
import mss
import numpy as np
import pygetwindow as gw

class CamControlMixin:
    def add_cam(self, cam_id: int, capture_method=cv2.CAP_DSHOW, tricky_window_title: str = None) -> None:
        """
        Add a cam by its ID or a "tricky cam" by a window title.
        Parameters:
            cam_id (int): The ID of the cam to be added.
            capture_method: The method used to capture the video stream.
            tricky_window_title (str, optional): The title of the window to be used as a tricky cam.
        """

        if tricky_window_title:
            if tricky_window_title not in self.tricky_cams:
                window = gw.getWindowsWithTitle(tricky_window_title)
                if window:
                    self.tricky_cams[tricky_window_title] = window[0]
                    if self.active_cam_id is None:
                        self.active_cam_id = tricky_window_title
                    print(f"Tricky cam [{tricky_window_title}] added successfully.")
                else: print(f"Window with title [{tricky_window_title}] not found.")
            else: print(f"Tricky cam [{tricky_window_title}] is already added.")
        else:
            if cam_id not in self.cams:
                cap = cv2.VideoCapture(cam_id, capture_method)
                if not cap.isOpened(): print(f"Failed to open cam [{cam_id}].")
                else:
                    self.cams[cam_id] = cap
                    if self.active_cam_id is None:
                        self.active_cam_id = cam_id
                    print(f"Cam [{cam_id}] added successfully.")
            else: print(f"Cam [{cam_id}] is already added.")

    def release_cam(self, cam_id: int = None, tricky_window_title: str = None) -> None:
        """
        Release a specific cam by its ID or a tricky cam by its window title.
        Parameters:
            cam_id (int, optional): The ID of the cam to be released.
            tricky_window_title (str, optional): The title of the tricky cam window to be released.
        """

        if tricky_window_title:
            if tricky_window_title in self.tricky_cams:
                del self.tricky_cams[tricky_window_title]
                if self.active_cam_id == tricky_window_title:
                    self.active_cam_id = None
                print(f"Tricky cam [{tricky_window_title}] released successfully.")
            else: print(f"Tricky cam [{tricky_window_title}] does not exist.")
        else:
            if cam_id in self.cams:
                self.cams[cam_id].release()
                del self.cams[cam_id]

                if self.active_cam_id == cam_id:
                    self.active_cam_id = None
                print(f"Cam [{cam_id}] released successfully.")
            else: print(f"Cam [{cam_id}] does not exist.")

    def release_all_cams(self) -> None:
        """Release all cams and tricky cams."""

        for cam_id in list(self.cams.keys()):
            self.release_cam(cam_id)
        for tricky_window_title in list(self.tricky_cams.keys()):
            self.release_cam(tricky_window_title=tricky_window_title)
        print("All cams and tricky cams released successfully.")

    def switch_active_cam(self, cam_id: int = None, tricky_window_title: str = None) -> None:
        """
        Switch the active cam to the specified ID or tricky cam to the specified window title.
        Parameters:
            cam_id (int, optional): The ID of the cam to be set as active.
            tricky_window_title (str, optional): The title of the tricky cam window to be set as active.
        """

        if tricky_window_title:
            if tricky_window_title in self.tricky_cams:
                self.active_cam_id = tricky_window_title
                print(f"Active cam switched to tricky cam [{tricky_window_title}].")
            else: print(f"Tricky cam [{tricky_window_title}] does not exist.")
        else:
            if cam_id in self.cams:
                self.active_cam_id = cam_id
                print(f"Active cam switched to [{cam_id}].")
            else: print(f"Cam [{cam_id}] does not exist.")

    def get_frame(self, cam_id: int = None, tricky_window_title: str = None) -> any:
        """
        Get a frame from a specific cam or tricky cam.
        Parameters:
            cam_id (int, optional): The ID of the cam to get the frame from. Default is None.
            tricky_window_title (str, optional): The title of the tricky cam window to get the frame from. Default is None.
        Returns: frame (any): The captured frame from the specified or active cam/tricky cam, or None if failed.
        """

        if cam_id is None and tricky_window_title is None:
            if self.active_cam_id is None:
                print("No active cam.")
                return None
            if isinstance(self.active_cam_id, int):
                cam_id = self.active_cam_id
            else: tricky_window_title = self.active_cam_id

        if tricky_window_title:
            if tricky_window_title in self.tricky_cams:
                window = self.tricky_cams[tricky_window_title]
                with mss.mss() as sct:
                    monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
                    frame = np.array(sct.grab(monitor))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    return frame
            else:
                print(f"Tricky cam [{tricky_window_title}] does not exist.")
                return None
        else:
            if cam_id in self.cams:
                ret, frame = self.cams[cam_id].read()
                if not ret:
                    print(f"Failed to get frame from cam [{cam_id}].")
                    return None
                return frame
            else:
                print(f"Cam [{cam_id}] does not exist.")
                return None

    def capture_image(self, cam_id: int = None, tricky_window_title: str = None, filename: str = "capture.jpg") -> None:
        """
        Capture an image from a specific cam or tricky cam and save it to a file.
        Parameters:
            cam_id (int, optional): The ID of the cam to capture the image from. Default is None.
            tricky_window_title (str, optional): The title of the tricky cam window to capture the image from. Default is None.
            filename (str, optional): The name of the file to save the captured image. Default is "capture.jpg".
        """

        frame = self.get_frame(cam_id, tricky_window_title)
        if frame is not None:
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as [{filename}].")
