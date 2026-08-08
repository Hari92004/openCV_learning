# Multi Color Detection using OpenCV (HSV based)
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# HSV color ranges
colors = {
    "Red": [
        (np.array([0, 120, 70]), np.array([10, 255, 255])),
        (np.array([170, 120, 70]), np.array([180, 255, 255]))
    ],
    "Green": [
        (np.array([35, 100, 50]), np.array([85, 255, 255]))
    ],
    "Blue": [
        (np.array([100, 150, 50]), np.array([140, 255, 255]))
    ],
    "Yellow": [
        (np.array([20, 100, 100]), np.array([30, 255, 255]))
    ],
    "Orange": [
        (np.array([10, 100, 100]), np.array([20, 255, 255]))
    ],
    "Purple": [
        (np.array([130, 50, 50]), np.array([160, 255, 255]))
    ],
    "Pink": [
        (np.array([160, 100, 100]), np.array([170, 255, 255]))
    ],
    "Cyan": [
        (np.array([85, 100, 100]), np.array([100, 255, 255]))
    ],
    "White": [
        (np.array([0, 0, 200]), np.array([180, 50, 255]))
    ],
    "Black": [
        (np.array([0, 0, 0]), np.array([180, 255, 50]))
    ],
    "Gray": [
        (np.array([0, 0, 50]), np.array([180, 50, 200]))
    ]
}

# BGR values for drawing text/box (OpenCV uses BGR)
color_bgr = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
    "Orange": (0, 165, 255),
    "Purple": (128, 0, 128),
    "Pink": (203, 192, 255),
    "Cyan": (255, 255, 0),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128)
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, ranges in colors.items():
        mask = None

        # Combine masks (important for RED which has two ranges)
        for lower, upper in ranges:
            temp_mask = cv2.inRange(hsv, lower, upper)
            mask = temp_mask if mask is None else mask + temp_mask

        # Noise removal
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 800:
                x, y, w, h = cv2.boundingRect(cnt)

                # Draw rectangle in same color
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h),
                    color_bgr[color_name], 2
                )

                # Black outline for readability
                cv2.putText(
                    frame, color_name, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 0), 4
                )

                # Colored text
                cv2.putText(
                    frame, color_name, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    color_bgr[color_name], 2
                )

    cv2.imshow("Multi Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
