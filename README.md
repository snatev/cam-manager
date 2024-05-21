CamManager - Methods

__init__()
Initializes a CamManager instance.

--------------------------------------------------

add_cam(cam_id: int) -> None
Adds a camera by its ID.

Parameters:
cam_id (int): The ID of the camera to be added.

Returns: None

--------------------------------------------------

release_cam(cam_id: int) -> None
Releases a specific camera by its ID.

Parameters:
cam_id (int): The ID of the camera to be released.

Returns: None

--------------------------------------------------

release_all_cams() -> None
Releases all added cameras.

Returns: None

--------------------------------------------------

switch_active_cam(cam_id: int) -> None
Switches the active camera to the specified ID.

Parameters:
cam_id (int): The ID of the camera to be set as active.

Returns: None

--------------------------------------------------

get_active_cam() -> int
Gets the currently active camera ID.

Returns:
int: The ID of the currently active camera.

--------------------------------------------------

get_all_cams() -> list
Gets a list of all added camera IDs.

Returns:
list: A list of all added camera IDs.

--------------------------------------------------

get_frame(cam_id: int = None) -> any
Gets a frame from a specific camera or the active camera.

Parameters:
cam_id (int, optional): The ID of the camera to get the frame from. If None, the frame is captured from the active camera. Default is None.

Returns:
frame (any): The captured frame from the specified or active camera, or None if failed.

--------------------------------------------------

capture_image(cam_id: int = None, filename: str = "capture.jpg") -> None
Captures an image from a specific camera or the active camera and saves it to a file.

Parameters:
cam_id (int, optional): The ID of the camera to capture the image from. If None, the image is captured from the active camera. Default is None.
filename (str, optional): The name of the file to save the captured image. Default is "capture.jpg".

Returns: None
