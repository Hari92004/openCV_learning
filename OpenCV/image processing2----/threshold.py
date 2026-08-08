# yeh ek image processing tehnique hai jo ek image ko pure black and white me convert karta hai---->
import cv2 as cv

image=cv.imread(r"C:\Users\harip\OneDrive\Pictures\blurr.jpg",cv.IMREAD_GRAYSCALE)
ret,edges=cv.threshold(image,130,225,cv.THRESH_BINARY) 
# yaha pe cv.THRESH_BINARY--> binary convert like 0 & 1 ,130<=pixel is for black and vice versa
cv.imshow("original image",image)
cv.imshow("threshold image",edges)
cv.waitKey(0)
cv.destroyAllWindows()