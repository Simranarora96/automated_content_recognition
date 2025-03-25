# 🎬 ACR Project – Video Fingerprinting & Matching

This project is a lightweight **Automatic Content Recognition (ACR)** system that identifies which video a given clip belongs to using **video fingerprinting** with **perceptual hashing and frame comparison**.

It's perfect for offline testing, media monitoring, or building the base of a larger real-time ACR engine.

---

## 🧠 How It Works

1. **Fingerprint Database Creation**
   - Extracts perceptual hashes from key frames of known videos (`video_db/`)
   - Stores them in `fingerprints.json`

2. **Clip Matching**
   - Takes a short query clip (`query_clips/`)
   - Extracts its fingerprints
   - Compares with database using Hamming distance
   - Returns the best-matching video

3. **Streamlit Web App**
   - Upload and analyze video clips
   - View match results interactively

---

## 📁 Project Structure

```
acr_project/
├── video_db/                 # Add your 5 reference videos here
├── query_clips/             # Add short test clips here
├── fingerprints.json         # Auto-generated fingerprints DB
│
├── utils.py                 # Shared code for frame hashing
├── extract_fingerprints.py  # Step 1: Build fingerprints
├── match_clip.py            # Step 2: Match test clips (CLI)
└── streamlit_app.py         # Step 3: Web interface
```

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install opencv-python imagehash pillow numpy tqdm streamlit
```

### 2. Add Videos

- Put **reference videos** in `video_db/`
- Put **test clips** in `query_clips/`

### 3. Generate Fingerprints

```bash
python extract_fingerprints.py
```

### 4. Match a Clip via CLI

```bash
python match_clip.py
```

### 5. Or Use the Web App

```bash
streamlit run streamlit_app.py
```

---

## ⚙️ Configuration

- **Frame rate**: Extracts 1 frame/sec by default
- **Threshold**: Matching tolerance (default: `10`) — lower = stricter

---

## 📌 Notes

- Works best with short clips (3–10 seconds)
- Matching is robust to compression, watermarking, slight changes
- Easily extendable to include audio or deep learning embeddings

---

## 🧩 To-Do / Improvements

- [ ] Use scene-change detection for better frame sampling
- [ ] Add audio fingerprinting for hybrid matching
- [ ] Use SQLite or Pinecone for scalable DB
- [ ] Add visualization of frame matches
