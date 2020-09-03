#hue-0-179, saturation-(0-255),value(brightness)-(0-255)
import numpy as np
import cv2 
import time
#hue-0-179, saturation-(0-255),value(brightness)-(0-255)    
capture=cv2.VideoCapture(0)
#save the video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('outputr.avi', fourcc, 20.0, (640, 480))

#capture=cv2.VideoCapture(0)
#allow the camera to open up
time.sleep(2)
count=0
bg=0
for i in range(60):
    ret,bg=capture.read()
bg=np.flip(bg,1)
# capture frame by frame in the range of 60
while(capture.isOpened()):
    ret, img = capture.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, 1)
    
    #use hsv-hue saturation value to detetct your color
    #this code is for blue,you can change the tuple values for different color]
    #convert from rbg to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #give the upper and lower boundaries to detect the color and create a mask
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255,255])

    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 120, 70])
    upper_red = np.array([180, 255, 255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    #concat the masks using or operator(+)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)
    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res1 = cv2.bitwise_and(bg, bg, mask=mask1)

    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    #out.write(finalOutput)
    cv2.imshow("deathly hallow", finalOutput)
    out.write(finalOutput)
    k=cv2.waitKey(10)
    if k==27:
        break


#release capture and out
capture.release()
out.release()
cv2.destroyAllWindows()

#hsv range for skin color is-(0-10)
#(0,120,70),(10,255,255)
