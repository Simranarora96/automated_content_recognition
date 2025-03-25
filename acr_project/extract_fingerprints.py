import os
import json
from utils import extract_frame_hashes
from tqdm import tqdm

DB_FOLDER = "video_db"
OUTPUT_FILE = "fingerprints.json"

def build_fingerprint_db():
    video_db = {}
    for filename in tqdm(os.listdir(DB_FOLDER), desc="Processing DB Videos"):
        if filename.lower().endswith((".mp4", ".mov", ".mkv")):
            path = os.path.join(DB_FOLDER, filename)
            video_db[filename] = extract_frame_hashes(path)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(video_db, f)
    print(f"✅ Fingerprints saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    build_fingerprint_db()
