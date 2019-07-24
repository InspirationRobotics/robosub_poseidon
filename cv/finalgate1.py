from nms import non_max_suppression_fast
import numpy as np
import cv2
import imutils
import time

#cap = cv2.VideoCapture('high_light_far_approach.mkv')
cap = cv2.VideoCapture('low_light_panning.mkv')

width = int(cap.get(3))
height = int(cap.get(4))
print 'h' + ' ' + str(height) + ' ' + 'w' + ' ' + str(width)
brightness = -100.0
brightness_correction = True
post_hsv_val = 0

while(cap.isOpened()):
            
    	ret, frame = cap.read()
    
    	cap_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    	# lower mask (0-10)
    	lower_red = np.array([10,0,0])
    	upper_red = np.array([30,255,255])
    	mask = cv2.inRange(cap_hsv, lower_red, upper_red)
    	# upper mask (170-180)
    	#lower_red = np.array([140,0,0])
    	#upper_red = np.array([185,255,255])
    	#mask1 = cv2.inRange(cap_hsv, lower_red, upper_red)
    	# join my masks
    	#mask = mask0 + mask1
    
    	output = cv2.bitwise_and(frame, frame, mask = mask)
    
    	#convert images to grayscale
    	gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    	gray = cv2.GaussianBlur(gray, (5,5), 0)
    
    	mask = gray.copy()
    	kernel = np.ones((5,5),np.uint8)
    	eroded = cv2.erode(mask, kernel, iterations=4)
    
    	#Erosions and dilations
    	mask = gray.copy()
    	kernel = np.ones((5,5),np.uint8)
    	dilated = cv2.dilate(eroded, kernel, iterations=3)
    
    	#edge detection
    	#applying edge detection 
    	edged = cv2.Canny(dilated, 30,150)
    
    	#detecting and drawing countours
        cnts, heirarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)
    	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:2]
    
    	boundingBoxes = np.empty((0, 4), float)
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        i = 0 

        # get original brightness values and print them
        roi = frame[0:1920, 0:1080]
        frame_hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        hsv_val = frame_hsv[10][1079][2]
        print("original frame value: %d" % frame_hsv[10][1079][2])
                        
        if post_hsv_val < 230 :
                brightness = brightness + 1
        if post_hsv_val > 240 :
                brightness = brightness - 1

        # apply the change in brightness and contrast
        array_alpha = None
        if (array_alpha is None):
                print(brightness)
                array_alpha = np.array([3.25])
                array_beta = np.array([brightness])
                
                # add a beta value to every pixel
                cv2.add(frame, array_beta, frame)
                
                # multiply every pixel value by alpha
                cv2.multiply(frame, array_alpha, frame)  
        
        
        roi = frame[0:1920, 0:1080]
        frame_hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        post_hsv_val = frame_hsv[10][1079][2]
        print("value after contrast and brightness: %d" % post_hsv_val)
        
    	for c in cnts:
    		x,y,w,h = cv2.boundingRect(c)
    		cv2.rectangle(frame,(x,y), (x+w, y+h), (0,255,0), 2)
    		cv2.imshow("bounding rectangle",frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                if i == 0: 
                  x1 = (x + w/2 )
                  y1 = (y + h/2 )
                  i = 1
                elif i == 1: 
                  x2 = (x + w/2 )
                  y2 = (y + h/2 )

        print("estimated center" + " " + str(((x1 + x2) /2) - (width / 2) ))
        time.sleep(0.1)
        
cap.release()
cv2.destroyAllWindows()
    
