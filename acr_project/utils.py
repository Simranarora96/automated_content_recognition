import cv2
from PIL import Image
import imagehash

def extract_frame_hashes(video_path, frame_rate=1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * frame_rate)
    frame_hashes = []

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            hash_val = imagehash.phash(img)
            frame_hashes.append(str(hash_val))
        frame_idx += 1
    cap.release()
    return frame_hashes
