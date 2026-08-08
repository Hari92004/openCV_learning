# let draw a line using the line function of te  openCV
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    center=(638,272) # value of x and y value
    radius=100 #  --->it is in pixel 
    color=(0,0,255)
    thickness=-1# it will fill whole the circle with red color
    draw=cv2.circle(image,center,radius,color,thickness)
    cv2.imshow("line drew image--->",draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()