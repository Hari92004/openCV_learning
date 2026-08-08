import math
from src.core.config import Config

class GestureState:
    HOVER = "HOVER"
    DRAW = "DRAW"
    ERASE = "ERASE"
    NONE = "NONE"

class GestureTracker:
    def __init__(self):
        self.primary_hand_center = None
        self.last_state = GestureState.NONE

    def process_hands(self, hand_landmarks_list):
        """
        Takes MediaPipe hand landmarks and returns (state, pointer_coords)
        pointer_coords are normalized [0, 1]
        """
        if not hand_landmarks_list:
            self.primary_hand_center = None
            self.last_state = GestureState.NONE
            return GestureState.NONE, None

        # Primary Hand Lock
        best_hand = None
        min_dist = float('inf')

        for hand_lms in hand_landmarks_list:
            # Calculate center (using wrist as proxy for center)
            center_x = hand_lms.landmark[0].x
            center_y = hand_lms.landmark[0].y
            center = (center_x, center_y)

            if self.primary_hand_center is None:
                # No primary hand, lock onto this one
                best_hand = hand_lms
                self.primary_hand_center = center
                break
            else:
                dist = math.hypot(center[0] - self.primary_hand_center[0], center[1] - self.primary_hand_center[1])
                if dist < min_dist and dist < Config.HAND_LOCK_DISTANCE_THRESHOLD:
                    min_dist = dist
                    best_hand = hand_lms
                    self.primary_hand_center = center

        if best_hand is None:
            # Lost primary hand, reset or use the first one if preferred.
            # For now, just take the first one to acquire a new hand immediately
            best_hand = hand_landmarks_list[0]
            self.primary_hand_center = (best_hand.landmark[0].x, best_hand.landmark[0].y)

        # Calculate states based on best_hand
        return self._detect_gesture(best_hand)

    def _detect_gesture(self, hand_landmarks):
        # Landmarks:
        # 4: Thumb tip, 8: Index tip, 12: Middle tip, 16: Ring tip, 20: Pinky tip
        # 3: Thumb IP, 7: Index DIP, 11: Middle DIP, 15: Ring DIP, 19: Pinky DIP
        
        tips = [8, 12, 16, 20]
        dips = [7, 11, 15, 19]

        fingers_up = []
        for tip, dip in zip(tips, dips):
            # Y goes down in image coordinates, so smaller Y means UP
            fingers_up.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y)

        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        
        pinch_dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
        
        # Pointer coords (midpoint of pinch, or just index tip)
        pointer_x = index_tip.x
        pointer_y = index_tip.y
        pointer_coords = (pointer_x, pointer_y)

        # 1. Erase: Open Palm (all 4 fingers up)
        if all(fingers_up):
            self.last_state = GestureState.ERASE
            return GestureState.ERASE, pointer_coords

        # 2. Draw: Index and Thumb pinched
        if pinch_dist < Config.PINCH_THRESHOLD and fingers_up[0]:
            self.last_state = GestureState.DRAW
            return GestureState.DRAW, pointer_coords

        # 3. Hover: Index up, middle/ring/pinky down, no pinch
        if fingers_up[0] and not fingers_up[1] and not fingers_up[2] and not fingers_up[3]:
            self.last_state = GestureState.HOVER
            return GestureState.HOVER, pointer_coords

        self.last_state = GestureState.NONE
        return GestureState.NONE, pointer_coords
