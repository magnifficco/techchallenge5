import os
import cv2
import zipfile
from pathlib import Path
from uuid import uuid4

def process_video(filepath: str, output_dir: str = "outputs") -> str:
    video_id = str(uuid4())
    frame_dir = Path(output_dir) / f"frames_{video_id}"
    frame_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(filepath)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = frame_dir / f"frame_{frame_count:05d}.jpg"
        cv2.imwrite(str(frame_path), frame)
        frame_count += 1

    cap.release()

    # Compactar os frames
    zip_path = Path(output_dir) / f"{video_id}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in frame_dir.iterdir():
            zipf.write(file, arcname=file.name)

    return str(zip_path)
