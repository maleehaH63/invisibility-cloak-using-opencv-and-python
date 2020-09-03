#hue-0-179, saturation-(0-255),value(brightness)-(0-255)
import numpy as np
import cv2 
import time
#open the camera to record the bg
capture=cv2.VideoCapture(0)
#save the video recorded
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('outputg.avi', fourcc, 20.0, (640, 480))

#capture=cv2.VideoCapture(0)
#allow camera to warm up
time.sleep(2)
count=0
bg=0
#capture frame by frame in range of 60
for i in range(60):
    ret,bg=capture.read()
bg=np.flip(bg,1)

while(capture.isOpened()):
    ret, img = capture.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, 1)
    #use hsv-hue saturation value to detetct your color
    #this code is for green,you can change the tuple values for different color]
    #convert from rbg to hsv

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #give the upper and lower boundaries to detect the color and create a mask
    lower_green = np.array([100, 50, 50])
    upper_green = np.array([100, 255,255])

    mask1 = cv2.inRange(hsv, lower_green, upper_green)

    lower_green = np.array([30, 50, 50])
    upper_green = np.array([102, 255, 255])

    mask2 = cv2.inRange(hsv, lower_green, upper_green)
    #concat the masks
    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    #create an inverted mask to segment out the green color from frame
    mask2 = cv2.bitwise_not(mask1)
    #segment the green color part out of frame using bitwise and with the inverted mask
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res1 = cv2.bitwise_and(bg, bg, mask=mask1)

    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    #out.write(finalOutput)
    cv2.imshow("deathly hallows", finalOutput)
    out.write(finalOutput)
    k=cv2.waitKey(10)
    if k==27:
        break

#release capture and out

capture.release()
out.release()
cv2.destroyAllWindows()
