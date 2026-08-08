# resizing the image by using the .resize shape---->
import cv2
image = cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    print("image load sucessfully")
    resixe=cv2.resize(image,(800,800)) # we can chage the pixel value here 
    cv2.imshow("resize image--",resixe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("image is not found")