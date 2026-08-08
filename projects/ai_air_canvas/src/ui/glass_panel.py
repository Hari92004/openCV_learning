from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from src.core.config import Config

class GlassPanel(QWidget):
    color_changed = pyqtSignal(tuple)
    thickness_changed = pyqtSignal(int)
    clear_requested = pyqtSignal()
    undo_requested = pyqtSignal()
    passthrough_toggled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_passthrough = False
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Style the widget to look like glass
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 50);
                color: white;
                font-family: Arial;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                border-radius: 5px;
                padding: 5px;
                min-width: 80px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 60);
            }
        """)

        title = QLabel("AI Canvas Tools")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Colors
        color_layout = QHBoxLayout()
        for name, rgb in Config.COLORS.items():
            btn = QPushButton(name)
            # Set button color indicator
            btn.setStyleSheet(f"background-color: rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 150); font-weight: bold;")
            btn.clicked.connect(lambda checked, c=rgb: self.color_changed.emit(c))
            color_layout.addWidget(btn)
        layout.addLayout(color_layout)

        # Thickness
        thick_layout = QVBoxLayout()
        thick_label = QLabel("Thickness")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(Config.DEFAULT_THICKNESS)
        self.slider.valueChanged.connect(self.thickness_changed.emit)
        thick_layout.addWidget(thick_label)
        thick_layout.addWidget(self.slider)
        layout.addLayout(thick_layout)

        # Actions
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_requested.emit)
        undo_btn = QPushButton("Undo")
        undo_btn.clicked.connect(self.undo_requested.emit)
        btn_layout.addWidget(undo_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

        # Pass-through
        self.pass_btn = QPushButton("Mode: Draw")
        self.pass_btn.clicked.connect(self.toggle_passthrough)
        layout.addWidget(self.pass_btn)

        self.setLayout(layout)
        
        # Position window initially (will be moved by main app later if needed)
        self.resize(300, 250)

    def toggle_passthrough(self):
        self.is_passthrough = not self.is_passthrough
        if self.is_passthrough:
            self.pass_btn.setText("Mode: Mouse (Pass-Through)")
            self.pass_btn.setStyleSheet("background-color: rgba(255, 100, 100, 150);")
        else:
            self.pass_btn.setText("Mode: Draw")
            self.pass_btn.setStyleSheet("")
        self.passthrough_toggled.emit(self.is_passthrough)

    # Allow dragging the panel
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
