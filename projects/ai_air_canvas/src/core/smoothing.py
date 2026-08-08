from src.core.config import Config

class EMASmoother:
    def __init__(self, alpha=Config.EMA_ALPHA):
        self.alpha = alpha
        self.prev_point = None

    def update(self, current_point):
        """
        Applies Exponential Moving Average to the current point.
        current_point: tuple (x, y)
        Returns smoothed tuple (x, y)
        """
        if self.prev_point is None:
            self.prev_point = current_point
            return current_point

        smoothed_x = int(self.alpha * current_point[0] + (1 - self.alpha) * self.prev_point[0])
        smoothed_y = int(self.alpha * current_point[1] + (1 - self.alpha) * self.prev_point[1])
        
        smoothed_point = (smoothed_x, smoothed_y)
        self.prev_point = smoothed_point
        return smoothed_point

    def reset(self):
        """Reset the smoother when drawing starts/stops to avoid jumping."""
        self.prev_point = None
