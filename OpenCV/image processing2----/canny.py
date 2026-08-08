import cv2 as cv

image=cv.imread(r"C:\Users\harip\OneDrive\Pictures\blurr.jpg",cv.IMREAD_GRAYSCALE)
edges=cv.Canny(image,50,150) 
"""After grayscale conversion, the Canny algorithm detects edges based on intensity gradients.
The lower threshold (50) identifies weak edges, while the upper threshold (150) identifies strong edges.
Weak edges are retained only if they are connected to strong edges, producing thin and accurate boundaries."""
cv.imshow("original image",image)
cv.imshow("canny image",edges)
cv.waitKey(0)
cv.destroyAllWindows()