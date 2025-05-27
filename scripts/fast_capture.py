import cv2
import os
import csv
import numpy as np
from datetime import datetime
from skimage import color
from utils import config

# --- ROI Box Calculator ---
def get_roi_box(resolution, size):
    h, w = resolution
    margin_map = {
        "small": 0.375, # 25% center box
        "medium": 0.25, # 50% center box
        "large": 0.1,   # 80% center box
    }
    margin = margin_map.get(size, 0.25)
    x1, x2 = int(w * margin), int(w * (1 - margin))
    y1, y2 = int(h * margin), int(h * (1 - margin))
    return x1, y1, x2, y2

# --- Main Capture and Logging Function ---
def capture_and_log(sample_id, mode, camera_id=0):
    box_size = config.BOX_SIZE # Fixed from config

    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {camera_id}")

    print(f"Capturing in '{box_size}' mode... Press 'q' to capture.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Draw ROI box overlay
        x1, y1, x2, y2 = get_roi_box(frame.shape[:2], box_size)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Live View (Press 'q' to capture)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # --- Crop to ROI ---
    roi = frame[y1:y2, x1:x2]

    # --- Convert to LAB & Average ---
    lab_img = color.rgb2lab(roi)
    avg_lab = np.mean(lab_img.reshape(-1, 3), axis=0)
    L, A, B = [round(v, 2) for v in avg_lab]

    # --- Log to CSV ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"data/logs/{mode}_log.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if mode == "sample":
            writer.writerow([timestamp, sample_id, camera_id, L, A, B, "", "", ""])
        else:
            writer.writerow([timestamp, sample_id, camera_id, L, A, B])

    print(f"{mode.title()} logged: LAB = ({L}, {A}, {B})")

# --- Entry Point ---
if __name__ == "__main__":
    mode = input("Enter mode ('master' or 'sample'): ").strip().lower()
    if mode not in ["master", "sample"]:
        print("Invalid mode")
        exit()
    sample_id = input("Enter sample ID or color name: ").strip()
    capture_and_log(sample_id, mode, camera_id=0)
