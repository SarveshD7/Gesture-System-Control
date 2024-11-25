# Gesture-Controlled Applications

This project implements **Gesture Volume Control** and a **Virtual Mouse** using hand gestures, leveraging **OpenCV**, **Mediapipe**, and **autopy** for computer vision and interaction.

---
<img align="left" src="https://raw.githubusercontent.com/SarveshD7/Gesture-Volume-Control/main/HandLandmarks.png" alt="Sarvesh | C" width="1000px"/>
---
## Features

### 1. Gesture Volume Control
- Control system volume using hand gestures.
- Utilizes Mediapipe for hand tracking and `pycaw` for Windows audio integration.

### 2. Virtual Mouse
- Move the mouse pointer using hand gestures.
- Click actions triggered by specific gestures.
- Uses Mediapipe for hand tracking and `autopy` for controlling the system cursor.

---

## Requirements

- Python 3.7 or later
- **Windows OS** (for `pycaw` compatibility)

### Dependencies
Install the following Python libraries:
- `opencv-python`
- `mediapipe`
- `pycaw`
- `autopy`
- `numpy`

---

## How It Works

### Gesture Volume Control
1. **Hand Tracking**: Detects hand landmarks using Mediapipe.
2. **Gesture Recognition**: Calculates the distance between the thumb and index finger to adjust volume.
3. **Volume Adjustment**: Uses the `pycaw` library to set the system volume dynamically.

### Virtual Mouse
1. **Hand Tracking**: Detects hand landmarks using Mediapipe.
2. **Pointer Control**:
   - Moves the mouse pointer based on the index finger's position.
   - Smoothens movements to reduce jitter.
3. **Click Detection**:
   - Detects when both index and middle fingers are raised and close together to trigger a mouse click.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Gesture-Controlled-Applications.git
   cd Gesture-Controlled-Applications
2. Installations:
   ```bash
   pip install opencv-python mediapipe pycaw autopy numpy
3. Usage
   1. Volume Control
      ```bash
      python VolumeControl.py
   2. Virtual Mouse
      ```bash
      python VirtualMouse.py

