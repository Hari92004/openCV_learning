import cv2 as cv

input1=cv.imread(r"D:\all file of mine\photo.jpeg")
image = cv.resize(input1, (600, 450)) # resizing the image for proper vies on window-->
blurr=cv.GaussianBlur(image,(9,9),5)

# let show the image --->
cv.imshow("original image",image)
cv.imshow("blurr image",blurr)
cv.waitKey(0)
cv.destroyAllWindows()