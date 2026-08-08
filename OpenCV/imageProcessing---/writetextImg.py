# let write tsxt on image using the line function of te  openCV
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    org=(640,275)
    thickness=2
    draw=cv2.putText(image,"this is my billa",org,cv2.FONT_HERSHEY_COMPLEX,2.0,(0,0,255),thickness)
    cv2.imshow("write text on image--->",draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """yaha pe org text ka starting point hai jo ki x and y ki value hai ,uske baad font apply hua hai """
#  yaha 2.0 --->font scale hai and thickness letter ki motai hai 