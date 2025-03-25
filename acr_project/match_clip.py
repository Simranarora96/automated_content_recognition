import json
import os
from utils import extract_frame_hashes
from imagehash import phash

FINGERPRINT_FILE = "fingerprints.json"
QUERY_FOLDER = "query_clips"
THRESHOLD = 10

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
    print(f"🎯 Best match for {os.path.basename(query_path)}: {best_match} (Score: {scores[best_match]})")

if __name__ == "__main__":
    fingerprints = load_fingerprints()
    for filename in os.listdir(QUERY_FOLDER):
        if filename.lower().endswith((".mp4", ".mov", ".mkv")):
            path = os.path.join(QUERY_FOLDER, filename)
            match_query_clip(path, fingerprints)
