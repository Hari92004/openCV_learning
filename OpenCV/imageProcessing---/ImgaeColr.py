# let understand how can we change the image color and modifiy it--->
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray image hai ye--",gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("the image is not found")