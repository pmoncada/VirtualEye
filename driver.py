#driver file

import numpy as np
import cv2

# Multithreading
import threading
import time

# Homeographic Matrix H
H = [[0, 0, 0],
	 [0, 0, 0],
	 [0, 0, 0]]

# Delay: frequency of recalculation of H in seconds
delay = 10

class Homography_Engine(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
    	while(True):
            time.sleep(delay)
            threadLock.acquire()
            print "recalculating homeographic matrix"
	        # Free lock to release next thread
            threadLock.release()

cap = cv2.VideoCapture(0)
hom = Homography_Engine(1)
threadLock = threading.Lock()
hom.start()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    threadLock.acquire()
    print "taking picture"
    # Free lock to release next thread
    threadLock.release()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
