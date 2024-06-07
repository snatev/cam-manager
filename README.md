# CamManager

A comprehensive library for managing cameras, including AI-based features, control, effects, settings and more.

## Cam_ai

### __init__

        """
        Initialize the CamAIMixin class with a specified AI processing mode.

        Parameters:
            mode (str): The mode of AI processing.
        """

### add_ai_to_frame

        """
        Add AI-based object detection, segmentation, classification, or pose estimation to the frame.

        Parameters:
            frame (ndarray): The input frame for processing.

        Returns:
            tuple: The processed frame and AI data.
        """

### process_detections

        """
        Process detections and draw bounding boxes on the frame.

        Parameters:
            result (dict): The result of the detection.
            frame (ndarray): The frame to draw the bounding boxes on.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

### process_segmentations

        """
        Process segmentations and draw masks on the frame.

        Parameters:
            result (dict): The result of the segmentation.
            frame (ndarray): The frame to draw the masks on.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

### process_classifications

        """
        Process classifications and add labels to the frame.

        Parameters:
            result (dict): The result of the classification.
            frame (ndarray): The frame to add the labels to.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

### process_pose_estimations

        """
        Process pose estimations and draw keypoints on the frame.

        Parameters:
            result (dict): The result of the pose estimation.
            frame (ndarray): The frame to draw the keypoints on.
            names (list): The names of the classes.
            ai_data (list): The list to store the AI data.
        """

## Cam_control

### add_cam

        """
        Add a cam by its ID or a tricky cam by a window title.

        Parameters:
            cam_id (int): The ID of the cam to be added.
            capture_method: The method used to capture the video stream.
            tricky_window_title (str, optional): The title of the window to be used as a tricky cam.
        """

### release_cam

        """
        Release a specific cam by its ID or a tricky cam by its window title.

        Parameters:
            cam_id (int, optional): The ID of the cam to be released.
            tricky_window_title (str, optional): The title of the tricky cam window to be released.
        """

### release_all_cams

        """
        Release all cams and tricky cams.
        """

### switch_active_cam

        """
        Switch the active cam to the specified ID or tricky cam to the specified window title.

        Parameters:
            cam_id (int, optional): The ID of the cam to be set as active.
            tricky_window_title (str, optional): The title of the tricky cam window to be set as active.
        """

### get_frame

        """
        Get a frame from a specific cam or tricky cam.

        Parameters:
            cam_id (int, optional): The ID of the cam to get the frame from. Default is None.
            tricky_window_title (str, optional): The title of the tricky cam window to get the frame from. Default is None.

        Returns:
            any: The captured frame from the specified or active cam/tricky cam, or None if failed.
        """

### capture_image

        """
        Capture an image from a specific cam or tricky cam and save it to a file.

        Parameters:
            cam_id (int, optional): The ID of the cam to capture the image from. Default is None.
            tricky_window_title (str, optional): The title of the tricky cam window to capture the image from. Default is None.
            filename (str, optional): The name of the file to save the captured image. Default is "capture.jpg".
        """

## Cam_effects

### apply_gray

        """
        Convert frame to grayscale.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The grayscaled frame.
        """

### apply_canny

        """
        Apply Canny edge detection to the frame.

        Parameters:
            frame (any): The input frame to be processed.
            threshold1 (int, optional): The first threshold for the hysteresis procedure. Default is 100.
            threshold2 (int, optional): The second threshold for the hysteresis procedure. Default is 200.

        Returns:
            any: The frame with Canny edge detection applied.
        """

### apply_sepia

        """
        Apply sepia effect to the frame.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The frame with sepia effect applied.
        """

### apply_emboss

        """
        Apply emboss effect to the frame.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The frame with emboss effect applied.
        """

### apply_negative

        """
        Apply negative effect to the frame.

        Parameters:
            frame (any): The input frame to be converted.

        Returns:
            any: The frame with negative effect applied.
        """

## Cam_info

### __init__

        """
        Initialize the CamInfoMixin class and set the user operating system.
        """

### get_available_cams

        """
        Get all available cam devices.

        Parameters:
            capture_method: The method used to capture the video stream. Default is cv2.CAP_DSHOW.

        Returns:
            list: A list of indices of available cam devices.
        """

### get_all_window_titles

        """
        Get titles of all open windows.

        Returns:
            list: A list of titles of all open windows.
        """

### get_window_by_title

        """
        Get a window by its title.

        Parameters:
            title (str): The title of the window to be retrieved.

        Returns:
            any: The window object matching the title, or None if not found.
        """

### get_active_cam

        """
        Get the currently active cam ID.

        Returns:
            int: The ID of the currently active cam.
        """

### get_all_added_cams

        """
        Get a list of all added cam IDs.

        Returns:
            list: A list of all added cam IDs.
        """

## Cam_manager

### __init__

        """
        Initialize the CamManager class.

        Parameters:
            is_ai (bool, optional): Whether to enable AI features. Default is False.
            ai_mode (str, optional): The AI mode to use ('detection', 'segmentation', 'classify', 'pose'). Default is 'detection'.
            load_settings (bool, optional): Whether to load camera settings from a file. Default is False.
        """

## Cam_settings

### __init__

        """
        Initialize the CamSettingsMixin class.

        Parameters:
            settings_file (str): The file path for saving and loading settings.
        """

### save_settings

        """
        Save the current settings of the camera to a file.

        Parameters:
            cap (cv2.VideoCapture): The video capture object from which to save settings.
        """

### load_settings

        """
        Load settings from a file and apply them to the camera.

        Parameters:
            cap (cv2.VideoCapture): The video capture object to which to apply settings.

        Returns:
            dict: The loaded settings.
        """

### focus_cam

        """
        Set the focus value of a specified camera.

        Parameters:
            cam_id (int): The ID of the camera to be focused.
            focus_value (int): The focus value to be set.
        """
