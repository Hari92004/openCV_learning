import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
import numpy as np

from src.core.config import Config
from src.core.gesture_tracker import GestureState
from src.core.smoothing import EMASmoother
from src.engine.geometry_engine import GeometryEngine

class Stroke:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness
        self.points = []
        self.shape_type = None
        self.shape_data = None
        self.text_data = None # For OCR text

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.smoother = EMASmoother()
        self.current_color = Config.COLORS[Config.DEFAULT_COLOR]
        self.current_thickness = Config.DEFAULT_THICKNESS
        
        self.strokes = []
        self.current_stroke = None
        
        self.pointer_pos = None
        self.current_state = GestureState.NONE
        self.is_erasing = False
        self.is_passthrough = False

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)
        
    def update_state(self, state, norm_coords):
        self.current_state = state
        if norm_coords is None:
            self.pointer_pos = None
            self.update()
            return

        raw_x = int(norm_coords[0] * self.width())
        raw_y = int(norm_coords[1] * self.height())
        
        smooth_x, smooth_y = self.smoother.update((raw_x, raw_y))
        self.pointer_pos = QPoint(smooth_x, smooth_y)
        
        self.is_erasing = False

        if state == GestureState.DRAW:
            if self.current_stroke is None:
                self.current_stroke = Stroke(self.current_color, self.current_thickness)
                self.strokes.append(self.current_stroke)
            self.current_stroke.points.append((smooth_x, smooth_y))
        
        elif state == GestureState.HOVER or state == GestureState.NONE:
            if self.current_stroke is not None:
                self._process_finished_stroke(self.current_stroke)
                self.current_stroke = None
            self.smoother.reset()

        elif state == GestureState.ERASE:
            self.is_erasing = True
            if self.current_stroke is not None:
                self.current_stroke = None
            self.smoother.reset()
            self._erase_at(smooth_x, smooth_y)
            
        self.update()

    def _process_finished_stroke(self, stroke):
        shape_type, shape_data = GeometryEngine.recognize_shape(stroke.points)
        if shape_type:
            stroke.shape_type = shape_type
            stroke.shape_data = shape_data

    def _erase_at(self, x, y):
        erase_radius = 50
        strokes_to_keep = []
        for stroke in self.strokes:
            keep = True
            for px, py in stroke.points:
                if (px - x)**2 + (py - y)**2 < erase_radius**2:
                    keep = False
                    break
            if keep:
                strokes_to_keep.append(stroke)
        self.strokes = strokes_to_keep

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for stroke in self.strokes:
            pen = QPen(QColor(*stroke.color), stroke.thickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            
            if stroke.text_data:
                # If we implement OCR replacement directly on canvas
                pass 
            elif stroke.shape_type == "LINE":
                pt1, pt2 = stroke.shape_data
                painter.drawLine(QPoint(*pt1), QPoint(*pt2))
            elif stroke.shape_type == "RECTANGLE":
                rx, ry, rw, rh = stroke.shape_data
                painter.drawRect(rx, ry, rw, rh)
            elif stroke.shape_type == "CIRCLE":
                center, radius = stroke.shape_data
                painter.drawEllipse(QPoint(*center), radius, radius)
            else:
                if len(stroke.points) > 1:
                    for i in range(1, len(stroke.points)):
                        p1 = QPoint(*stroke.points[i-1])
                        p2 = QPoint(*stroke.points[i])
                        painter.drawLine(p1, p2)
                elif len(stroke.points) == 1:
                    p = QPoint(*stroke.points[0])
                    painter.drawPoint(p)

        if self.pointer_pos and not self.is_passthrough:
            if self.current_state == GestureState.ERASE:
                painter.setPen(QPen(Qt.red, 2))
                painter.setBrush(QColor(255, 100, 100, 100))
                painter.drawEllipse(self.pointer_pos, 25, 25)
                painter.setPen(Qt.red)
                painter.setFont(QFont("Arial", 16, QFont.Bold))
                painter.drawText(self.pointer_pos + QPoint(35, 10), "ERASE")
            elif self.current_state == GestureState.HOVER:
                # Hover cursor (empty circle)
                painter.setPen(QPen(QColor(150, 150, 150, 200), 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(self.pointer_pos, self.current_thickness + 2, self.current_thickness + 2)
                painter.setPen(QColor(150, 150, 150))
                painter.setFont(QFont("Arial", 14, QFont.Bold))
                painter.drawText(self.pointer_pos + QPoint(20, 10), "HOVER")
            elif self.current_state == GestureState.DRAW:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(*self.current_color))
                painter.drawEllipse(self.pointer_pos, self.current_thickness + 2, self.current_thickness + 2)
                painter.setPen(QColor(*self.current_color))
                painter.setFont(QFont("Arial", 16, QFont.Bold))
                painter.drawText(self.pointer_pos + QPoint(20, 10), "DRAW")
            else:
                # NONE state (e.g. tracking lost or unrecognizable)
                painter.setPen(QColor(255, 255, 255, 100))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(self.pointer_pos + QPoint(20, 10), "?")

    def set_color(self, rgb):
        self.current_color = rgb
        
    def set_thickness(self, thick):
        self.current_thickness = thick
        
    def clear_all(self):
        self.strokes.clear()
        self.current_stroke = None
        self.update()
        
    def undo(self):
        if self.strokes:
            if self.current_stroke and self.strokes[-1] == self.current_stroke:
                self.current_stroke = None
            self.strokes.pop()
            self.update()
            
    def set_passthrough(self, is_pass):
        self.is_passthrough = is_pass
        if is_pass:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        else:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        # Needed for X11/Windows to register flag changes dynamically
        self.hide()
        self.show()
