import cv2

class CamManager:
    def __init__(self):
        """Initialize the CamManager instance."""

        self.cams = {}
        self.active_cam_id = None

    def add_cam(self, cam_id: int) -> None:
        """
        Add a cam by its ID.

        Parameters: cam_id (int): The ID of the cam to be added.
        Returns: None
        """

        if cam_id not in self.cams:
            cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
            if not cap.isOpened(): print(f"Failed to open cam [{cam_id}].")
            else:
                self.cams[cam_id] = cap
                if self.active_cam_id is None:
                    self.active_cam_id = cam_id
                print(f"Cam [{cam_id}] added successfully.")
        else: print(f"Cam [{cam_id}] is already added.")

    def release_cam(self, cam_id: int) -> None:
        """
        Release a specific cam by its ID.

        Parameters: cam_id (int): The ID of the cam to be released.
        Returns: None
        """

        if cam_id in self.cams:
            self.cams[cam_id].release()
            del self.cams[cam_id]

            if self.active_cam_id == cam_id:
                self.active_cam_id = None
            print(f"Cam [{cam_id}] released successfully.")
        else: print(f"Cam [{cam_id}] is not exist.")

    def release_all_cams(self) -> None:
        """
        Release all cams.

        Returns: None
        """

        for cam_id in list(self.cams.keys()):
            self.release_cam(cam_id)
        print("All cams released successfully.")

    def switch_active_cam(self, cam_id: int) -> None:
        """
        Switch the active cam to the specified ID.

        Parameters: cam_id (int): The ID of the cam to be set as active.
        Returns: None
        """

        if cam_id in self.cams:
            self.active_cam_id = cam_id
            print(f"Active cam switched to [{cam_id}].")
        else: print(f"Cam [{cam_id}] is not exist.")

    def get_active_cam(self) -> int:
        """
        Get the currently active cam ID.

        Returns: int: The ID of the currently active cam.
        """

        return self.active_cam_id

    def get_all_cams(self) -> list:
        """
        Get a list of all added cam IDs.

        Returns: list: A list of all added cam IDs.
        """

        return list(self.cams.keys())

    def get_frame(self, cam_id: int = None) -> any:
        """
        Get a frame from a specific cam or the active cam.

        Parameters: cam_id (int, optional): The ID of the cam to get the frame from. If None, the frame is captured from the active cam. Default is None.
        Returns: frame (any): The captured frame from the specified or active cam, or None if failed.
        """

        if cam_id is None:
            cam_id = self.active_cam_id

        if cam_id in self.cams:
            ret, frame = self.cams[cam_id].read()
            if not ret:
                print(f"Failed to get frame from cam [{cam_id}].")
                return None
            return frame
        else:
            print(f"Cam [{cam_id}] is not exist.")
            return None

    def capture_image(self, cam_id: int = None, filename: str = "capture.jpg") -> None:
        """
        Capture an image from a specific cam or the active cam and save it to a file.

        Parameters:
        cam_id (int, optional): The ID of the cam to capture the image from. If None, the image is captured from the active cam. Default is None.
        filename (str, optional): The name of the file to save the captured image. Default is "capture.jpg".

        Returns: None

        """
        frame = self.get_frame(cam_id)
        if frame is not None:
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as [{filename}].")
