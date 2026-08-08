# # “HSV-based color detection is sensitive to illumination changes.
# I addressed this by dynamically tuning HSV ranges using trackbars and filtering noise through contour analysis.

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.namedWindow("HSV Trackbars")

def nothing(x):
    pass

# Create trackbars
cv2.createTrackbar("H Min", "HSV Trackbars", 0, 179, nothing)
cv2.createTrackbar("H Max", "HSV Trackbars", 179, 179, nothing)
cv2.createTrackbar("S Min", "HSV Trackbars", 0, 255, nothing)
cv2.createTrackbar("S Max", "HSV Trackbars", 255, 255, nothing)
cv2.createTrackbar("V Min", "HSV Trackbars", 0, 255, nothing)
cv2.createTrackbar("V Max", "HSV Trackbars", 255, 255, nothing)

def get_color_name(h, s, v):
    # Black, White, Gray detection
    if v < 50:
        return "Black"
    if s < 40 and v > 200:
        return "White"
    if s < 40:
        return "Gray"

    # Hue based colors
    if h <= 10 or h >= 160:
        return "Red"
    elif 11 <= h <= 20:
        return "Maroon"
    elif 21 <= h <= 25:
        return "Orange"
    elif 26 <= h <= 35:
        return "Yellow"
    elif 36 <= h <= 85:
        return "Green"
    elif 86 <= h <= 95:
        return "Cyan / Aqua"
    elif 96 <= h <= 130:
        return "Blue"
    elif 131 <= h <= 145:
        return "Purple"
    elif 146 <= h <= 160:
        return "Pink / Magenta"
    elif 10 < h < 20 and s > 100:
        return "Brown"
    else:
        return "Unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get HSV values from trackbars
    h_min = cv2.getTrackbarPos("H Min", "HSV Trackbars")
    h_max = cv2.getTrackbarPos("H Max", "HSV Trackbars")
    s_min = cv2.getTrackbarPos("S Min", "HSV Trackbars")
    s_max = cv2.getTrackbarPos("S Max", "HSV Trackbars")
    v_min = cv2.getTrackbarPos("V Min", "HSV Trackbars")
    v_max = cv2.getTrackbarPos("V Max", "HSV Trackbars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Create mask
    mask = cv2.inRange(hsv, lower, upper)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 800:
            x, y, w, h = cv2.boundingRect(cnt)

            # Center pixel
            cx = x + w // 2
            cy = y + h // 2

            h_val, s_val, v_val = hsv[cy, cx]
            b, g, r = frame[cy, cx]

            color_name = get_color_name(h_val, s_val, v_val)
            color_bgr = (int(b), int(g), int(r))

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)

            # Draw color name in same color
            cv2.putText(
                frame,
                color_name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color_bgr,
                2
            )

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
