# DSN2098 Sponsor Logo Detection & Forecasting Pipeline

## 🧠 Overview
This project detects sponsor logos in IPL match footage, computes visibility KPIs, and forecasts future exposure. It integrates outputs from six team members into a unified pipeline.

## 📁 Folder Structure
integration/ ├── member2_frames/ # Extracted frames + index ├── member3_detection/ # Annotated images + detections ├── member4_kpis/ # KPI metrics ├── member5_forecast/ # Forecast results + plots ├── member6_app/ # Frontend files ├── run_all.sh # Integration script └── run.log  # Execution log
Code

## 🚀 How to Run
1. Activate virtual environment:
   ```bash
   source venv/bin/activate
Run the pipeline:
bash
cd integration
./run_all.sh
🧪 Dependencies
See requirements.txt for all required packages.
📦 Dataset & Training
Training data is located in member3_detection/dataset/
Configuration: data.yaml, readme.dataset.txt, readme.roboflow.txt
Detection model: YOLOv5 (/yolov5/)
👥 Team Members
Member 1: Integration & orchestration
Member 2: Frame extraction
Member 3: Logo detection
Member 4: KPI computation
Member 5: Forecasting
Member 6: Frontend
📌 Notes
Raw video files are excluded from GitHub. Use sample frames or external links.
For retraining, follow instructions in member3_detection/dataset_config/
Code

---

### 📦 `requirements.txt` — Dependencies

```txt
torch>=2.0.0
opencv-python
pandas
matplotlib
seaborn
scikit-learn
numpy
