# median bur is image filtering technique which take the middel value and ajust the side value and increases
# the pixel value ---thats how the technique removes the spot,noise from the image-->

import cv2 as cv

image=cv.imread(r"C:\Users\harip\OneDrive\Pictures\noise image.jpeg")
resized_img = cv.resize(image, (720, 480))
# let show the original first tehn we will show the blurr one---
cv.imshow("original image",resized_img)
# teh blur image ---> clear image done by median blur technique-->
blurr=cv.medianBlur(resized_img,5) # isme 5 matrix ya kernel size hai jo 5x5 matrix crry kartah hai and so on-->
cv.imshow("blurred  image -->",blurr)
cv.waitKey(0)
cv.destroyAllWindows()