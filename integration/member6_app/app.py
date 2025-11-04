from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:8080"])

@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    video = request.files.get('video')
    if not video:
        return jsonify({"error": "No video uploaded"}), 400

    filename = video.filename
    save_path = os.path.join("member2_frames", filename)
    video.save(save_path)

    try:
        subprocess.run(["python3", "run_all.py", filename], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Pipeline failed", "details": str(e)}), 500

    results = []
    try:
        with open("member4_kpis/member4_kpis.csv") as f:
            lines = f.readlines()[1:]  # skip header
            for line in lines:
                frame_id, timestamp, class_name, confidence, x, y, w, h = line.strip().split(",")
                results.append({
                    "frame_id": frame_id,
                    "timestamp": timestamp,
                    "class_name": class_name,
                    "confidence": float(confidence),
                    "x": x, "y": y, "width": w, "height": h
                })
    except Exception as e:
        return jsonify({"error": "Failed to read results", "details": str(e)}), 500

    return jsonify({
        "filename": filename,
        "results": results
    })

if __name__ == '__main__':
    app.run(host="localhost", port=5050)
