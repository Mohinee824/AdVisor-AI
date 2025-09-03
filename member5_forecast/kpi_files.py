# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 15:29:34 2025

@author: HP
"""

import pandas as pd
import numpy as np

# Load raw detections
raw_path = "C:/Users/HP/Downloads/brand_kpis/raw_detections/raw_detections.csv"   # update path if needed
df = pd.read_csv(raw_path)

df["second"] = df["timestamp"].astype(int)

kpi_list = []
fps = 30

for second, group in df.groupby("second"):
    impressions = len(group)
    unique_frames = group["frame_id"].nunique()
    
    screen_time = unique_frames / fps
    exposure_rate = unique_frames / fps   # since denominator = fps frames per second
    
    kpi_list.append({
        "second": second,
        "impressions": impressions,
        "screen_time": screen_time,
        "exposure_rate": exposure_rate
    })




# Step 3: convert to DataFrame
kpis = pd.DataFrame(kpi_list)


print(" member4_kpis.csv has been created with KPIs per minute.")
output_path = r"E:/Project/kpi_files/kpis.csv"
kpis.to_csv(output_path, index=False)
print(f" File saved at: {output_path}")
