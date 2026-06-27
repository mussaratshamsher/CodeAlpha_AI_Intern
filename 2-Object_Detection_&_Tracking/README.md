# Object Detection & Tracking System

A real-time object detection and tracking application using YOLOv8 and ByteTrack.

## Features

- **Real-time Video Capture** - Uses laptop camera or video file input
- **Object Detection** - YOLOv8 model (yolov8n.pt)
- **Object Tracking** - ByteTrack for consistent tracking IDs
- **Bounding Boxes** - Visual detection boxes
- **Object Labels** - Class names with confidence scores
- **Tracking IDs** - Persistent IDs across frames
- **FPS Counter** - Real-time performance display
- **Screenshot** - Save frames with 'S' key

## Tech Stack

- **Python** 3.8+
- **ultralytics** - YOLO model
- **opencv-python** - Video capture and visualization
- **numpy** - Numerical operations

## Project Structure

```
2-Object_Detection_&_Tracking/
├── main.py           # Main application
├── requirements.txt  # Dependencies
├── README.md         # This file
├── plan.md          # Development plan
├── outputs/         # Saved screenshots
└── videos/         # Video files (optional)
```

## Installation

1. **Create virtual environment** (optional but recommended):

```bash
python -m venv .venv
```

2. **Activate virtual environment**:

- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install ultralytics opencv-python numpy
```

## Running the Application

### Basic Usage (Laptop Camera):

```bash
python main.py
```

### Using a Video File:

Edit `main.py` and change:

```python
SOURCE = 0  # Use 0 for camera
```

To:

```python
SOURCE = "data/sample1.mp4"  # Or your video file path
```

Then run:

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `Q` | Quit application |
| `S` | Save screenshot to `outputs/` folder |

## Output

When you press `S`, screenshots are saved to the `outputs/` folder with timestamp:
```
outputs/screenshot_1234567890.jpg
```

## Detected Objects

The YOLOv8 model can detect 80+ object classes including:

- Person
- Bottle
- Cup
- Chair
- Laptop
- Cell Phone
- Book
- Remote
- Keyboard
- Mouse
- and more...

## Testing Checklist

- [x] Camera opens successfully
- [x] Video file input works
- [x] YOLO detects objects
- [x] Bounding boxes displayed
- [x] Labels displayed
- [x] Tracking IDs displayed
- [x] FPS displayed
- [x] Real-time tracking works
- [x] Pressing Q exits application
- [x] Code runs from a single main.py file

## Troubleshooting

### Camera Not Opening

- Check if camera is enabled in BIOS
- Ensure no other application is using the camera
- Try different camera index: change `SOURCE = 0` to `SOURCE = 1`

### Poor FPS

- Use yolov8n.pt (nano) for best performance
- Close other running applications
- Reduce video resolution if needed

### Model Download Error

The model (yolov8n.pt) downloads automatically on first run. If it fails:
1. Download manually from: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8n.pt
2. Place it in the project folder

### No Detections

- Ensure adequate lighting
- Check conf threshold in code (default: 0.3)
- Hold objects closer to camera

## Code Overview

### Key Configuration Variables

```python
SOURCE = 0              # 0 = camera, "video.mp4" = video file
CONFIDENCE_THRESHOLD = 0.3  # Detection confidence (0.0-1.0)
SAVE_OUTPUT = True      # Enable output saving
```

### Main Functions

- `main()` - Entry point, runs the detection loop
- `draw_detections()` - Draws boxes, labels, and tracking IDs

## License

This project is for educational purposes.

## Author

CodeAlpha AI Intern Task