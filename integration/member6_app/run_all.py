#!/usr/bin/env python3

import sys
import os
import subprocess
from datetime import datetime

LOG = "run.log"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def run_command(command, step_name):
    log(f"[{step_name}] Starting")
    subprocess.run(command, check=True)
    log(f"[{step_name}] Completed")

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_all.py <video_filename>")
        sys.exit(1)

    video_filename = sys.argv[1]
    video_path = os.path.join("member2_frames", video_filename)

    # Clear log
    with open(LOG, "w") as f:
        f.write(f"Integration started: {datetime.now()}\n")

    # Step 1: Frame extraction
    run_command([
        "python3", "../member2_frames/extract_frames.py",
        "--video", video_path,
        "--out_dir", "member2_frames/frames",
        "--index_csv", "member2_frames/frames_index.csv"
    ], "1 Frame extraction")

    # Step 2: Logo detection
    run_command([
        "python", "../yolov5/detect.py",
        "--weights", "../member3_detection/best.pt",
        "--source", video_path,
        "--save-csv"
    ], "2 Logo detection")

    # Step 3: KPI computation
    run_command([
        "python3", "../member4_kpis/compute_kpis.py",
        "--detections", "../yolov5/runs/detect/exp15/raw_detections.csv",
        "--out_csv", "member4_kpis/member4_kpis.csv"
    ], "3 KPI computation")

    # Step 4: Forecasting & visualization
    run_command([
        "python3", "../member5_forecast/run_forecast.py",
        "--kpi_csv", "member4_kpis/member4_kpis.csv",
        "--out_csv", "member5_forecast/member5_forecast.csv",
        "--figures_dir", "member5_forecast/reports/figures"
    ], "4 Forecasting & visualization")

    # Step 5: Copy frontend & docs
    os.makedirs("member6_app", exist_ok=True)
    run_command([
        "cp", "-r", "../member6_app/", "member6_app/"
    ], "5 Copy frontend & docs")

    log("Integration completed")

if __name__ == "__main__":
    main()
