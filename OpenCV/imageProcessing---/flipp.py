# let flip a image horizontaly and vertically--->
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    flipped_img1=cv2.flip(image,1)#----->verticall
    flipped_img2=cv2.flip(image,0)#----> horizontal
    flipped_img3=cv2.flip(image,-1)#----> both horizontal and verticall
    cv2.imshow("verticall image--->",flipped_img1)
    cv2.imshow("horizontally image--->",flipped_img2)
    cv2.imshow("both ver & horizon image--->",flipped_img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("image not found")