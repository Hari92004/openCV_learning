class Config:
    # Camera settings
    CAMERA_INDEX = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    FPS = 30
    
    # Tracking thresholds
    PINCH_THRESHOLD = 0.12  # Relaxed distance so drawing doesn't cut out easily while writing
    HAND_LOCK_DISTANCE_THRESHOLD = 0.5  # Max normalized distance to keep tracking the same hand
    
    # UI settings
    COLORS = {
        "Red": (255, 0, 0),
        "Blue": (0, 0, 255),
        "Green": (0, 255, 0),
        "White": (255, 255, 255)
    }
    DEFAULT_COLOR = "Blue"
    DEFAULT_THICKNESS = 5
    
    # Smoothing filter (EMA)
    EMA_ALPHA = 0.2  # Lower value = smoother lines (less jitter, more delay). Good for smooth handwriting.
