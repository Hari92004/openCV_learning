import cv2 as cv
import numpy as np

image=cv.imread(r"C:\Users\harip\OneDrive\Pictures\blurr.jpg")
resized_img = cv.resize(image, (720, 480))
# let show the original first tehn we will show the blurr one---
cv.imshow("original image",resized_img)
kernel1 = np.array([
    [ 0,  0, -1,  0,  0],
    [ 0, -1, -2, -1,  0],
    [-1, -2, 17, -2, -1],
    [ 0, -1, -2, -1,  0],
    [ 0,  0, -1,  0,  0]
])
# the blur image ---> clear image done by median blur technique-->
blurr=cv.filter2D(resized_img,0,kernel1) # 3 x 3 matrix 
cv.imshow("clear image -->",blurr)
cv.waitKey(0)
cv.destroyAllWindows()