"""
Object Detection & Tracking System using YOLOv8 and ByteTrack
Supports laptop camera or video file input
"""

import cv2
import time
import os
from ultralytics import YOLO

# Configuration
SOURCE = "data/sample2.mp4" 
# Use 0 for laptop camera, "data/sample1.mp4" for video

CONFIDENCE_THRESHOLD = 0.3
SAVE_OUTPUT = True

# Display settings
DISPLAY_WIDTH = 1500  # Display window width (HD 1920 width fits in 960 window)

# Create output directory
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_detections(frame, results):
    """Draw bounding boxes, labels, and tracking IDs on frame"""
    annotated_frame = frame.copy()

    # Get detection results
    if results and len(results) > 0:
        result = results[0]
        boxes = result.boxes

        # Check if boxes exist
        if boxes is None or len(boxes) == 0:
            return annotated_frame

        # Process each detection
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            # Get class name and confidence
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]

            # Get tracking ID (if available)
            track_id = None
            if box.id is not None:
                track_id = int(box.id[0])

            # Convert to integers
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Draw bounding box
            color = (0, 255, 0)  # Green
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

            # Create label text
            label = f"{class_name} {confidence:.1%}"
            if track_id is not None:
                label = f"ID:{track_id} {class_name} {confidence:.1%}"

            # Draw label background
            label_bg_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(annotated_frame, (x1, y1 - label_bg_size[1] - 10),
                        (x1 + label_bg_size[0], y1), color, -1)

            # Draw label text
            cv2.putText(annotated_frame, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return annotated_frame


def main():
    """Main function to run object detection and tracking"""

    # Load YOLO model
    print("Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")
    print("Model loaded successfully!")

    # Open video source
    print(f"Opening video source: {SOURCE}...")
    cap = cv2.VideoCapture(SOURCE)

    if not cap.isOpened():
        print("Error: Could not open video source!")
        return

    # Get video properties for resizing
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Video resolution: {frame_width}x{frame_height}")

    # Calculate display scale ratio
    scale_ratio = DISPLAY_WIDTH / frame_width if frame_width > DISPLAY_WIDTH else 1
    display_height = int(frame_height * scale_ratio)
    print(f"Display will be resized to: {DISPLAY_WIDTH}x{display_height}")

    print("Camera opened successfully!")

    # FPS calculation variables
    frame_count = 0
    start_time = time.time()
    fps = 0

    # Main loop
    print("Starting detection... Press 'Q' to quit, 'S' to save screenshot")

    while True:
        # Read frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame!")
            break

        # Run YOLO detection with tracking
        results = model.track(frame, persist=True, conf=CONFIDENCE_THRESHOLD, verbose=False)

        # Calculate FPS
        frame_count += 1
        elapsed = time.time() - start_time
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            start_time = time.time()

        # Draw detections on frame
        annotated_frame = draw_detections(frame, results)

        # Resize for display if needed
        if scale_ratio != 1:
            annotated_frame = cv2.resize(annotated_frame, (DISPLAY_WIDTH, display_height))

        # Add FPS counter
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display frame
        cv2.imshow("Object Detection & Tracking", annotated_frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("Quitting application...")
            break
        elif key == ord('s') or key == ord('S'):
            # Save screenshot
            screenshot_path = os.path.join(OUTPUT_DIR, f"screenshot_{int(time.time())}.jpg")
            cv2.imwrite(screenshot_path, annotated_frame)
            print(f"Screenshot saved: {screenshot_path}")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Application closed successfully!")


if __name__ == "__main__":
    main()