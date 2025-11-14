#!/usr/bin/env python3
import os, json, sys, cv2, librosa, numpy as np, whisper
from pathlib import Path
from datetime import datetime

from config import PATHS

os.environ['PATH'] = '/Users/anderson115/00-interlink/12-work/3m-lighting-project/bin:' + os.environ.get('PATH', '')

OUTPUT_BASE = Path(PATHS["processed"])
FRAME_INTERVAL = 5

video_path = sys.argv[1]
output_dir = OUTPUT_BASE / Path(video_path).stem
output_dir.mkdir(parents=True, exist_ok=True)

results = {"video_path": str(video_path), "video_name": Path(video_path).name, 
           "processed_at": datetime.now().isoformat(), "status": {}}

print(f"Processing: {Path(video_path).name}")

# 1. Extract audio
print("→ Extracting audio...")
audio_path = output_dir / "audio.wav"
os.system(f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" -y -loglevel error')
results["status"]["audio"] = "✓" if audio_path.exists() else "✗"

# 2. Transcribe
print("→ Transcribing...")
model = whisper.load_model("large-v3", download_root="/Volumes/TARS/llm-models/whisper")
result = model.transcribe(str(audio_path), language="en", fp16=False)
transcript = {"text": result["text"], "segments": [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in result["segments"]]}
with open(output_dir / "transcript.json", "w") as f:
    json.dump(transcript, f, indent=2)
results["status"]["transcript"] = "✓"
results["transcript_segments"] = len(result["segments"])

# 3. Extract frames
print("→ Extracting frames...")
frames_dir = output_dir / "frames"
frames_dir.mkdir(exist_ok=True)
cap = cv2.VideoCapture(str(video_path))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret: break
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
    if int(current_time) % FRAME_INTERVAL == 0:
        cv2.imwrite(str(frames_dir / f"frame_{int(current_time):04d}s.jpg"), frame)
        frame_count += 1
cap.release()
results["status"]["frames"] = "✓"
results["frames_extracted"] = frame_count

# 4. Emotion features
print("→ Analyzing emotion...")
y, sr = librosa.load(str(audio_path), sr=16000)
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
rms = librosa.feature.rms(y=y)[0]
emotion_data = {"pitch_mean": float(np.mean([pitches[:, i].max() for i in range(pitches.shape[1])])), 
                "energy_mean": float(np.mean(rms))}
with open(output_dir / "emotion_features.json", "w") as f:
    json.dump(emotion_data, f, indent=2)
results["status"]["emotion"] = "✓"

with open(output_dir / "processing_summary.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"✓ Complete: {results['transcript_segments']} segments, {frame_count} frames")
