import pandas as pd
import glob

OUTPUT_FILE = 'member4_kpis.csv'
MAX_FRAME_GAP = 15

try:
    detection_files = sorted(glob.glob('../yolov5/runs/detect/exp*/raw_detections.csv'))
    if not detection_files:
        raise FileNotFoundError("No raw_detections.csv found in any exp folder.")
    
    INPUT_FILE = detection_files[-1]
    detections_df = pd.read_csv(INPUT_FILE)
    detections_df = detections_df.sort_values(by=['class_name', 'frame_id'])
    detections_df['frame_diff'] = detections_df.groupby('class_name')['frame_id'].diff()
    detections_df['is_new_appearance'] = (detections_df['frame_diff'] > MAX_FRAME_GAP).fillna(1).astype(int)
    detections_df['appearance_group_id'] = detections_df.groupby('class_name')['is_new_appearance'].cumsum()
    detections_df['appearance_id'] = detections_df['class_name'] + '_' + detections_df['appearance_group_id'].astype(str)

    kpi_df = detections_df.groupby('appearance_id').agg({
        'frame_id': ['min', 'max'],
        'confidence': ['mean']
    })

    kpi_df.columns = ['start_frame', 'end_frame', 'avg_confidence']
    kpi_df['duration_frames'] = kpi_df['end_frame'] - kpi_df['start_frame'] + 1
    kpi_df = kpi_df.reset_index()
    kpi_df['class_name'] = kpi_df['appearance_id'].apply(lambda x: x.split('_')[0])

    final_kpi_df = kpi_df[['appearance_id', 'class_name', 'start_frame', 'end_frame', 'duration_frames', 'avg_confidence']]
    final_kpi_df.to_csv(OUTPUT_FILE, index=False)

    print("--- KPI Computation and Aggregation Complete ---")
    print(f"Final KPIs saved to: {OUTPUT_FILE}")
    print("\n--- Sample of Final Output ---")
    print(final_kpi_df.head())

except FileNotFoundError as e:
    print(f"ERROR: {e}")
    print("Make sure YOLOv5 detection was run and raw_detections.csv was generated.")
