import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import math
import time

class TonyStarkHologram:
    def __init__(self):
        # MediaPipe Hands
        import mediapipe.solutions.hands as mp_hands
        import mediapipe.solutions.drawing_utils as mp_draw
        self.mp_hands = mp_hands
        self.mp_draw = mp_draw
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Colors (Tony Stark Style)
        self.cyan = (255, 255, 0)      # Neon Cyan
        self.orange = (0, 165, 255)    # Arc Reactor Orange
        self.magenta = (255, 0, 255)   # HUD Accent
        self.blue = (255, 100, 0)      # Deep Blue
        
        # Tracking & Animation
        self.fingertip_trails = {i: deque(maxlen=20) for i in range(21)}
        self.frame_count = 0
        self.prev_time = time.time()
        
        # Holographic Object State
        self.box_pos = [640, 360] 
        self.box_size = 150
        self.is_dragging = False
        
        # Repulsor State
        self.charge_level = 0
        self.is_blasting = False
        self.blast_radius = 0
        
    def get_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def draw_hud_elements(self, frame):
        h, w = frame.shape[:2]
        
        # 1. Digital Grid
        grid_spacing = 60
        for y in range(0, h, grid_spacing):
            cv2.line(frame, (0, y), (w, y), self.cyan, 1)
        for x in range(0, w, grid_spacing):
            cv2.line(frame, (x, 0), (x, h), self.cyan, 1)
            
        # 2. Scanning Line
        scan_y = int(h * (self.frame_count % 100) / 100)
        cv2.line(frame, (0, scan_y), (w, scan_y), self.cyan, 1)
        
        # 3. Corner Brackets
        size = 40
        thickness = 2
        cv2.line(frame, (10, 10), (10 + size, 10), self.cyan, thickness) # TL
        cv2.line(frame, (10, 10), (10, 10 + size), self.cyan, thickness)
        cv2.line(frame, (w-10, 10), (w-10-size, 10), self.cyan, thickness) # TR
        cv2.line(frame, (w-10, 10), (w-10, 10 + size), self.cyan, thickness)
        
    def draw_holographic_box(self, frame):
        """Draws a floating 3D-effect wireframe box"""
        x, y = self.box_pos
        s = self.box_size
        color = self.magenta if self.is_dragging else self.cyan
        
        # Front square
        pts = np.array([[x-s//2, y-s//2], [x+s//2, y-s//2], [x+s//2, y+s//2], [x-s//2, y+s//2]], np.int32)
        cv2.polylines(frame, [pts], True, color, 2)
        
        # Back square (offset for 3D effect)
        offset = 30
        pts_back = pts + offset
        cv2.polylines(frame, [pts_back], True, color, 1)
        
        # Connect front to back
        for i in range(4):
            cv2.line(frame, tuple(pts[i]), tuple(pts_back[i]), color, 1)
            
        cv2.putText(frame, "TYPE: OBJ_ALPHA", (x-s//2, y-s//2-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    def draw_repulsor_blast(self, frame, cx, cy):
        """Iron Man Repulsor Blast Animation"""
        if self.charge_level > 0 and not self.is_blasting:
            # Charging Effect
            charge_radius = int(self.charge_level * 2)
            cv2.circle(frame, (cx, cy), charge_radius, (255, 255, 255), 2)
            cv2.circle(frame, (cx, cy), charge_radius + 5, self.cyan, 1)
            
            if self.charge_level > 25:
                # Shake effect simulation
                offset = np.random.randint(-5, 5, size=2)
                cv2.putText(frame, "MAX POWER - READY", (cx - 80 + offset[0], cy - 100 + offset[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.magenta, 2)

        if self.is_blasting:
            # Expansion wave
            self.blast_radius += 40
            alpha = max(0, 1 - self.blast_radius / 600)
            blast_color = tuple(int(c * alpha) for c in (255, 255, 255))
            
            # Draw multiple shockwaves
            for i in range(3):
                r = self.blast_radius - (i * 40)
                if r > 0:
                    cv2.circle(frame, (cx, cy), r, blast_color, 10 - i*2)
            
            # Flash at center
            flash_size = max(10, 100 - self.blast_radius // 2)
            if flash_size > 0:
                cv2.circle(frame, (cx, cy), flash_size, (255, 255, 255), -1)
            
            if self.blast_radius > 600:
                self.is_blasting = False
                self.blast_radius = 0

    def draw_hand_hologram(self, frame, hand_landmarks, handedness):
        h, w = frame.shape[:2]
        color = self.cyan if handedness == "Right" else self.orange
        
        # Get Key Points
        palm_center = hand_landmarks.landmark[9]
        cx, cy = int(palm_center.x * w), int(palm_center.y * h)
        
        # 1. Detect Gesture: OPEN PALM (Repulsor)
        # Check if all fingers are extended
        fingertips = [8, 12, 16, 20]
        finger_bases = [6, 10, 14, 18]
        is_open = all(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y for tip, base in zip(fingertips, finger_bases))
        
        if is_open:
            self.charge_level += 2
            if self.charge_level > 30:
                self.is_blasting = True
        else:
            self.charge_level = max(0, self.charge_level - 5)

        # 2. Detect Gesture: PINCH (Drag Box)
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        tx, ty = int(thumb.x * w), int(thumb.y * h)
        ix, iy = int(index.x * w), int(index.y * h)
        dist = self.get_distance((tx, ty), (ix, iy))
        
        is_pinching = dist < 40
        
        if is_pinching and not is_open:
            bx, by = self.box_pos
            if abs(ix - bx) < self.box_size//2 and abs(iy - by) < self.box_size//2:
                self.is_dragging = True
                self.box_pos = [ix, iy]
        else:
            self.is_dragging = False

        # 3. Draw Blast Effect
        self.draw_repulsor_blast(frame, cx, cy)

        # 4. Arc Reactor Style Circles
        if not self.is_blasting:
            for i in range(3):
                radius = 30 + i * 20
                rotation = (self.frame_count * (i + 1) * 2) % 360
                cv2.ellipse(frame, (cx, cy), (radius, radius), rotation, 0, 300, color, 1)
            
        # 5. Hexagonal Grid
        for i in range(6):
            angle = i * math.pi / 3 + (self.frame_count * 0.05)
            hx = int(cx + 80 * math.cos(angle))
            hy = int(cy + 80 * math.sin(angle))
            cv2.line(frame, (cx, cy), (hx, hy), color, 1)

        # 6. Connect Landmarks
        for connection in self.mp_hands.HAND_CONNECTIONS:
            start = hand_landmarks.landmark[connection[0]]
            end = hand_landmarks.landmark[connection[1]]
            pt1 = (int(start.x * w), int(start.y * h))
            pt2 = (int(end.x * w), int(end.y * h))
            cv2.line(frame, pt1, pt2, color, 2)
            
        # Highlight Interaction Points
        if is_pinching:
            cv2.circle(frame, (ix, iy), 15, self.magenta, 2)
            cv2.circle(frame, (ix, iy), 5, self.magenta, -1)

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("🚀 JARVIS Hologram System Initializing...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            self.frame_count += 1
            
            # HUD Overlay
            hud_overlay = frame.copy()
            self.draw_hud_elements(hud_overlay)
            self.draw_holographic_box(hud_overlay)
            
            # Hand Tracking
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    handedness = results.multi_handedness[i].classification[0].label
                    self.draw_hand_hologram(hud_overlay, hand_landmarks, handedness)
            
            # Final Blend
            result = cv2.addWeighted(frame, 0.3, hud_overlay, 0.7, 0)
            
            # Telemetry Data
            curr_time = time.time()
            fps = 1 / (curr_time - self.prev_time)
            self.prev_time = curr_time
            
            cv2.putText(result, f"SYSTEM: ONLINE | FPS: {int(fps)}", (w-400, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cyan, 2)
            cv2.putText(result, f"USER: TONY STARK", (40, h-40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.orange, 2)
            
            cv2.imshow('JARVIS Hologram v2.0', result)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hologram = TonyStarkHologram()
    hologram.run()
