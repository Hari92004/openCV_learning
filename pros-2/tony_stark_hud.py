import cv2
import numpy as np
from collections import deque
import math

class IronManHUD:
    """Tony Stark JARVIS-style HUD with hand tracking and AR effects"""
    
    def __init__(self):
        # Iron Man colors - neon blue and cyan
        self.primary_color = (255, 165, 0)    # Cyber blue
        self.secondary_color = (0, 255, 255)  # Cyan
        self.accent_color = (255, 0, 127)     # Magenta
        
        # Skin detection
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        self.trail = deque(maxlen=80)
        self.frame_count = 0
        self.scan_angle = 0
        
    def draw_corner_markers(self, frame, color, thickness=3, size=30):
        """Draw corner markers like a scanner"""
        h, w = frame.shape[:2]
        
        # Top-left
        cv2.line(frame, (0, 0), (size, 0), color, thickness)
        cv2.line(frame, (0, 0), (0, size), color, thickness)
        
        # Top-right
        cv2.line(frame, (w-size, 0), (w, 0), color, thickness)
        cv2.line(frame, (w, 0), (w, size), color, thickness)
        
        # Bottom-left
        cv2.line(frame, (0, h-size), (0, h), color, thickness)
        cv2.line(frame, (0, h-size), (size, h-size), color, thickness)
        
        # Bottom-right
        cv2.line(frame, (w-size, h), (w, h), color, thickness)
        cv2.line(frame, (w, h), (w, h-size), color, thickness)
    
    def draw_scanning_circles(self, frame, cx, cy, color, num_circles=5):
        """Draw expanding scanning circles"""
        for i in range(num_circles):
            radius = 20 + (i * 15)
            alpha = max(0, 1 - i / num_circles)
            circle_color = tuple(int(c * alpha) for c in color)
            cv2.circle(frame, (cx, cy), radius, circle_color, 2)
    
    def draw_crosshair(self, frame, cx, cy, color, size=40):
        """Draw targeting crosshair"""
        # Horizontal line
        cv2.line(frame, (cx - size, cy), (cx - size//2, cy), color, 2)
        cv2.line(frame, (cx + size//2, cy), (cx + size, cy), color, 2)
        
        # Vertical line
        cv2.line(frame, (cx, cy - size), (cx, cy - size//2), color, 2)
        cv2.line(frame, (cx, cy + size//2), (cx, cy + size), color, 2)
        
        # Center dot
        cv2.circle(frame, (cx, cy), 5, color, -1)
    
    def draw_hexagon(self, frame, cx, cy, radius, color, thickness=2):
        """Draw hexagon around target"""
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            points.append([x, y])
        points = np.array(points, dtype=np.int32)
        cv2.polylines(frame, [points], True, color, thickness)
    
    def draw_grid(self, frame, spacing=50, color=(0, 255, 255)):
        """Draw digital grid overlay"""
        h, w = frame.shape[:2]
        color_dim = tuple(int(c * 0.2) for c in color)
        
        for y in range(0, h, spacing):
            cv2.line(frame, (0, y), (w, y), color_dim, 1)
        for x in range(0, w, spacing):
            cv2.line(frame, (x, 0), (x, h), color_dim, 1)
    
    def draw_data_bars(self, frame, cx, cy):
        """Draw data analysis bars"""
        bar_width = 80
        bar_height = 200
        bar_x = cx - bar_width // 2
        bar_y = cy - bar_height // 2
        
        # Power bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                     self.secondary_color, 2)
        fill_height = int(bar_height * 0.7)
        cv2.rectangle(frame, (bar_x + 2, bar_y + bar_height - fill_height - 2), 
                     (bar_x + bar_width - 2, bar_y + bar_height - 2), 
                     self.primary_color, -1)
    
    def draw_target_lock(self, frame, cx, cy, lock_status="ARMED"):
        """Draw lock-on indicator"""
        color = (0, 255, 0) if lock_status == "LOCKED" else self.accent_color
        
        # Lock animation
        size = 60
        cv2.rectangle(frame, (cx - size, cy - size), (cx + size, cy + size), color, 2)
        cv2.circle(frame, (cx, cy), size + 10, color, 1)
        
        # Status text
        status_color = (0, 255, 0) if lock_status == "LOCKED" else (0, 165, 255)
        cv2.putText(frame, f"TARGETING: {lock_status}", (cx - 80, cy - 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    
    def get_skin_mask(self, frame):
        """Detect hand using skin color"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return mask
    
    def find_hand_center(self, mask):
        """Find hand position"""
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                area = cv2.contourArea(largest_contour)
                return (cx, cy), area, largest_contour
        
        return None, 0, None
    
    def process_frame(self, frame):
        """Apply JARVIS-style HUD effects"""
        self.frame_count += 1
        h, w = frame.shape[:2]
        
        # Create HUD overlay
        hud_overlay = frame.copy()
        
        # Draw background grid
        self.draw_grid(hud_overlay, spacing=60, color=(0, 255, 255))
        
        # Draw corner markers (scanner frame)
        self.draw_corner_markers(hud_overlay, self.secondary_color, thickness=4, size=50)
        
        # Get hand position
        mask = self.get_skin_mask(frame)
        hand_pos, area, contour = self.find_hand_center(mask)
        
        if hand_pos is not None and area > 500:
            hx, hy = hand_pos
            self.trail.append((hx, hy))
            
            # Draw targeting system
            self.draw_target_lock(hud_overlay, hx, hy, "TRACKING")
            
            # Draw scanning circles
            self.draw_scanning_circles(hud_overlay, hx, hy, self.primary_color, num_circles=4)
            
            # Draw crosshair
            self.draw_crosshair(hud_overlay, hx, hy, self.secondary_color, size=50)
            
            # Draw hexagon
            self.draw_hexagon(hud_overlay, hx, hy, 80, self.accent_color, thickness=2)
            
            # Draw data bars
            self.draw_data_bars(hud_overlay, hx, hy)
            
            # Draw hand contour
            if contour is not None:
                cv2.drawContours(hud_overlay, [contour], 0, self.secondary_color, 3)
            
            # Draw laser trail
            if len(self.trail) > 1:
                trail_list = list(self.trail)
                for i in range(1, len(trail_list)):
                    alpha = i / len(trail_list)
                    trail_color = tuple(int(c * alpha * 0.6) for c in self.primary_color)
                    thickness = max(1, int(3 * alpha))
                    cv2.line(hud_overlay, trail_list[i-1], trail_list[i], trail_color, thickness)
            
            # Display hand stats
            cv2.putText(hud_overlay, f"TARGET ID: HAND", (20, h-80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.secondary_color, 2)
            cv2.putText(hud_overlay, f"DISTANCE: {int(area)} units", (20, h-50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.secondary_color, 2)
            cv2.putText(hud_overlay, f"POSITION: ({hx}, {hy})", (20, h-20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.secondary_color, 2)
        else:
            self.trail.clear()
            cv2.putText(hud_overlay, "NO TARGET DETECTED", (w//2 - 150, h//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        
        # Add scanning line effect
        scan_y = int(h * (self.frame_count % 100) / 100)
        cv2.line(hud_overlay, (0, scan_y), (w, scan_y), (0, 255, 0), 1)
        
        # Add frame info
        cv2.putText(hud_overlay, f"FRAME: {self.frame_count}", (w-250, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.accent_color, 2)
        cv2.putText(hud_overlay, "JARVIS SYSTEM ONLINE", (w-250, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Blend with original
        result = cv2.addWeighted(frame, 0.4, hud_overlay, 0.6, 0)
        
        return result
    
    def run(self):
        """Main execution loop"""
        cap = cv2.VideoCapture(0)
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not cap.isOpened():
            print("❌ Camera not found!")
            return
        
        print("=" * 60)
        print("🤖 TONY STARK JARVIS-STYLE HUD")
        print("=" * 60)
        print("✨ Features:")
        print("   - Real-time hand tracking")
        print("   - Digital grid overlay")
        print("   - Targeting system with lock-on")
        print("   - Scanning circles and crosshairs")
        print("   - Data visualization bars")
        print("   - Laser trail effects")
        print("=" * 60)
        print("👋 Show your hand to activate targeting")
        print("⌨️  Press 'q' to quit")
        print("=" * 60 + "\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            result = self.process_frame(frame)
            
            cv2.imshow("JARVIS HUD System", result)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n🔴 JARVIS system offline")
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hud = IronManHUD()
    hud.run()
