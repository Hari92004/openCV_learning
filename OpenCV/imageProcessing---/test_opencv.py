import cv2
import numpy as np

# Create a white image (300x300)
img = np.ones((300, 300, 3), dtype=np.uint8) * 255

# Draw a blue circle
cv2.circle(img, (150, 150), 80, (255, 0, 0), 3)

# Show the image
cv2.imshow("Second OpenCV Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
