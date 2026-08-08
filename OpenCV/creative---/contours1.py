import cv2 as cv

# Open webcam
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally
    frame = cv.flip(frame, 1)
    
    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, threshold = cv.threshold(gray, 130, 255, cv.THRESH_BINARY)
    
    # Find contours
    contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original frame
    cv.drawContours(frame, contours, -1, (0, 0, 255), 2)
    
    # Show the result
    cv.imshow("Contours", frame)
    
    # Press 'q' to quit
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv.destroyAllWindows()
