# OpenCV Learning & Computer Vision Projects 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Supported-orange.svg)](https://google.github.io/mediapipe/)
[![PyQt5](https://img.shields.io/badge/PyQt-5-purple.svg)](https://www.riverbankcomputing.com/software/pyqt/)

Welcome to the **OpenCV Learning Repository**! This repository serves as a comprehensive collection of Computer Vision concepts, practical OpenCV modules, object detection scripts, and feature-rich interactive AI applications.

---

## 🌟 Featured Projects

### 🎨 1. AI Air Canvas (`projects/ai_air_canvas`)
An interactive, real-time virtual drawing canvas driven by hand-gesture recognition and a sleek UI overlay.
* **Hand Tracking**: Real-time hand landmark detection using MediaPipe.
* **Futuristic Glassmorphism UI**: Built with PyQt5 transparent overlays for color picking, brush size adjustments, undo, and canvas clearing.
* **Geometric & OCR Engines**: Shape recognition and text extraction capabilities integrated into the drawing stream.

---

### 💫 2. Sci-Fi Hologram & HUD Displays (`pros-2`)
Futuristic heads-up displays (HUDs) and holographic interaction modules powered by gesture tracking:
* **`tony_stark_hud.py`**: Iron Man-style HUD interface featuring interactive UI widgets and gesture control.
* **`hologram_hand_gesture.py` & `hologram_v2.py`**: Holographic projection simulations controlled by hand coordinates.

---

### 📷 3. Core OpenCV Modules (`OpenCV/`)
Structured practice modules covering fundamental to advanced Computer Vision concepts:
* **Image Processing**: Image reading, resizing, cropping, color space conversions, rotation, and drawing primitives.
* **Filtering & Thresholding**: Gaussian Blur, Median Blur, Sharpening, Canny Edge Detection, and Adaptive Thresholding.
* **Contour & Bitwise Operations**: Contour extraction, area analysis, and bitwise mask operations.
* **Face & Feature Detection**: Face, eye, smile, body, and license plate detection using Haar Cascade classifiers (`.xml`).
* **Color Detection**: Real-time accurate single and multi-color detection scripts.
* **Video Functions**: Video capture, frame processing, and video writer pipelines.

---

## 📂 Repository Structure

```
OpenCV/
├── projects/
│   └── ai_air_canvas/              # AI Air Canvas Application
│       ├── main.py                 # Main entry point for PyQt5 + MediaPipe Air Canvas
│       ├── requirements.txt        # Dependencies for AI Air Canvas
│       └── src/
│           ├── core/               # Vision worker, gesture tracker & smoothing logic
│           ├── engine/             # Geometry recognition & OCR engines
│           └── ui/                 # Glasspanel UI and transparent overlay screens
│
├── pros-2/                         # Futuristic HUD & Hologram Experiments
│   ├── tony_stark_hud.py           # Interactive Tony Stark HUD interface
│   ├── hologram_hand_gesture.py    # Hand gesture hologram controller
│   └── hologram_v2.py              # Advanced holographic display
│
├── OpenCV/                         # Core OpenCV Tutorials & Modules
│   ├── imageProcessing---/         # Basic image operations (crop, rotate, colors, shapes)
│   ├── image processing2----/      # Advanced image ops (blur, Canny, contours, bitwise)
│   ├── face_objectDetection--/     # Face/Eye/Smile detection & Haar cascades
│   ├── videoFunction--/            # Video recording & webcam streaming
│   ├── Projects---/                # Color detection & multi-color tracking
│   ├── creative---/                # Creative image processing scripts
│   └── assignments--/              # Practice tasks & assignment scripts
│
└── .gitignore                      # Ignored virtual environments, cache, and IDE files
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8 or higher installed.

```bash
python --version
```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hari92004/openCV_learning.git
   cd openCV_learning
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r projects/ai_air_canvas/requirements.txt
   ```

---

## 🎯 How to Run

### Run AI Air Canvas
```bash
python projects/ai_air_canvas/main.py
```

### Run Tony Stark HUD
```bash
python pros-2/tony_stark_hud.py
```

### Run Face & Feature Detection
```bash
python OpenCV/face_objectDetection--/face_eye_smile_detect.py
```

---

## 💻 Tech Stack

* **Language**: Python 3
* **Computer Vision**: OpenCV (`opencv-python`), MediaPipe
* **GUI / UI Framework**: PyQt5
* **Numerical Processing**: NumPy
* **OCR**: EasyOCR

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.