# lets draw on image based on contour---
import cv2 as cv

image=cv.imread(r"C:\Users\harip\OneDrive\Pictures\shape.avif")
gray=cv.cvtColor(image,cv.COLOR_RGB2GRAY)
_,threshold=cv.threshold(gray,130,255,cv.THRESH_BINARY)

#  find contour--->
contours, hierarchy=cv.findContours(threshold,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
# let draw it on image--->
# cv2.drawContours(image, contours, contour_index, color, thickness)
cv.drawContours(image,contours,-1,(0,0,255),1)
# here contour index tells about what to draw based on value like -1 --> draw all,1-->only outlinec
cv.imshow("contours",image)
cv.waitKey(0)
cv.destroyAllWindows()