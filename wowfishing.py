import cv2 
import numpy as np
from PIL import ImageGrab
from PIL import Image
import time

def nothing(x):
	pass

#screen resolution
width = 2560
height = 1440


#states
fishing = False
bite = False



# create trackbars for color change
cv2.namedWindow("trackbars", cv2.WINDOW_NORMAL)
cv2.createTrackbar('u1',"trackbars",0,255,nothing)
cv2.createTrackbar('l1',"trackbars",0,255,nothing)
cv2.createTrackbar('u2',"trackbars",0,255,nothing)
cv2.createTrackbar('l2',"trackbars",0,255,nothing)
cv2.createTrackbar('u3',"trackbars",0,255,nothing)
cv2.createTrackbar('l3',"trackbars",0,255,nothing)

#cv2.namedWindow("trackbars2", cv2.WINDOW_NORMAL)
#cv2.createTrackbar('erosion',"trackbars2",0,20,nothing)

def filterFrameforLure(img):
	
	# get current positions of four trackbars
	# u1 = cv2.getTrackbarPos('u1',"trackbars")
	# l1 = cv2.getTrackbarPos('l1',"trackbars")
	# u2 = cv2.getTrackbarPos('u2',"trackbars")
	# l2 = cv2.getTrackbarPos('l2',"trackbars")
	# u3 = cv2.getTrackbarPos('u3',"trackbars")
	# l3 = cv2.getTrackbarPos('l3',"trackbars")

	#WC TEST
	u1 = 255
	l1 = 0
	u2 = 139
	l2 = 20
	u3 = 117
	l3 = 12

	lower = np.array([l1,l2,l3])
	upper = np.array([u1,u2,u3])

	mask = cv2.inRange(img, lower, upper)
	#res = cv2.bitwise_and(frame,frame, mask= mask)

	#Erosion
	#		erosion_value = cv2.getTrackbarPos('erosion',"trackbars2")
	erosion_value1 = 0
	kernel = np.ones((erosion_value1, erosion_value1), np.uint8)
	mask = cv2.erode(mask, kernel, iterations=1)

	return mask


while(True):
	#motion detection
	
	#	frame1
	img = ImageGrab.grab(bbox=((width/2)-100,(height/2)-100,(width/2)+100,(height/2)+100)) #returned as BGR
	img = np.array(img)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	frame1 = filterFrameforLure(img)
	#	frame2
	img = ImageGrab.grab(bbox=((width/2)-100,(height/2)-100,(width/2)+100,(height/2)+100)) #returned as BGR
	img = np.array(img)
	origional = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # for gui
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	frame2 = filterFrameforLure(img)


	#find center of lure
	try:

		#	find biggest contour
		contours,hierarchy = cv2.findContours(frame2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnt = max(contours, key = cv2.contourArea)

		#	find center
		M = cv2.moments(cnt)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		# draw the contour and center of the shape on the image
		cv2.drawContours(origional, cnt, -1, (0, 255, 0), 2)
		cv2.circle(origional, (cX, cY), 5, (0, 0, 255), -1)
		cv2.putText(origional, "center", (cX - 30, cY - 60),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		fishing = True
	except:
		print("Failed detecting lure")
		fishing = False


	#check if motion is detected

	delta = cv2.absdiff(frame1, frame2)

	#	erosion 
	# erosion_value = cv2.getTrackbarPos('erosion',"trackbars2")
	# kernel = np.ones((erosion_value, erosion_value), np.uint8)
	# delta = cv2.erode(delta, kernel, iterations=1)

	motion_score = cv2.countNonZero(delta)

	if (motion_score > 80):
		bite = True
		print("Fish on the line!!!")
	else:
		bite = False


	#Game input Send click command to lure
	# if (fishing and bite):
	# 	clickSomeShit()
	# else:
	#	stop any existing thread
	# 	castline() - start fishing timer thread - time.sleep(1.5)
	#	
	# 	


	#display
	

	cv2.imshow('delta',delta)
	cv2.imshow('filter',frame1)

	cv2.putText(origional, "Fishing: " + str(fishing), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
	cv2.putText(origional, "Motion: " + str(motion_score), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2) 
	cv2.putText(origional, "Bite: " + str(bite), (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2) 
	cv2.imshow('origional',origional)
	
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
