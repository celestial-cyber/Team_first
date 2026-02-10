import json
import os
from extract_frames import extract_frames
from intent_api import interpret_intent
from frame_graph_api import build_frame_graph, traverse_frame_graph
from regenerate_api import regenerate_video

VIDEO_PATH = "input/input.mp4"
FRAME_DIR = "frames"
OUTPUT_VIDEO = "output/output.mp4"
STATE_DIR = "states"

os.makedirs(STATE_DIR, exist_ok=True)

# Step 1: Extract frames
extract_frames(VIDEO_PATH, FRAME_DIR)

# Step 2: User input
user_input = input("Describe the style you want (cinematic / fast / reel): ")

# Step 3: Intent Understanding
intent = interpret_intent(user_input)

# Step 4: Frame Graph Traversal
frames = build_frame_graph(FRAME_DIR)
frame_path = traverse_frame_graph(frames, intent)

# Step 5: Regenerate Video
regenerate_video(
    FRAME_DIR,
    frame_path,
    OUTPUT_VIDEO,
    intent["fps"]
)

# Step 6: Save Creative State
state = {
    "intent": intent,
    "frame_path_length": len(frame_path),
    "output_video": OUTPUT_VIDEO
}

with open(f"{STATE_DIR}/state_1.json", "w") as f:
    json.dump(state, f, indent=2)

print("[DONE] Creative state saved")
