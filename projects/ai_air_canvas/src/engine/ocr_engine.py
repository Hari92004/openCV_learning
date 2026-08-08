class OCREngine:
    def __init__(self):
        self.reader = None
        try:
            import easyocr
            # Initialize easyocr reader for English. 
            # Downloads models to ~/.EasyOCR/model on first run.
            self.reader = easyocr.Reader(['en'], gpu=False) 
        except Exception as e:
            print(f"Warning: OCR engine failed to initialize (PyTorch DLL error is common on Windows). OCR features will be disabled. Error: {e}")

    def recognize_text(self, image_np):
        """
        Takes a numpy array representing the drawing buffer.
        Returns a list of tuples: (bounding_box, text, confidence).
        Bounding box format: [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        """
        if self.reader is None or image_np is None or image_np.size == 0:
            return []
            
        # readtext accepts numpy arrays
        results = self.reader.readtext(image_np)
        
        # Filter low confidence results
        filtered_results = [res for res in results if res[2] > 0.5]
        return filtered_results
