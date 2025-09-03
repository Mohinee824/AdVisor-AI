#!/usr/bin/env bash
set -euo pipefail

LOG="run.log"
echo "Integration started: $(date)" > "$LOG"

# Step 1: Frame extraction
echo "[1] Frame extraction"
python3 ../member2_frames/extract_frames.py \
  --video member2_frames/my_video.mp4 \
  --out_dir member2_frames/frames \
  --index_csv member2_frames/frames_index.csv
echo "[1] Frame extraction completed" >> "$LOG"

# Step 2: Logo detection
echo "[2] Logo detection"
python ../yolov5/detect.py \
  --weights ../member3_detection/best.pt \
  --source member2_frames/my_video.mp4 \
  --save-csv
echo "[2] Logo detection completed" >> "$LOG"

# Step 3: KPI computation
echo "[3] KPI computation"
python3 ../member4_kpis/compute_kpis.py \
  --detections ../yolov5/runs/detect/exp15/raw_detections.csv \
  --out_csv ./member4_kpis/member4_kpis.csv
echo "[3] KPI computation completed" >> "$LOG"

# Step 4: Forecasting & visualization
echo "[4] Forecasting & visualization"
python3 ../member5_forecast/run_forecast.py \
  --kpi_csv ./member4_kpis/member4_kpis.csv \
  --out_csv ./member5_forecast/member5_forecast.csv \
  --figures_dir ./member5_forecast/reports/figures
echo "[4] Forecasting completed" >> "$LOG"

# Step 5: Copy frontend & docs
echo "[5] Copy frontend & docs"
mkdir -p member6_app/
cp -r ../member6_app/* member6_app/ >> "$LOG" 2>&1
echo "[5] Frontend copied" >> "$LOG"

echo "Integration completed: $(date)" >> "$LOG"
