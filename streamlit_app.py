import os
import shutil
import json
import tempfile
import streamlit as st

from video_engine.extract_frames import extract_frames
from core.intent_engine import interpret_intent
from video_engine.frame_graph_api import build_frame_graph, traverse_frame_graph
from video_engine.regenerate_api import regenerate_video


DATA_INPUT = os.path.join("data", "input_videos")
DATA_FRAMES = os.path.join("data", "frames")
DATA_OUTPUTS = os.path.join("data", "outputs")
DATA_STATES = os.path.join("data", "states")

os.makedirs(DATA_INPUT, exist_ok=True)
os.makedirs(DATA_FRAMES, exist_ok=True)
os.makedirs(DATA_OUTPUTS, exist_ok=True)
os.makedirs(DATA_STATES, exist_ok=True)


st.set_page_config(page_title="Scriptoria — Video Remix", layout="centered")

st.title("Scriptoria — Interactive Video Remix")
st.markdown("Upload a short video, describe the style, and generate a remixed output.")

uploaded = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"]) 
style_text = st.text_input("Describe the style (e.g. 'cinematic, dramatic, 15fps, 30s')", "cinematic")
fps_input = st.number_input("Optional FPS (leave 0 to use intent default)", min_value=0, max_value=60, value=0)

if uploaded:
    st.info(f"Selected: {uploaded.name} ({uploaded.size} bytes)")

if st.button("Generate Video"):
    if not uploaded:
        st.error("Please upload a video first.")
    else:
        with st.spinner("Saving and extracting frames..."):
            # Save uploaded file to data input
            input_path = os.path.join(DATA_INPUT, uploaded.name)
            with open(input_path, "wb") as f:
                shutil.copyfileobj(uploaded, f)

            # Clear previous frames
            try:
                shutil.rmtree(DATA_FRAMES)
            except Exception:
                pass
            os.makedirs(DATA_FRAMES, exist_ok=True)

            extract_frames(input_path, DATA_FRAMES)

        st.success("Frames extracted.")

        st.info("Interpreting intent...")
        intent = interpret_intent(style_text)
        if fps_input and fps_input > 0:
            intent["fps"] = int(fps_input)

        st.write("**Interpreted intent**")
        st.json(intent)

        st.info("Building frame graph and selecting frames...")
        frames = build_frame_graph(DATA_FRAMES)
        frame_path = traverse_frame_graph(frames, intent)

        if not frame_path:
            st.error("No frames selected by traversal algorithm.")
        else:
            st.success(f"Selected {len(frame_path)} frames.")

            output_name = f"output_streamlit.mp4"
            output_path = os.path.join(DATA_OUTPUTS, output_name)

            with st.spinner("Regenerating video (this may take a moment)..."):
                regenerate_video(DATA_FRAMES, frame_path, output_path, intent)

            st.success("Video generated!")
            st.video(output_path)

            # Save state
            state = {"intent": intent, "frame_path_length": len(frame_path), "output_video": output_path}
            state_file = os.path.join(DATA_STATES, "state_streamlit.json")
            with open(state_file, "w") as sf:
                json.dump(state, sf, indent=2)

            st.write("Saved state")
            st.json(state)

st.markdown("---")
st.caption("Tip: try 'cinematic', 'trailer fast 15fps', or 'reel 10s' in the style box.")
