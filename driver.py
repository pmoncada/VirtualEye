import numpy as np
import cv2
import threading
import time

# ----------------- Parameters ----------------- #

# Delay: frequency of recalculation of H in seconds
delay = 10

# Video capture structures for physical cameras 0 and 1
cap_0 = cv2.VideoCapture(0)
cap_1 = cv2.VideoCapture(1)

# Frame 0 and Frame 1
ret_0, frame_0 = cap_0.read()
ret_1, frame_1 = cap_1.read()

# Point correspondences between frame 0 and frame 1
point_correspondences = get_point_correspondence_from_image(frame_0, frame_1)

# Homeographic Matrix H
hom_mat = get_homography_from_point_correspondence(point_correspondences)

# Frame 2, the generated image
frame_2 = cv2.perspectiveTransform(frame_1, frame_2, hom_mat)

# Lock around image frames and homeographic matrix
frameLock = threading.Lock()
matrixLock = threading.Lock()

# ----------------- Homography Thread ----------------- #

# Create Homography Engine
class Homography_Engine(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
    	while(True):
            # Make thread sleep
            time.sleep(delay)

            # Update point correspondences
            frameLock.acquire()
            point_correspondences = get_point_correspondence_from_image(frame_0, frame_1)
            frameLock.release()

            # Update Homeographic matrix
            matrixLock.acquire()
            hom_mat = get_homography_from_point_correspondence(point_correspondences)
            matrixLock.release()

hom = Homography_Engine(1)
hom.start()

# ----------------- Frame capture Thread ----------------- #

while(True):
    # Capture frame-by-frame
    frameLock.acquire()
    ret_0, frame_0 = cap_0.read()
    ret_1, frame_1 = cap_1.read()
    frameLock.release()

    # Create new frame by calculating homeographic matrix
    matrixLock.acquire()
    frame_2 = cv2.perspectiveTransform(frame_1, frame_2, hom_mat)
    matrixLock.release()

    # Display the resulting frame
    cv2.imshow('frame',frame_2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
