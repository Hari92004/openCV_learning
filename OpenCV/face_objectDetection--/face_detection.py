import cv2 as cv
face_casecade=cv.CascadeClassifier(r"D:\OpenCV\OpenCV\face_objectDetection--\haarcascade_frontalface_default.xml")

cap=cv.VideoCapture(0)
while True:
    ret,fram=cap.read()
    for frame in fram:
       frame=cv.flip(fram,1)
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces=face_casecade.detectMultiScale(gray,1.1,5)
    
    # detectMultiScale(gray,1.1,5)=scan & detect faces ,1.1 --->balace zoom 
    # mniNeighbors=s
    # """
    #  1.1 → scaleFactor This tells the detector how much to shrink the image at each scale.
    #  1.1 means the image size is reduced 10% at each step.
    #  Smaller values → more scales → more accurate but slower.
    #  Typical values: 1.05 to 1.3
     
    #  2️⃣ 5 → minNeighbors
    #  This sets how many “neighbor detections” each candidate rectangle must have to be kept.
    #  Higher number → fewer false positives.
    #  Lower number → more detections, but more noise.
    #  Typical range: 3–6
    # """
    for (x,y,w,h) in faces :
        cv.rectangle(frame,(x,y),(x+h,y+w),(0,0,255),2)
        
    cv.imshow("webcame face",frame)

    if cv.waitKey(1)& 0xFF==ord('q'):
     break
cap.release()
cv.destroyAllWindows()