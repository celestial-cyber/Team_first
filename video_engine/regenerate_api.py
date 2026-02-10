from moviepy.editor import ImageSequenceClip
import os

def regenerate_video(frame_dir, frame_path, output_path, fps):
    images = [os.path.join(frame_dir, f) for f in frame_path]

    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_path, codec="libx264")

    print(f"[INFO] Video regenerated at {output_path}")
