# lets know how the opencv reads  the images------>
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is None:
    print("image is not found")
     # agar koi key press hota hai then just close the window...
else:
    print("image is uploaded sucessfully") 
    cv2.imshow("hello guys this is my billa",image)  # open the window
    cv2.waitKey(0)  # jab tak koi key press nhi hota tab tak image show karte rahe--->
    cv2.destroyAllWindows()