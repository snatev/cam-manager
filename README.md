#MANAGER
--------------------
In the CamManager init, switch "is_ai" parameter to use the default AI process.
You can also change the AI mode on the CamManager init with the "ai_mode" parameter. Possible options are: "detection", "segmentation"

#INFO
--------------------
get_available_cams
=====
Description: Get all available camera devices.
Parameters: capture_method: The method used to capture the video stream (default is cv2.CAP_DSHOW).
Returns: list: A list of indices of available camera devices.

get_available_windows
====
Description: Get all available windows.
Returns: list: A list of all available windows.

get_active_cam
=====
Description: Get the currently active camera ID.
Returns: int: The ID of the currently active camera. If no active camera, a message is printed.

get_all_added_cams
=====
Description: Get a list of all added camera IDs.
Returns: list: A list of all added camera IDs. If no cameras have been added, a message is printed.

#EFFECTS
--------------------
apply_gray
=====
Description: Convert the frame to grayscale.
Parameters: frame: The input frame to be converted.
Returns: The grayscale frame.

apply_canny
=====
Description: Apply Canny edge detection to the frame.
Parameters:
    frame: The input frame for edge detection.
    threshold1 (int, optional): The first threshold for the hysteresis procedure. Default is 100.
    threshold2 (int, optional): The second threshold for the hysteresis procedure. Default is 200.
Returns: The frame with Canny edge detection applied.

apply_sepia
=====
Description: Apply sepia effect to the frame.
Parameters: frame: The input frame for the sepia effect.
Returns: The frame with the sepia effect applied.

apply_emboss
=====
Description: Apply emboss effect to the frame.
Parameters: frame: The input frame for the emboss effect.
Returns: The frame with the emboss effect applied.

apply_negative
=====
Description: Apply negative effect to the frame.
Parameters: frame: The input frame for the negative effect.
Returns: The frame with the negative effect applied.

#CONTROL
--------------------
add_cam
=====
Description: Add a camera by its ID.
Paramters:
    cam_id (int): The ID of the camera to be added.
    capture_method: The method used to capture the video stream (default is cv2.CAP_DSHOW).
    tricky_window_title (str, optional): The title of the window to be used as a tricky cam.

release_cam
=====
Description: Release a specific camera by its ID.
Parameters: cam_id (int): The ID of the camera to be released.
tricky_window_title (str, optional): The title of the tricky cam window to be released.

release_all_cams
=====
Description: Release all cameras.

switch_active_cam
=====
Description: Switch the active camera to the specified ID.
Parameters: cam_id (int): The ID of the camera to be set as active.
tricky_window_title (str, optional): The title of the tricky cam window to be set as active.

get_frame
=====
Description: Get a frame from a specific camera or the active camera.
Parameters:
    cam_id (int, optional): The ID of the camera to get the frame from. If None, the frame is captured from the active camera (default is None).
    tricky_window_title (str, optional): The title of the tricky cam window to get the frame from. Default is None.
Returns: The captured frame from the specified or active camera, or None if failed.


capture_image
=====
Description: Capture an image from a specific camera or the active camera and save it to a file.
Parameters:
    cam_id (int, optional): The ID of the camera to capture the image from. If None, the image is captured from the active camera (default is None).
    tricky_window_title (str, optional): The title of the tricky cam window to capture the image from. Default is None.
    filename (str, optional): The name of the file to save the captured image (default is "capture.jpg").

#AI
--------------------
add_ai_to_frame
=====
Description: Add AI-based object detection or segmentation to the frame.
Parameters: frame (ndarray): The input frame for processing.
Returns: The frame with the AI method applied.
