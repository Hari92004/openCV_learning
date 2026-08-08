# lets crop a image by using slicing in openCV---->
import cv2
image = cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    cv2.imshow("original image",image)
    cropped_image=image[200:900,200:750]
    cv2.imshow("cropped image",cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("image showing is completed--->")
else:
    print("image is not found")