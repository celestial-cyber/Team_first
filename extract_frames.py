import cv2
import os

def extract_frames(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = os.path.join(output_dir, f"frame_{frame_id}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_id += 1

    cap.release()
    print(f"[INFO] Extracted {frame_id} frames")
