# let save a recorded video through openCV-------->
import cv2
camera=cv2.VideoCapture(0)

frame_width=int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height=int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

codec=cv2.VideoWriter_fourcc(*'XVID')
recored=cv2.VideoWriter("recorded_video.avi",codec,30,(frame_width,frame_height))
# yaha avi -->audio video interleave
while True:
    success,image=camera.read()
    if not success:
        break
    recored.write(image)
    cv2.imshow("live recording",image)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
       break

camera.release()
recored.release()
cv2.destroyAllWindows()