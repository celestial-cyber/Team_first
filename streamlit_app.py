import os
import shutil
import json
import tempfile
import streamlit as st

from video_engine.extract_frames import extract_frames
from core.intent_engine import interpret_intent
from video_engine.frame_graph_api import build_frame_graph, traverse_frame_graph
from video_engine.regenerate_api import regenerate_video
from preproduction_engine.preprod_controller import run_preproduction


DATA_INPUT = os.path.join("data", "input_videos")
DATA_FRAMES = os.path.join("data", "frames")
DATA_OUTPUTS = os.path.join("data", "outputs")
DATA_STATES = os.path.join("data", "states")

os.makedirs(DATA_INPUT, exist_ok=True)
os.makedirs(DATA_FRAMES, exist_ok=True)
os.makedirs(DATA_OUTPUTS, exist_ok=True)
os.makedirs(DATA_STATES, exist_ok=True)


# Set page config with custom theme
st.set_page_config(page_title="Scriptoria — Video Remix", layout="wide")

# Modern gradient + blur background CSS
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        backdrop-filter: blur(10px);
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.5);
    }
    h1, h2, h3 {
        color: #333;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ Scriptoria — Interactive Video Remix")
st.markdown("Upload a short video, describe the style, and generate a beautifully remixed output with AI-enhanced preproduction planning.")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded = st.file_uploader("📹 Upload a video file", type=["mp4", "mov", "avi"])
    style_text = st.text_input("📝 Describe the style (e.g. 'cinematic, dramatic, 15fps, 30s')", "cinematic")

with col2:
    st.subheader("⚙️ Options")
    use_llm = st.toggle("🤖 Use LLM intent parsing", value=False, help="Send style to remote LLM API if configured")
    fps_input = st.number_input("FPS (0 = auto)", min_value=0, max_value=60, value=0)

if uploaded:
    st.info(f"✅ Selected: {uploaded.name} ({uploaded.size / 1e6:.1f} MB)")

if st.button("🎬 Generate Video & Preproduction", use_container_width=True):
    if not uploaded:
        st.error("Please upload a video first.")
    else:
        with st.spinner("🎞️ Saving and extracting frames..."):
            # Save uploaded file
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

        st.success("✅ Frames extracted.")

        st.info("🧠 Interpreting your vision...")
        intent = interpret_intent(style_text, use_llm=use_llm)
        if fps_input and fps_input > 0:
            intent["fps"] = int(fps_input)

        # Show intent interpretation
        with st.expander("📊 Interpreted Intent", expanded=False):
            st.json(intent)

        # Run preproduction
        st.info("🎬 Running preproduction planning...")
        preprod_result = run_preproduction(style_text, intent)

        # Display preproduction outputs in tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Screenplay", "Workflow", "Characters", "Sound Design", "Video"])

        with tab1:
            st.subheader("📖 Screenplay")
            st.write(f"**Title:** {preprod_result['screenplay']['title']}")
            for scene in preprod_result['screenplay']['scenes']:
                st.write(f"**Scene {scene['id']}:** {scene['description']} (~{scene['rough_duration_s']}s)")

        with tab2:
            st.subheader("📋 Production Workflow")
            wf = preprod_result['workflow']
            st.write(f"**Style:** {wf['style']} | **Pace:** {wf['pace']}")
            for step in wf['steps']:
                priority_color = "🔴" if step['priority'] == "high" else "🟡" if step['priority'] == "medium" else "🟢"
                st.write(f"{priority_color} **Phase {step['phase']}: {step['name']}** — {step['notes']}")

        with tab3:
            st.subheader("🎭 Characters & Subjects")
            chars = preprod_result['characters']
            st.write(f"**Primary Mood:** {chars['primary_mood']} | **Count:** {chars['count']}")
            for ch in chars['characters']:
                st.write(f"- **{ch['role']}** ({ch['screen_time_pct']}% screen time) | Lighting: {ch['lighting']}")

        with tab4:
            st.subheader("🎵 Sound Design Plan")
            sound = preprod_result['sound_design']
            st.write(f"**Style:** {sound['style']} | **Tracks:** {sound['track_count']} | **Narration:** {'Yes ✓' if sound['has_narration'] else 'No'}")
            for track in sound['tracks']:
                st.write(f"- **{track['name']}** | Type: {track['type']} | Volume: {track['volume_db']}dB")

        with tab5:
            st.info("🎥 Generating video (this may take a moment)...")
            
            st.info("🔗 Building frame graph and selecting frames...")
            frames = build_frame_graph(DATA_FRAMES)
            frame_path = traverse_frame_graph(frames, intent)

            if not frame_path:
                st.error("❌ No frames selected by traversal algorithm.")
            else:
                st.success(f"✅ Selected {len(frame_path)} frames from {len(frames)} total.")

                output_name = f"output_streamlit.mp4"
                output_path = os.path.join(DATA_OUTPUTS, output_name)

                with st.spinner("🎬 Assembling video..."):
                    regenerate_video(DATA_FRAMES, frame_path, output_path, intent)

                st.success("✅ Video generated!")
                st.video(output_path)

                # Save state
                state = {"intent": intent, "frame_path_length": len(frame_path), "output_video": output_path, "preprod": preprod_result}
                state_file = os.path.join(DATA_STATES, "state_streamlit.json")
                with open(state_file, "w") as sf:
                    json.dump(state, sf, indent=2, default=str)

                st.write("💾 Saved creative state")

st.markdown("---")
st.caption("💡 **Tips:** Try 'cinematic dramatic', 'trailer energetic 15fps', or 'reel vibrant 10s'. Enable LLM mode for smarter parsing with your configured API.")
