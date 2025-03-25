import streamlit as st
import os
import json
from utils import extract_frame_hashes
from imagehash import phash
import tempfile

FINGERPRINT_FILE = "fingerprints.json"
THRESHOLD = 10

@st.cache_data
def load_fingerprints():
    with open(FINGERPRINT_FILE, "r") as f:
        return json.load(f)

def match_query_clip(query_path, db_fingerprints, threshold=THRESHOLD):
    query_hashes = extract_frame_hashes(query_path)
    scores = {}

    for video, db_hashes in db_fingerprints.items():
        match_score = 0
        for qh in query_hashes:
            for dbh in db_hashes:
                if phash.hex_to_hash(qh) - phash.hex_to_hash(dbh) < threshold:
                    match_score += 1
        scores[video] = match_score

    best_match = max(scores, key=scores.get)
    return best_match, scores[best_match], scores

st.title("🎬 ACR (Video Fingerprinting) Demo")
st.markdown("Upload a video clip, and we’ll tell you which database video it belongs to.")

uploaded_file = st.file_uploader("Upload a short video clip", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.video(temp_path)
    st.info("Extracting fingerprints...")

    db = load_fingerprints()
    best_video, score, all_scores = match_query_clip(temp_path, db)

    st.success(f"✅ Best Match: **{best_video}** with score **{score}**")
    st.subheader("📊 Match Scores")
    st.json(all_scores)

    os.remove(temp_path)
