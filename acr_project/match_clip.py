import json
import os
from utils import extract_frame_hashes_with_timestamps
from imagehash import phash

FINGERPRINT_FILE = "fingerprints.json"
QUERY_FOLDER = "query_clips"
THRESHOLD = 10

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
    print(f"🎯 Best match: {best_video} (Score: {scores[best_video]})")
    if segment:
        print(f"🕒 Matching segment: {segment[0]}s → {segment[1]}s")
    return best_video, segment

if __name__ == "__main__":
    fingerprints = load_fingerprints()
    for filename in os.listdir(QUERY_FOLDER):
        if filename.lower().endswith((".mp4", ".mov", ".mkv")):
            path = os.path.join(QUERY_FOLDER, filename)
            match_query_clip(path, fingerprints)
