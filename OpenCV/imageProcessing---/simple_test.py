import cv2
import numpy as np

# Create a black image (300x300)
img = np.zeros((300, 300, 3), dtype=np.uint8)

# Draw a green rectangle
cv2.rectangle(img, (50, 50), (250, 250), (0, 255, 0), 3)

# Put some text
cv2.putText(
    img,
    "OpenCV Test",
    (60, 160),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 255, 255),
    2
)

# Show the image
cv2.imshow("Simple OpenCV Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
