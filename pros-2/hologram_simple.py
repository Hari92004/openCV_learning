import cv2
import numpy as np
from collections import deque
import math

class SimpleHologramEffect:
    """Simple hologram effect using color detection and hand tracking"""
    
    def __init__(self):
        # Colors to define hand tracking (skin tone range in HSV)
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Neon colors
        self.neon_colors = [
            (255, 0, 127),    # Magenta
            (0, 255, 255),    # Cyan
            (0, 255, 0),      # Green
            (255, 0, 0),      # Blue
            (0, 165, 255),    # Orange
        ]
        
        self.color_idx = 0
        self.trail = deque(maxlen=60)
        self.frame_count = 0
        
    def get_skin_mask(self, frame):
        """Detect skin color to find hand regions"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask using skin tone colors
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        return mask
    
    def find_hand_center(self, mask):
        """Find the center of hand region"""
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                area = cv2.contourArea(largest_contour)
                return (cx, cy), area, largest_contour
        
        return None, 0, None
    
    def draw_hologram_glow(self, frame, x, y, color, radius=25):
        """Draw glowing hologram effect at position"""
        # Multiple circles for glow effect
        for i in range(4):
            alpha = max(0, 1 - i/4)
            glow_color = tuple(int(c * alpha) for c in color)
            thickness = max(1, 4 - i)
            cv2.circle(frame, (int(x), int(y)), radius + i*8, glow_color, thickness)
    
    def draw_energy_waves(self, frame, x, y, color, wave_num):
        """Draw energy wave patterns"""
        radius = 30 + (wave_num * 15) % 60
        cv2.circle(frame, (x, y), radius, color, 2)
    
    def draw_particle_burst(self, frame, x, y, color, intensity=0.7):
        """Draw particle burst effect"""
        num_particles = 12
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * np.pi
            length = np.random.randint(20, 80)
            px = int(x + length * np.cos(angle))
            py = int(y + length * np.sin(angle))
            line_color = tuple(int(c * intensity) for c in color)
            cv2.line(frame, (x, y), (px, py), line_color, 2)
    
    def draw_laser_trail(self, frame, trail_points, color):
        """Draw laser trail from finger movement"""
        if len(trail_points) > 1:
            for i in range(1, len(trail_points)):
                alpha = i / len(trail_points)
                trail_color = tuple(int(c * alpha * 0.8) for c in color)
                thickness = max(1, int(3 * alpha))
                cv2.line(frame, trail_points[i-1], trail_points[i], trail_color, thickness)
    
    def process_frame(self, frame):
        """Process frame and add hologram effects"""
        self.frame_count += 1
        h, w, c = frame.shape
        
        # Get skin mask
        mask = self.get_skin_mask(frame)
        
        # Find hand center
        hand_pos, area, contour = self.find_hand_center(mask)
        
        # Create hologram overlay
        hologram_overlay = frame.copy()
        
        if hand_pos is not None and area > 500:
            hx, hy = hand_pos
            
            # Add to trail
            self.trail.append((hx, hy))
            
            # Cycle through colors
            color = self.neon_colors[self.color_idx % len(self.neon_colors)]
            self.color_idx += 1
            
            # Draw hologram effects
            self.draw_hologram_glow(hologram_overlay, hx, hy, color, 30)
            
            # Draw energy waves
            for i in range(3):
                self.draw_energy_waves(hologram_overlay, hx, hy, color, i)
            
            # Draw laser trail
            trail_list = list(self.trail)
            self.draw_laser_trail(hologram_overlay, trail_list, color)
            
            # Draw hand contour with neon effect
            if contour is not None:
                cv2.drawContours(hologram_overlay, [contour], 0, color, 3)
            
            # Draw particle burst effect intermittently
            if self.frame_count % 30 == 0:
                self.draw_particle_burst(hologram_overlay, hx, hy, color, 0.6)
            
            # Get approximate hand size for finger points
            if contour is not None:
                x, y, w_c, h_c = cv2.boundingRect(contour)
                
                # Detect approximate finger tips using contour
                hull = cv2.convexHull(contour)
                if len(hull) > 5:
                    # Draw finger tips with glow
                    for point in hull[::len(hull)//5]:  # Sample some points
                        px, py = point[0]
                        cv2.circle(hologram_overlay, (px, py), 8, color, -1)
                        cv2.circle(hologram_overlay, (px, py), 12, color, 2)
            
            # Display hand info
            cv2.putText(hologram_overlay, f"Hand Area: {int(area)}", 
                       (hx - 60, hy - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(hologram_overlay, f"X:{hx} Y:{hy}", 
                       (hx - 60, hy + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        else:
            # Clear trail if hand not detected
            self.trail.clear()
        
        # Blend hologram overlay with original frame
        result = cv2.addWeighted(frame, 0.6, hologram_overlay, 0.4, 0)
        
        return result
    
    def run(self):
        """Main execution loop"""
        cap = cv2.VideoCapture(0)
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("=" * 60)
        print("🌌 HOLOGRAM HAND GESTURE PROJECT")
        print("=" * 60)
        print("✨ Features:")
        print("   - Real-time hand detection using color detection")
        print("   - Dynamic neon glow effects")
        print("   - Energy waves that follow your hand")
        print("   - Laser trail effects")
        print("   - Particle burst animations")
        print("=" * 60)
        print("👋 Controls:")
        print("   - Show your hand to the camera")
        print("   - Move your hand around to create effects")
        print("   - Press 'q' to quit")
        print("   - Press 'space' to clear trail")
        print("=" * 60)
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame
            result = self.process_frame(frame)
            
            # Add FPS and info
            frame_count += 1
            cv2.putText(result, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(result, "Press 'q' to quit | 'space' to clear", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 1)
            
            cv2.imshow("🌌 Hologram Hand Gesture", result)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n✨ Hologram effect ended!")
                break
            elif key == ord(' '):
                print("🔄 Trail cleared!")
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hologram = SimpleHologramEffect()
    hologram.run()
