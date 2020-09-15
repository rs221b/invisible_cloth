
import numpy as np
import cv2
import time

print("invisible_cloth")

input = 'video.avi' # name of the input video in the same directory
# use input = 0, if want to use webcam   

cap = cv2.VideoCapture(input) #instance of the video file/camera

time.sleep(3)
background = 0
for i in range(60):
    ret, background = cap.read()

t = time.localtime()
t = time.strftime("output_%H_%M_%S", t)
outputfile = t + '.avi'

codec = cv2.VideoWriter_fourcc(*'XVID') # Video Codec
out = cv2.VideoWriter(outputfile,codec,30.0,(1280,720)) # output

while(cap.isOpened()):
    ret, img = cap.read()
    if ret == False:
        break
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #converting image to hsv

    lower_red = np.array([0, 140, 80])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 140, 80])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    #lower and upper limits of the color to hide (taken red here)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) #removing noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1) #removing noise
    
    mask2 = cv2.bitwise_not(mask1)

    #mask1 can be considered as bool true where red area and bool false in the rest of the image
    #mask2 is opposite of mask1 ie. false for red and true for the rest of the image 
    
    res1 = cv2.bitwise_and(background, background, mask = mask1) # res1 = red area replaced with background
    res2 = cv2.bitwise_and(img, img, mask = mask2) #res2 = all except the red area
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) # final output is adding of both parts ie. replaced red and the rest of the image

    out.write(final_output) 
    cv2.imshow(outputfile, final_output)
    k = cv2.waitKey(10) #press escape to exit
    if k == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
