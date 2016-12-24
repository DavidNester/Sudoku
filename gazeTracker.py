import cv2
import numpy as np
import sys

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

video_capture = cv2.VideoCapture(0)
def cleanFaces(faces,width,height):
    if len(faces) == 0 or len(faces) == 1:
        return list(faces)
    best = (10000,-1)
    for i in range(len(faces)):
        xCen = faces[i][0] + faces[i][2]/2
        yCen = faces[i][1] + faces[i][3]/2
        dif = abs(xCen - width/2) + abs(yCen - height/2)
        if dif < best[0]:
            best = (dif,i)
    if best[1] == -1:
        return list()
    return list(faces[best[1]])
def cleanEyes(eyes):
    if len(eyes) == 0 or len(eyes) == 1:
        return list()
    #      ( val, i, j)
    best = (1000,-1,-1)
    for i in range(len(eyes)):
        for j in range(i+1,len(eyes)):
            if eyes[i][3] > 60 and eyes[j][3]:
                dif = abs(eyes[i][1] - eyes[j][1])
                if dif < best[0]:
                    best = (dif,i,j)
    if best[1] == -1:
        return list()
    return list([eyes[best[1]],eyes[best[2]]])
    

num = -1
while True:
    num += 1
    if num % 5 == 0:
        num = 0
        # Capture frame-by-frame
        ret, frame = video_capture.read()
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        faces = cleanFaces(faces,int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)),int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eyeCascade.detectMultiScale(roi_gray)
            eyes = cleanEyes(eyes)
            
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                
                small = roi_gray[y:ey+eh, ex:ex+ew]
                small_real = roi_color[y:ey+eh, ex:ex+ew]
                
                retval, image = cv2.threshold(small, 20, 255, cv2.cv.CV_THRESH_BINARY)
                #el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                #image = cv2.dilate(image, el, iterations=4)
                #image = cv2.GaussianBlur(image, (13, 13), 0)
                cv2.imshow('small',image)
                circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 5, param2 = 30) #find circles
                if circles is not None:
                    # convert the (x, y) coordinates and radius of the circles to integers
                    circles = np.round(circles[0, :]).astype("int")
                    #check if the circles agree with previous data
                    for cx,cy,cr in circles:
                        cv2.circle(small_real, (cx, cy), cr+5, (228, 20, 20), 4)
                        cv2.rectangle(small_real, (cx - 5, cy - 5), (cx + 5, cy + 5), (0, 128, 255), -1)
    
        # Display the resulting frame
        cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
