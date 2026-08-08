import cv2
import numpy as np

class GeometryEngine:
    @staticmethod
    def recognize_shape(points_list):
        """
        Takes a list of tuples (x, y) representing a single continuous stroke.
        Returns a tuple (shape_type, shape_data) if recognized, else (None, None).
        """
        if len(points_list) < 15:
            return None, None

        contour = np.array(points_list, dtype=np.int32).reshape((-1, 1, 2))
        
        # We assume it's a closed shape for perimeter calculation if start and end are close
        start_pt = points_list[0]
        end_pt = points_list[-1]
        dist = np.hypot(start_pt[0] - end_pt[0], start_pt[1] - end_pt[1])
        closed = dist < 50
        
        perimeter = cv2.arcLength(contour, closed)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, closed)
        x, y, w, h = cv2.boundingRect(contour)

        # Line Check
        if not closed and (w < 20 or h < 20 or len(approx) == 2):
            return "LINE", (start_pt, end_pt)

        # Only check closed shapes for rect/circle
        if closed:
            area = cv2.contourArea(contour)
            if area == 0:
                return None, None
                
            (cx, cy), radius = cv2.minEnclosingCircle(contour)
            circle_area = np.pi * (radius ** 2)
            
            if circle_area > 0 and (area / circle_area) > 0.75:
                return "CIRCLE", ((int(cx), int(cy)), int(radius))
                
            rect_area = w * h
            if rect_area > 0 and (area / rect_area) > 0.7:
                return "RECTANGLE", (x, y, w, h)

        return None, None
