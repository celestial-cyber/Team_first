import os

def build_frame_graph(frame_dir):
    frames = sorted(os.listdir(frame_dir))
    return frames


def traverse_frame_graph(frames, intent):
    step = intent["step"]

    # MVP logic: intent-driven traversal
    selected_path = frames[::step]

    return selected_path
