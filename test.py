import cv2
from main import CamManager

cm = CamManager()

cm.add_cam(0)
cm.switch_active_cam(0)

while True:
    frame = cm.get_frame()
    if frame is not None:
        cv2.imshow("Active cam Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to capture frame from the cam.")
        break

cm.release_all_cams()
cv2.destroyAllWindows()
