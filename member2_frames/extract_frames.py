import cv2
import pandas as pd
import os

source_video_file = "my_video.mp4" 
output_frames_folder = "frames"
output_csv_file = "frames_index.csv"


if not os.path.exists(output_frames_folder):
    os.makedirs(output_frames_folder)


video_capture = cv2.VideoCapture(source_video_file)


if not video_capture.isOpened():
    print("Error: Could not open video.")
    exit()

frame_data = []
current_frame_count = 0


while True:
    success, frame = video_capture.read()
    if not success:
        break  
    

    frame_image_name = f"frame_{current_frame_count:05d}.jpg"
    frame_image_path = os.path.join(output_frames_folder, frame_image_name)
  
    cv2.imwrite(frame_image_path, frame)

    frame_info = {
        'frame_id': current_frame_count,
        'filename': frame_image_name,
        'timestamp_ms': video_capture.get(cv2.CAP_PROP_POS_MSEC)
    }
    frame_data.append(frame_info)
    
    current_frame_count += 1
    
video_capture.release()
cv2.destroyAllWindows()

df = pd.DataFrame(frame_data)
df.to_csv(output_csv_file, index=False)

print(f"Successfully extracted {current_frame_count} frames and created {output_csv_file}.")
