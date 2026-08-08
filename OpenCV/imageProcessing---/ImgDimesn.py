#lets discuss about the dimenssion of an image---->
import cv2
image=cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")
if image is not None:
    h,w,c=image.shape
    print(f"image loaded \nHeight :{h} \nWidth :{w} \nChannel: {c}")
else:
    print("image is not found")
# print(image.shape)
    