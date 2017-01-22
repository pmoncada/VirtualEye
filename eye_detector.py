import numpy as np
import cv2

# ----------------- Eye detector ----------------- #

def get_point_correspondence_from_image(img0, img1):
    eye_array_0 = eye_detector(img0)
    eye_array_1 = eye_detector(img1)
    return point_corresponder(eye_array_0, eye_array_1)

# Using a pretrained model, this function computes the location of a face and the eyes on the face,
# in order to generate 8 point correspondences between images
def eye_detector(img):

    face_cascade = cv2.CascadeClassifier('haarcascade_face.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    eye_array = []
    for index, (x,y,w,h) in enumerate(faces):
        if(index): continue
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            eye_array.append([ex,ey,ew,eh])
    return eye_array

# Given the left bottom corner point, width and height of a rectangle
# Returns the four corner points
def point_reconstruct(point):

    x,y,w,h = point[0],point[1],point[2],point[3]
    point0 = [x, y]
    point1 = [x + w, y]
    point2 = [x, y + h]
    point3 = [x + w, y + h]
    return [point0, point1, point2, point3]

# Returns two arrays of point correspondences between the two images
def point_corresponder(eye_array_0, eye_array_1):

    sorted(eye_array_0,key = lambda entry:entry[0])
    sorted(eye_array_1,key = lambda entry:entry[0])
    first_img = point_reconstruct(eye_array_0[0]) + point_reconstruct(eye_array_0[1])
    second_img = point_reconstruct(eye_array_1[0]) + point_reconstruct(eye_array_1[1])
    return first_img, second_img
