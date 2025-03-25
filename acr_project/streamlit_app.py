import streamlit as st
import os
import json
import tempfile
from utils import extract_frame_hashes_with_timestamps
from imagehash import phash
from moviepy.editor import VideoFileClip

FINGERPRINT_FILE = "fingerprints.json"
DB_FOLDER = "video_db"
THRESHOLD = 10

@st.cache_data
def load_fingerprints():
    with open(FINGERPRINT_FILE, "r") as f:
        return json.load(f)

def find_longest_contiguous_segment(timestamps):
    if not timestamps:
        return None
    timestamps = sorted(timestamps)
    segments = []
    start = timestamps[0]
    prev = start

    for ts in timestamps[1:]:
        if ts - prev > 1.5:
            segments.append((start, prev + 1))
            start = ts
        prev = ts
    segments.append((start, prev + 1))
    longest = max(segments, key=lambda x: x[1] - x[0])
    return longest

def match_query_clip(query_path, db_fingerprints, threshold=THRESHOLD):
    query_hashes = extract_frame_hashes_with_timestamps(query_path)
    scores = {}
    match_times = {}

    for video, db_frames in db_fingerprints.items():
        db_hashes = [(phash.hex_to_hash(f["hash"]), f["timestamp"]) for f in db_frames]
        score = 0
        matched_ts = []

        for q in query_hashes:
            qh = phash.hex_to_hash(q["hash"])
            for dbh, ts in db_hashes:
                if qh - dbh < threshold:
                    matched_ts.append(ts)
                    score += 1
                    break

        scores[video] = score
        match_times[video] = matched_ts

    best_video = max(scores, key=scores.get)
    segment = find_longest_contiguous_segment(match_times[best_video])
    return best_video, scores[best_video], segment, scores

def extract_segment(video_path, start, end):
    clip = VideoFileClip(video_path).subclip(start, end)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    clip.write_videofile(tmp_file.name, codec="libx264", audio=False, verbose=False, logger=None)
    return tmp_file.name

# Streamlit UI
st.title("🎬 ACR – Video Matching with Timestamp Preview")
st.markdown("Upload a short video clip and find out which known video it matches, including a preview of the matching segment.")

uploaded_file = st.file_uploader("Upload a query video", type=["mp4", "mov", "mkv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.video(temp_path)
    st.info("Analyzing...")

    fingerprints = load_fingerprints()
    best_video, score, segment, all_scores = match_query_clip(temp_path, fingerprints)

    st.success(f"✅ Match: **{best_video}** with score **{score}**")
    if segment:
        st.info(f"🕒 Matching segment: **{segment[0]}s → {segment[1]}s**")

        db_video_path = os.path.join(DB_FOLDER, best_video)
        if os.path.exists(db_video_path):
            preview_path = extract_segment(db_video_path, segment[0], segment[1])
            st.video(preview_path)
            os.remove(preview_path)

    st.subheader("📊 All Scores")
    st.json(all_scores)

    os.remove(temp_path)
