import cv2 as cv

face_casecade=cv.CascadeClassifier(r"D:\OpenCV\OpenCV\face_objectDetection--\haarcascade_frontalface_default.xml")
eye_detect=cv.CascadeClassifier(r"D:\OpenCV\OpenCV\face_objectDetection--\haarcascade_eye.xml")
smile_detect=cv.CascadeClassifier(r"D:\OpenCV\OpenCV\face_objectDetection--\haarcascade_smile.xml")

cap=cv.VideoCapture(0)
while True:
    ret,fram=cap.read()
    
    frame=cv.flip(fram,1)
    gray=cv.cvtColor(frame,cv.COLOR_RGB2GRAY)
    faces=face_casecade.detectMultiScale(gray,1.1,10) # here u can change the nwighbors no.
    
    for (x,y,w,h) in faces :
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
        roi_gray=gray[y:y+h,x:x+w] # gray image me y ka move y --> y+h tak and x move ---> x to x+w
        roi_color=frame[y:y+h,x:x+w] # ye rgb frame ke liye x an dy ka move 
        
        eyes=eye_detect.detectMultiScale(roi_gray,1.1,10)
        if len(eyes):
           cv.putText(frame,"eye detected",(x,y-30),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        smile=smile_detect.detectMultiScale(roi_gray,1.1,10)
        if len(smile):
           cv.putText(frame,"smile detected",(x,y-5),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
    cv.imshow("smart face detection",frame)

    if cv.waitKey(1)& 0xFF==ord('q'):
     break
cap.release()
cv.destroyAllWindows()
    