# let rotate the image--->
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    h,w,c=image.shape
    print(f"image loaded \nHeight :{h} \nWidth :{w} \nChannel: {c}")
    center_point=(h//2,w//2)
    m=cv2.getRotationMatrix2D(center_point,90,1.0)
    rotate_img=cv2.warpAffine(image,m,(w,h))
    cv2.imshow("rotated image--->",rotate_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("image not found")