# OpenCV Learning & Computer Vision Projects 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Supported-orange.svg)](https://google.github.io/mediapipe/)

Welcome to the **OpenCV Learning Repository**! This repository serves as a comprehensive collection of Computer Vision concepts, practical OpenCV modules, object detection scripts, and feature-rich interactive AI applications.

---

## 🌟 Featured Highlights

### 💫 1. Sci-Fi Hologram & HUD Displays (`pros-2`)
Futuristic heads-up displays (HUDs) and holographic interaction modules powered by hand tracking and gesture recognition:
* **`tony_stark_hud.py`**: Iron Man-style HUD interface featuring interactive UI widgets and gesture-based controls.
* **`hologram_hand_gesture.py` & `hologram_v2.py`**: Interactive holographic projection simulations driven by MediaPipe hand coordinates.

---

### 📷 2. Core OpenCV Modules (`OpenCV/`)
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
├── pros-2/                         # Futuristic HUD & Hologram Experiments
│   ├── tony_stark_hud.py           # Interactive Tony Stark HUD interface
│   ├── hologram_hand_gesture.py    # Hand gesture hologram controller
│   ├── hologram_v2.py              # Advanced holographic display
│   └── test_mp.py                  # MediaPipe test script
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
   pip install opencv-python mediapipe numpy
   ```

---

## 🎯 How to Run

### Run Tony Stark HUD
```bash
python pros-2/tony_stark_hud.py
```

### Run Hologram Hand Gesture Control
```bash
python pros-2/hologram_hand_gesture.py
```

### Run Face & Feature Detection
```bash
python OpenCV/face_objectDetection--/face_eye_smile_detect.py
```

### Run Multi-Color Detection
```bash
python OpenCV/Projects---/multiColor.py
```

---

## 💻 Tech Stack

* **Language**: Python 3
* **Computer Vision**: OpenCV (`opencv-python`), MediaPipe
* **Numerical Processing**: NumPy

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a Pull Request.

---
