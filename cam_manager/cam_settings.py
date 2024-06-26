import os
import cv2
import json

class CamSettingsMixin:
    """
    A mixin class for managing camera settings, including saving and loading settings from a file.

    Attributes:
        settings_file (str): The file path for saving and loading settings.
        settings (dict): A dictionary mapping property names to OpenCV property IDs.
    """

    def __init__(self, settings_file):
        """
        Initialize the CamSettingsMixin class.

        Parameters:
            settings_file (str): The file path for saving and loading settings.
        """

        self.settings_file = settings_file
        self.settings = {
            "CAP_PROP_SETTINGS": cv2.CAP_PROP_SETTINGS,

            "CAP_PROP_FRAME_WIDTH": cv2.CAP_PROP_FRAME_WIDTH,
            "CAP_PROP_FRAME_HEIGHT": cv2.CAP_PROP_FRAME_HEIGHT,

            "CAP_PROP_EXPOSURE": cv2.CAP_PROP_EXPOSURE,
            "CAP_PROP_AUTO_EXPOSURE": cv2.CAP_PROP_AUTO_EXPOSURE,

            "CAP_PROP_ZOOM": cv2.CAP_PROP_ZOOM,
            "CAP_PROP_FOCUS": cv2.CAP_PROP_FOCUS,
            "CAP_PROP_AUTOFOCUS": cv2.CAP_PROP_AUTOFOCUS,

            "CAP_PROP_FPS": cv2.CAP_PROP_FPS,
            "CAP_PROP_FOURCC": cv2.CAP_PROP_FOURCC,
            "CAP_PROP_FRAME_COUNT": cv2.CAP_PROP_FRAME_COUNT,

            "CAP_PROP_HUE": cv2.CAP_PROP_HUE,
            "CAP_PROP_GAIN": cv2.CAP_PROP_GAIN,
            "CAP_PROP_GUID": cv2.CAP_PROP_GUID,
            "CAP_PROP_GAMMA": cv2.CAP_PROP_GAMMA,
            "CAP_PROP_FORMAT": cv2.CAP_PROP_FORMAT,

            "CAP_PROP_PAN": cv2.CAP_PROP_PAN,
            "CAP_PROP_TILT": cv2.CAP_PROP_TILT,
            "CAP_PROP_ROLL": cv2.CAP_PROP_ROLL,
            "CAP_PROP_IRIS": cv2.CAP_PROP_IRIS,
            "CAP_PROP_TRIGGER": cv2.CAP_PROP_TRIGGER,
            "CAP_PROP_CONTRAST": cv2.CAP_PROP_CONTRAST,
            "CAP_PROP_SHARPNESS": cv2.CAP_PROP_SHARPNESS,
            "CAP_PROP_ISO_SPEED": cv2.CAP_PROP_ISO_SPEED,
            "CAP_PROP_BACKLIGHT": cv2.CAP_PROP_BACKLIGHT,
            "CAP_PROP_MONOCHROME": cv2.CAP_PROP_MONOCHROME,
            "CAP_PROP_BRIGHTNESS": cv2.CAP_PROP_BRIGHTNESS,
            "CAP_PROP_SATURATION": cv2.CAP_PROP_SATURATION,
            "CAP_PROP_BUFFERSIZE": cv2.CAP_PROP_BUFFERSIZE,
            "CAP_PROP_CONVERT_RGB": cv2.CAP_PROP_CONVERT_RGB,
            "CAP_PROP_TEMPERATURE": cv2.CAP_PROP_TEMPERATURE,
            "CAP_PROP_RECTIFICATION": cv2.CAP_PROP_RECTIFICATION,
            "CAP_PROP_WHITE_BALANCE_RED_V": cv2.CAP_PROP_WHITE_BALANCE_RED_V,
            "CAP_PROP_WHITE_BALANCE_BLUE_U": cv2.CAP_PROP_WHITE_BALANCE_BLUE_U }

    def save_settings(self, cap) -> None:
        """
        Save the current settings of the camera to a file.

        Parameters:
            cap (cv2.VideoCapture): The video capture object from which to save settings.
        """

        settings_data = {prop: cap.get(prop_id) for prop, prop_id in self.settings.items()}
        with open(self.settings_file, 'w') as f:
            json.dump(settings_data, f, indent=4)
        print(f"Settings saved to {self.settings_file}")

    def load_settings(self, cap) -> dict:
        """
        Load settings from a file and apply them to the camera.

        Parameters:
            cap (cv2.VideoCapture): The video capture object to which to apply settings.

        Returns:
            dict: The loaded settings.
        """

        settings_data = {}
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings_data = json.load(f)

            for prop, value in settings_data.items():
                prop_id = self.settings.get(prop)
                if prop_id is not None and prop_id != cv2.CAP_PROP_SETTINGS:
                    if not cap.set(prop_id, value):
                        print(f"Failed to set {prop} to {value}")
            print(f"Settings loaded from {self.settings_file}")
        else:
            print("No settings file found. Using default settings.")
            self.save_settings(cap)
        return settings_data

    def focus_cam(self, cam_id: int, focus_value: int) -> None:
        """
        Set the focus value of a specified camera.

        Parameters:
            cam_id (int): The ID of the camera to be focused.
            focus_value (int): The focus value to be set.
        """

        if cam_id in self.cams:
            cap = self.cams[cam_id]
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            cap.set(cv2.CAP_PROP_FOCUS, focus_value)
        else: raise Exception(f"Camera {cam_id} not found in self.cams")
