import cv2 as cv
cap=cv.VideoCapture(0)
while True:
    ret,frame=cap.read() # read the all frame ---
    vdo=cv.flip(frame,1)
    canny=cv.cvtColor(vdo, cv.COLOR_BGR2GRAY) # convert the rgb frame to grayscale---
    video=cv.Canny(canny,50,150)
    if not ret:
        print("camera is not found")
        break
    cv.imshow("original video",vdo) #it will show the capture frame--->
    cv.imshow("canny video",video)
    
    if cv.waitKey(1) & 0xFF==ord('q'): # wait for keypress q for 1 mili sec ,if press then quit from the it
# here  the meaning of ord is it will give the ascii value of the given char--->
        print("quitting...")
        break

cap.release() #its mean just stop to access the camera and stop capturing the video
cv.destroyAllWindows()