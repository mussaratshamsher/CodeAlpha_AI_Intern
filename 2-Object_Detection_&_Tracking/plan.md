# Object Detection & Tracking System (Laptop Camera Version)

## Project Overview

Build a simple Python application that uses the **laptop's built-in camera** (or a video file) to perform:

- Real-time video capture using OpenCV
- Object detection using YOLOv8
- Object tracking using ByteTrack
- Bounding box visualization
- Object labels
- Tracking IDs
- Real-time display

This project is designed specifically to satisfy the assignment requirements while keeping the codebase simple and easy to understand.

---

# Assignment Requirements Mapping

| Requirement | Solution |
|------------|-----------|
| Real-time video input | OpenCV + Laptop Camera |
| Object Detection | YOLOv8 |
| Bounding Boxes | OpenCV Drawing |
| Object Tracking | ByteTrack |
| Tracking IDs | ByteTrack |
| Real-time Display | OpenCV Window |

---

# Technology Stack

## Python Libraries

- ultralytics
- opencv-python
- numpy

---

# Simple Project Structure

```text
object-tracking/

├── main.py
├── requirements.txt
├── README.md
│
├── outputs/
│   └── processed_video.mp4
│
└── videos/
    └── sample.mp4
```

Only one Python file is required.

No complex architecture.

No unnecessary folders.

---

# Development Phases

---

# Phase 1 — Environment Setup

## Create Project Folder

```text
object-tracking/
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux/Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install ultralytics
pip install opencv-python
pip install numpy
```

Generate requirements:

```bash
pip freeze > requirements.txt
```

---

# Phase 2 — Camera Setup

## Objective

Access laptop camera.

OpenCV camera index:

```python
cv2.VideoCapture(0)
```

Usually:

```text
0 = Laptop Camera
```

Verify:

- Camera opens
- Frames are received
- Window displays live feed

---

# Phase 3 — YOLO Object Detection

## Model

Use:

```text
yolov8n.pt
```

Reason:

- Fast
- Lightweight
- Free
- Works on CPU

Load model:

```python
model = YOLO("yolov8n.pt")
```

Detect:

```python
results = model(frame)
```

Expected detections:

```text
Person
Bottle
Chair
Laptop
Cell Phone
Book
Cup
```

---

# Phase 4 — Object Tracking

## Tracker

Use:

```text
ByteTrack
```

Built into Ultralytics.

No additional packages required.

Tracking:

```python
model.track()
```

Enable:

```python
persist=True
```

This allows:

```text
Person → ID 1
Bottle → ID 2
```

Tracking IDs remain consistent between frames.

---

# Phase 5 — Visualization

Display:

### Bounding Boxes

```text
┌─────────────┐
│ Person      │
└─────────────┘
```

### Labels

```text
Person
Bottle
Laptop
```

### Confidence

```text
Person 95%
```

### Tracking ID

```text
Person ID:1
```

---

# Phase 6 — FPS Counter

Display:

```text
FPS: 24
```

Purpose:

Measure real-time performance.

---

# Phase 7 — Main Processing Pipeline

Workflow:

```text
Laptop Camera
      ↓
Read Frame
      ↓
YOLO Detection
      ↓
ByteTrack Tracking
      ↓
Draw Labels
      ↓
Display Window
```

---

# Phase 8 — Keyboard Controls

## Quit Application

```text
Q
```

---

## Save Screenshot

```text
S
```

Store image:

```text
outputs/
```

---

# Phase 9 — Video File Support

The application should support:

### Laptop Camera

```python
cv2.VideoCapture(0)
```

### Video File

```python
cv2.VideoCapture("videos/sample.mp4")
```

Switch source using a variable:

```python
SOURCE = 0
```

or

```python
SOURCE = "videos/sample.mp4"
```

---

# Testing Checklist

## Test 1

Application starts.

Expected:

```text
Camera Opened Successfully
```

---

## Test 2

Live video visible.

Expected:

```text
Real-time feed displayed
```

---

## Test 3

Object detected.

Show:

```text
Person
Bottle
Laptop
```

---

## Test 4

Tracking IDs visible.

Expected:

```text
Person ID:1
Bottle ID:2
```

---

## Test 5

Move object.

Expected:

```text
Same ID remains attached
```

Example:

```text
Frame 1:
Person ID:1

Frame 50:
Person ID:1
```

---

## Test 6

FPS visible.

Expected:

```text
FPS: 20+
```

---

## Test 7

Press Q.

Expected:

```text
Application closes cleanly
```

---

# Deliverables

## Source Code

```text
main.py
```

---

## Dependency File

```text
requirements.txt
```

---

## Documentation

```text
README.md
```

---

## Sample Output

Screenshot showing:

- Bounding boxes
- Labels
- Tracking IDs
- FPS

---

# Final Success Criteria

The assignment is complete when:

- [ ] Laptop camera opens successfully
- [ ] Video file input works
- [ ] YOLO detects objects
- [ ] Bounding boxes displayed
- [ ] Labels displayed
- [ ] Tracking IDs displayed
- [ ] FPS displayed
- [ ] Real-time tracking works
- [ ] Pressing Q exits application
- [ ] Code runs from a single main.py file

This structure keeps the project extremely simple, beginner-friendly, and fully aligned with the assignment requirements while remaining easy to extend later into a FastAPI + Next.js portfolio project.