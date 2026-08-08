# lets know how the save  the images in the memory------>
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is None:
    print("image is not found")
     # agar koi key press hota hai then just close the window...
else:
    sucess=cv2.imwrite("billu.jpg",image)
    if sucess:
     print("image is saved sucessfully") 
    