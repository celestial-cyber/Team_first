from .extract_frames import extract_frames
from .frame_graph_api import build_frame_graph, traverse_frame_graph
from .regenerate_api import regenerate_video

def orchestrate(video_path, data_dirs, user_input):
    frames_dir = data_dirs.get("frames")
    outputs_dir = data_dirs.get("outputs")

    extract_frames(video_path, frames_dir)
    frames = build_frame_graph(frames_dir)
    # interpret intent is external; user_input expected to be processed already
    # this is a small helper for higher-level controllers
    return frames
