import cv2
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read() # read the all frame ---
    if not ret:
        print("camera is not found")
        break
    org=(213,108)
    thickness=1
    draw=cv2.putText(frame,"iiH",org,cv2.FONT_HERSHEY_COMPLEX,1.0,(0,0,255),thickness)
    cv2.imshow("webcame feed",cv2.flip(draw,1)) #it will show the capture frame--->
    
    if cv2.waitKey(1) & 0xFF==ord('q'): # wait for keypress q for 1 mili sec ,if press then quit from the it
# here  the meaning of ord is it will give the ascii value of the given char--->
        print("quitting...")
        break

cap.release() #its mean just stop to access the camera and stop capturing the video
cv2.destroyAllWindows() # the running part will be close-->