#!/usr/bin/env python3
"""
Batch video processor for 3M Lighting consumer videos
Extracts: transcripts, audio, frames, emotion features
"""

from config import PATHS
import os
import json
import sys
from pathlib import Path
import whisper
import cv2
import librosa
import numpy as np
from datetime import datetime

# Configuration
OUTPUT_BASE = Path(PATHS["processed"])
FRAME_INTERVAL = 5  # seconds

def process_video(video_path, output_dir):
    """Process single video - extract all raw data"""
    print(f"\n{'='*60}")
    print(f"Processing: {Path(video_path).name}")
    print(f"{'='*60}")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        "video_path": str(video_path),
        "video_name": Path(video_path).name,
        "processed_at": datetime.now().isoformat(),
        "status": {}
    }
    
    # 1. Extract audio
    print("→ Extracting audio...")
    audio_path = output_dir / "audio.wav"
    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps if fps > 0 else 0
        cap.release()
        
        ffmpeg_bin = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/bin/ffmpeg"
        cmd = f'{ffmpeg_bin} -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" -y -loglevel error'
        os.system(cmd)
        results["status"]["audio"] = "✓" if audio_path.exists() else "✗"
        results["duration_seconds"] = duration
    except Exception as e:
        results["status"]["audio"] = f"✗ {str(e)}"
        print(f"  Error: {e}")
    
    # 2. Transcribe
    print("→ Transcribing...")
    try:
        model = whisper.load_model("large-v3", download_root="/Volumes/TARS/llm-models/whisper")
        result = model.transcribe(str(audio_path), language="en")
        
        transcript = {
            "text": result["text"],
            "segments": [{
                "start": s["start"],
                "end": s["end"],
                "text": s["text"]
            } for s in result["segments"]]
        }
        
        with open(output_dir / "transcript.json", "w") as f:
            json.dump(transcript, f, indent=2)
        
        results["status"]["transcript"] = "✓"
        results["transcript_word_count"] = len(result["text"].split())
    except Exception as e:
        results["status"]["transcript"] = f"✗ {str(e)}"
        print(f"  Error: {e}")
    
    # 3. Extract frames
    print("→ Extracting frames...")
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            if int(current_time) % FRAME_INTERVAL == 0:
                frame_path = frames_dir / f"frame_{int(current_time):04d}s.jpg"
                cv2.imwrite(str(frame_path), frame)
                frame_count += 1
        
        cap.release()
        results["status"]["frames"] = "✓"
        results["frames_extracted"] = frame_count
    except Exception as e:
        results["status"]["frames"] = f"✗ {str(e)}"
        print(f"  Error: {e}")
    
    # 4. Emotion features (prosodic analysis)
    print("→ Analyzing emotion...")
    try:
        y, sr = librosa.load(str(audio_path), sr=16000)
        
        # Extract prosodic features
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_mean = np.mean([pitches[:, i].max() for i in range(pitches.shape[1])])
        
        rms = librosa.feature.rms(y=y)[0]
        energy_mean = np.mean(rms)
        
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = np.mean(zcr)
        
        emotion_data = {
            "prosodic_features": {
                "pitch_mean": float(pitch_mean),
                "energy_mean": float(energy_mean),
                "zero_crossing_rate": float(zcr_mean)
            },
            "analysis_note": "Raw features - interpretation requires context"
        }
        
        with open(output_dir / "emotion_features.json", "w") as f:
            json.dump(emotion_data, f, indent=2)
        
        results["status"]["emotion"] = "✓"
    except Exception as e:
        results["status"]["emotion"] = f"✗ {str(e)}"
        print(f"  Error: {e}")
    
    # Save summary
    with open(output_dir / "processing_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Complete: {output_dir.name}")
    return results

if __name__ == "__main__":
    videos = [
        "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/MarkR_Activity8PainPoints_2025-06-30_115448_1.mov",
        "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/TylrD_Activity8PainPoints_2025-06-30_052938_1.MOV",
        "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/GeneK_Activity8PainPoints_2025-06-30_010218_1.webm",
        "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/FarahN_Activity8PainPoints_2025-07-02_083153_1.MOV",
        "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/FrederickK_Activity7ToolsandMaterials_2025-07-03_042614_1.mp4"
    ]
    
    batch_results = []
    for video in videos:
        output_name = Path(video).stem
        output_dir = OUTPUT_BASE / output_name
        result = process_video(video, output_dir)
        batch_results.append(result)
    
    # Batch summary
    print(f"\n{'='*60}")
    print("BATCH 1 SUMMARY")
    print(f"{'='*60}")
    for r in batch_results:
        status_str = " ".join([f"{k}:{v}" for k,v in r["status"].items()])
        print(f"{r['video_name']}: {status_str}")
