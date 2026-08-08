import cv2
import mediapipe as mp
import time
from PyQt5.QtCore import QThread, pyqtSignal
from src.core.config import Config
from src.core.gesture_tracker import GestureTracker, GestureState

class VisionWorker(QThread):
    # Signals to communicate with the GUI thread
    update_frame = pyqtSignal(object)  # Sends the debug frame (BGR numpy array)
    gesture_event = pyqtSignal(str, object) # Sends state (str) and coords (tuple of normalized x, y)

    def __init__(self):
        super().__init__()
        self.running = True
        self.gesture_tracker = GestureTracker()
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def run(self):
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        cap.set(3, Config.CAMERA_WIDTH)
        cap.set(4, Config.CAMERA_HEIGHT)

        while self.running:
            success, img = cap.read()
            if not success:
                time.sleep(0.1)
                continue

            # Flip the image horizontally for a selfie-view display
            img = cv2.flip(img, 1)
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)

            state = GestureState.NONE
            coords = None

            if results.multi_hand_landmarks:
                # Draw landmarks for debug frame
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                state, coords = self.gesture_tracker.process_hands(results.multi_hand_landmarks)
            else:
                self.gesture_tracker.process_hands(None) # Reset tracking if no hands

            self.gesture_event.emit(state, coords)
            self.update_frame.emit(img)
            
            # Sleep slightly to prevent 100% CPU usage
            time.sleep(1 / Config.FPS)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()
