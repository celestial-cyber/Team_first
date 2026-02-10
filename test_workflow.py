#!/usr/bin/env python
"""
Test workflow - demonstrates Scriptoria without requiring an actual video file
"""
import json
import os
from core.intent_engine import interpret_intent
from core.state_manager import save_state
from video_engine.frame_graph_api import build_frame_graph, traverse_frame_graph
from preproduction_engine.screenplay_generator import generate_screenplay
from preproduction_engine.workflow_planner import plan_workflow

DATA_FRAMES = "data/frames"
DATA_STATES = "data/states"

def create_synthetic_frames():
    """Create synthetic frames for testing"""
    os.makedirs(DATA_FRAMES, exist_ok=True)
    
    # Create 24 dummy frame files
    for i in range(24):
        frame_path = os.path.join(DATA_FRAMES, f"frame_{i:03d}.jpg")
        # Write a minimal JPEG header (a 1x1 gray image)
        with open(frame_path, 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
                   b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
                   b'\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a'
                   b'\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\''
                   b'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x11\x00\xff'
                   b'\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00'
                   b'\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t'
                   b'\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03'
                   b'\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05'
                   b'\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15'
                   b'R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86'
                   b'\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3'
                   b'\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9'
                   b'\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6'
                   b'\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1'
                   b'\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x08\x01\x01\x00'
                   b'\x00?\x00\xfb\xd4P\xff\xd9')
    
    print(f"[OK] Created {24} synthetic frames in {DATA_FRAMES}")

def main():
    print("=" * 60)
    print("SCRIPTORIA PROJECT WORKFLOW TEST")
    print("=" * 60)
    
    # Step 1: Create synthetic frames
    print("\n[STEP 1] Creating synthetic frames...")
    create_synthetic_frames()
    
    # Step 2: User input / Intent Understanding
    print("\n[STEP 2] Understanding intent...")
    user_input = "cinematic"
    intent = interpret_intent(user_input)
    print(f"  Input: '{user_input}'")
    print(f"  Intent: {json.dumps(intent, indent=4)}")
    
    # Step 3: Frame Graph Traversal
    print("\n[STEP 3] Building and traversing frame graph...")
    frames = build_frame_graph(DATA_FRAMES)
    print(f"  Total frames available: {len(frames)}")
    
    frame_path = traverse_frame_graph(frames, intent)
    print(f"  Selected frames ({len(frame_path)} frames): {frame_path[:5]}...")
    
    # Step 4: Preproduction Planning
    print("\n[STEP 4] Preproduction planning...")
    screenplay = generate_screenplay("A cinematic visual story")
    print(f"  Screenplay: {json.dumps(screenplay, indent=4)}")
    
    workflow = plan_workflow({"style": intent["style"], "pace": intent["pace"]})
    print(f"  Workflow: {json.dumps(workflow, indent=4)}")
    
    # Step 5: Save Creative State
    print("\n[STEP 5] Saving creative state...")
    state = {
        "intent": intent,
        "frame_count": len(frames),
        "selected_frames": len(frame_path),
        "fps": intent["fps"],
        "style": intent["style"],
        "screenplay": screenplay,
        "workflow": workflow
    }
    
    save_state(state, DATA_STATES, "demo_state.json")
    print(f"  State saved to: {os.path.join(DATA_STATES, 'demo_state.json')}")
    
    # Display results
    print("\n" + "=" * 60)
    print("PROJECT STRUCTURE VALIDATION")
    print("=" * 60)
    
    dirs = {
        "Frames": DATA_FRAMES,
        "States": DATA_STATES,
        "Outputs": "data/outputs",
        "Inputs": "data/input_videos"
    }
    
    for name, path in dirs.items():
        exists = os.path.exists(path)
        count = len(os.listdir(path)) if exists else 0
        status = "OK" if exists else "MISSING"
        print(f"  [{status}] {name:15} - {path:30} ({count} items)")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Scriptoria workflow completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Add a video to data/input_videos/input.mp4")
    print("  2. Run app.py for full video processing")
    print("  3. Check data/states/ for saved creative states")

if __name__ == "__main__":
    main()
