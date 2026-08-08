import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import cv2

from src.core.vision_worker import VisionWorker
from src.ui.overlay import Overlay
from src.ui.glass_panel import GlassPanel
from src.engine.ocr_engine import OCREngine

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        self.overlay = Overlay()
        self.panel = GlassPanel()
        
        # Connect Panel signals to Overlay
        self.panel.color_changed.connect(self.overlay.set_color)
        self.panel.thickness_changed.connect(self.overlay.set_thickness)
        self.panel.clear_requested.connect(self.overlay.clear_all)
        self.panel.undo_requested.connect(self.overlay.undo)
        self.panel.passthrough_toggled.connect(self.overlay.set_passthrough)
        
        # Start Vision Worker
        self.worker = VisionWorker()
        self.worker.gesture_event.connect(self.overlay.update_state)
        # We can also connect the debug frame to a small window or ignore it
        # self.worker.update_frame.connect(self.show_debug) 
        
        self.worker.start()
        
        # We won't eagerly load OCR to save startup time if not used immediately,
        # but the engine handles lazy loading of easyocr well.
        # self.ocr_engine = OCREngine()
        
        # Position panel in the top right
        screen_geometry = self.app.desktop().screenGeometry()
        self.panel.move(screen_geometry.width() - 350, 50)
        
        self.overlay.show()
        self.panel.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    # Initialize the OCR Engine here if we wanted background pre-loading
    app = MainApp()
    app.run()
