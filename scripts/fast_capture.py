import cv2
import os
import time
import csv
from datetime import datetime
from skimage import color
from utils import config

# --- Config ---
TARGET_SERIAL = "YLAF20221208V0"
BOX_SIZE = config.BOX_SIZE

# --- Helper: Find Camera by Serial ---
def find_camera_by_serial(target_serial):
    by_id_path = "/dev/v4l/by-id"
    if os.path.exists(by_id_path):
        for dev in os.listdir(by_id_path):
            if target_serial in dev:
                full_path = os.path.join(by_id_path, dev)
                print(f"Found camera by serial: {full_path}")
                return full_path
        print(f"{by_id_path} exists but no device with serial '{target_serial}' found.")
    else:
        print(f"{by_id_path} not found. Falling back to /dev/video* scan.")
    
    # Fallback to /dev/video*
    for i in range(10):  # Check /dev/video0..9
        test_path = f"/dev/video{i}"
        if os.path.exists(test_path):
            print(f"Using fallback camera: {test_path}")
            return test_path
    
    raise RuntimeError("No usable camera found.")

# --- ROI Box Calculator ---
def get_roi_box(resolution, size):
    w, h = resolution
    margin_map = {
        "small": 0.375,   # 25% center box
        "medium": 0.25,   # 50% center box
        "large": 0.1      # 80% center box
    }
    margin = margin_map.get(size, 0.25)
    x1, x2 = int(w * margin), int(w * (1 - margin))
    y1, y2 = int(h * margin), int(h * (1 - margin))
    return x1, y1, x2, y2

# --- Main Capture ---
def capture_and_log(sample_id, mode):
    camera_path = find_camera_by_serial(TARGET_SERIAL)
    cap = cv2.VideoCapture(camera_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera at {camera_path}")
    print(f"Capturing in '{BOX_SIZE}' mode... Press 'q' to capture.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        x1, y1, x2, y2 = get_roi_box(frame.shape[:2], BOX_SIZE)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Live View (Press 'q' to capture)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Crop to ROI & Convert to LAB
    roi = frame[y1:y2, x1:x2]
    lab_img = color.rgb2lab(roi)
    avg_lab = lab_img.reshape(-1, 3).mean(axis=0)
    L, A, B = [round(v, 2) for v in avg_lab]
    
    # Log Results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"data/logs/{mode}_log.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if mode == "sample":
            writer.writerow([timestamp, sample_id, camera_path, L, A, B, "", "", ""])
        else:
            writer.writerow([timestamp, sample_id, camera_path, L, A, B])
    print(f"{mode.title()} logged: LAB = {{L}}, {{A}}, {{B}}")

# --- Entry Point ---
if __name__ == "__main__":
    mode = input("Enter mode ('master' or 'sample'): ").strip().lower()
    if mode not in ["master", "sample"]:
        print("Invalid mode.")
        exit()
    sample_id = input("Enter sample ID or color name: ").strip()
    capture_and_log(sample_id, mode)
