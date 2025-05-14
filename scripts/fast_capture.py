import cv2
import os
import csv
import numpy as np
from datetime import datetime
from skimage import color

def capture_and_log(sample_id, mode, camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {camera_id}")

    print("Capturing image... Press 'q' to capture.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow("Live View (Press 'q' to capture)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # --- ROI Cropping Placeholder ---
    # Crop to center square (50% area)
    h, w = frame.shape[:2]
    crop = frame[h//4:3*h//4, w//4:3*w//4]

    # --- Convert to LAB & Average ---
    lab_img = color.rgb2lab(crop)
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

if __name__ == "__main__":
    mode = input("Enter mode ('master' or 'sample'): ").strip().lower()
    if mode not in ["master", "sample"]:
        print("Invalid mode")
        exit()
    sample_id = input("Enter sample ID or color name: ").strip()
    capture_and_log(sample_id, mode)
