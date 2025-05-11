import csv
import cv2
import os
from datetime import datetime

def capture_image(camera_index=0):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError(f"Failed to open camera at index {camera_index}.")
    
    print("Capturing image... Press 'q' to confirm capture.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow("Live Preview - Press 'q' to Capture", frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return frame

def save_image(frame, mode, sample_id, camera_id=0):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_id = sample_id.lower().replace(" ", "_")
    filename = f"{clean_id}.png"

    if mode == "master":
        save_path = os.path.join("data", "masters")
        log_path = os.path.join("data", "logs", "master_log.csv")
    else:  # Scan mode
        save_path = os.path.join("data", "samples")
        log_path = os.path.join("data", "logs", "sample_log.csv")

    os.makedirs(save_path, exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    file_path = os.path.join(save_path, filename)
    cv2.imwrite(file_path, frame)

    # Logging
    log_entry = [timestamp, sample_id, filename, camera_id]
    if mode == "sample":
        log_entry.extend(["", "", ""])  # Placeholders for reference color, delta E, result

    with open(log_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(log_entry)

    print(f"{mode.capitalize()} Image saved to: {file_path}")
    print(f"Logged entry to: {log_path}")

    return file_path

def main():
    print("=== COLOR INSPECTION IMAGE CAPTURE ===")
    mode = input("Enter mode ('master' or 'sample'): ").strip().lower()
    if mode not in ["master", "sample"]:
        print("Invalid mode. Choose 'master' or 'sample'.")
        return
    
    sample_id = input("Enter color name or sample ID: ").strip()

    camera_index = 0
    frame = capture_image(camera_index)
    save_image(frame, mode, sample_id, camera_id=camera_index)

if __name__ == "__main__":
    main()
    