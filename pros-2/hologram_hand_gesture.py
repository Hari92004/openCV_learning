import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import math

class HologramEffect:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Color palettes for hologram effect
        self.neon_colors = [
            (255, 0, 127),    # Magenta
            (0, 255, 255),    # Cyan
            (0, 255, 0),      # Green
            (255, 0, 0),      # Blue
            (0, 165, 255),    # Orange
        ]
        
        # Particle trails for each hand
        self.trail_points = deque(maxlen=50)
        self.fingertip_trails = {i: deque(maxlen=30) for i in range(21)}
        
    def get_distance(self, p1, p2):
        """Calculate distance between two points"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def draw_hologram_glow(self, frame, x, y, color, radius=20):
        """Draw glowing hologram effect"""
        # Multiple circles for glow effect
        for i in range(3):
            alpha = (1 - i/3)
            glow_color = tuple(int(c * alpha) for c in color)
            cv2.circle(frame, (int(x), int(y)), radius + i*5, glow_color, 1)
    
    def draw_particle_effects(self, frame, x, y, color):
        """Draw particle burst effect"""
        num_particles = 8
        radius = 30
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * np.pi
            px = int(x + radius * np.cos(angle))
            py = int(y + radius * np.sin(angle))
            cv2.line(frame, (int(x), int(y)), (px, py), color, 1)
    
    def detect_gesture(self, hand_landmarks, handedness):
        """Simple gesture detection"""
        # Get key points
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        
        palm_center = hand_landmarks.landmark[0]
        
        # Calculate distances
        thumb_index_dist = self.get_distance(
            (thumb_tip.x, thumb_tip.y),
            (index_tip.x, index_tip.y)
        )
        
        # Peace sign (index and middle fingers up)
        if thumb_index_dist > 0.1:
            return "PEACE"
        
        # Rock sign (index and pinky up, middle and ring down)
        if (index_tip.y < middle_tip.y and 
            pinky_tip.y < ring_tip.y and 
            thumb_index_dist > 0.1):
            return "ROCK"
        
        # Open hand (all fingers spread)
        finger_distances = [
            self.get_distance((thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y)),
            self.get_distance((index_tip.x, index_tip.y), (middle_tip.x, middle_tip.y)),
            self.get_distance((middle_tip.x, middle_tip.y), (ring_tip.x, ring_tip.y)),
            self.get_distance((ring_tip.x, ring_tip.y), (pinky_tip.x, pinky_tip.y))
        ]
        
        if all(d > 0.05 for d in finger_distances):
            return "OPEN_HAND"
        
        # Fist (all fingers down)
        if all(f.y > palm_center.y + 0.1 for f in [index_tip, middle_tip, ring_tip, pinky_tip]):
            return "FIST"
        
        return "NONE"
    
    def process_frame(self, frame):
        """Process video frame and apply hologram effects"""
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        # Create hologram overlay
        hologram_overlay = frame.copy()
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness_info in zip(
                results.multi_hand_landmarks, 
                results.multi_handedness
            ):
                # Get hand position
                hand_center_x = int(hand_landmarks.landmark[9].x * w)
                hand_center_y = int(hand_landmarks.landmark[9].y * h)
                
                # Detect gesture
                gesture = self.detect_gesture(hand_landmarks, handedness_info)
                
                # Choose color based on handedness
                if handedness_info.classification[0].label == "Right":
                    color = self.neon_colors[0]  # Magenta for right hand
                else:
                    color = self.neon_colors[1]  # Cyan for left hand
                
                # Draw hologram effects
                self.draw_hologram_glow(hologram_overlay, hand_center_x, hand_center_y, color, 25)
                
                # Draw fingertip trails
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    lx = int(landmark.x * w)
                    ly = int(landmark.y * h)
                    
                    # Store fingertip positions
                    if idx in self.fingertip_trails:
                        self.fingertip_trails[idx].append((lx, ly))
                        
                        # Draw trail
                        trail = list(self.fingertip_trails[idx])
                        for i in range(1, len(trail)):
                            alpha = i / len(trail)
                            trail_color = tuple(int(c * alpha * 0.7) for c in color)
                            cv2.line(hologram_overlay, trail[i-1], trail[i], trail_color, 1)
                    
                    # Draw fingertip with glow
                    cv2.circle(hologram_overlay, (lx, ly), 5, color, -1)
                    cv2.circle(hologram_overlay, (lx, ly), 8, color, 1)
                
                # Draw hand mesh with neon effect
                for connection in mp.solutions.hands.HAND_CONNECTIONS:
                    start = hand_landmarks.landmark[connection[0]]
                    end = hand_landmarks.landmark[connection[1]]
                    
                    start_pos = (int(start.x * w), int(start.y * h))
                    end_pos = (int(end.x * w), int(end.y * h))
                    
                    cv2.line(hologram_overlay, start_pos, end_pos, color, 2)
                
                # Apply gesture-based effects
                if gesture == "PEACE":
                    self.draw_particle_effects(hologram_overlay, hand_center_x, hand_center_y, color)
                elif gesture == "ROCK":
                    # Rock effect - circular waves
                    cv2.circle(hologram_overlay, (hand_center_x, hand_center_y), 50, color, 1)
                    cv2.circle(hologram_overlay, (hand_center_x, hand_center_y), 70, color, 1)
                elif gesture == "OPEN_HAND":
                    # Explosion effect
                    for _ in range(12):
                        angle = np.random.rand() * 2 * np.pi
                        length = np.random.randint(20, 60)
                        px = int(hand_center_x + length * np.cos(angle))
                        py = int(hand_center_y + length * np.sin(angle))
                        cv2.line(hologram_overlay, (hand_center_x, hand_center_y), (px, py), color, 1)
                
                # Display gesture text
                gesture_color = (0, 255, 0) if gesture != "NONE" else (100, 100, 100)
                cv2.putText(hologram_overlay, f"Gesture: {gesture}", 
                           (hand_center_x - 50, hand_center_y - 80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, gesture_color, 2)
        
        # Blend hologram overlay with original frame
        result = cv2.addWeighted(frame, 0.5, hologram_overlay, 0.5, 0)
        
        return result
    
    def run(self):
        """Main execution loop"""
        cap = cv2.VideoCapture(0)
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Hologram Hand Gesture Project Started!")
        print("Controls:")
        print("   - Show your hand to the camera")
        print("   - Try different gestures: PEACE, ROCK, OPEN_HAND, FIST")
        print("   - Press 'q' to quit")
        print("=" * 50)
        
        cv2.namedWindow("Hologram Hand Gesture", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Hologram Hand Gesture", cv2.WND_PROP_TOPMOST, 1)
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame with hologram effects
            result = self.process_frame(frame)
            
            # Add info display
            frame_count += 1
            fps = cap.get(cv2.CAP_PROP_FPS)
            cv2.putText(result, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(result, "Press 'q' to quit", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 1)
            
            # Display result
            cv2.imshow("Hologram Hand Gesture", result)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nHologram effect ended!")
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hologram = HologramEffect()
    hologram.run()
