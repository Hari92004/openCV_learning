# let draw a rectangle  using the line function of te  openCV
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    pt1=(566,246)
    pt2=(712,280)
    color=(0,0,255)
    thickness=4
    draw=cv2.rectangle(image,pt1,pt2,color,thickness)
    cv2.imshow("line drew image--->",draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()