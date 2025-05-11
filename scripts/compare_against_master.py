import os
import csv
from datetime import datetime
from skimage import io, color
import numpy as np
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000

# --- Settings ---
SAMPLES_DIR = "data/samples"
MASTERS_DIR = "data/masters"
LOG_PATH = "data/logs/sample_log.csv"
TOLERANCE = 1.0 # Adjust delta tolerance as needed. Need to check tolerance

# --- Utilities ---
def calculate_average_lab(image_path):
    rgb = io.imread(image_path)
    lab = color.rgb2lab(rgb)
    avg_lab = np.mean(lab.reshape(-1, 3), axis=0)
    return LabColor(*avg_lab)

def compare_sample_to_master(sample_path, master_path):
    sample_lab = calculate_average_lab(sample_path)
    master_lab = calculate_average_lab(master_path)
    return delta_e_cie2000(sample_lab, master_lab)

def update_log(sample_id, delta_e, reference_color, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{sample_id.lower().replace(' ', '_')}.png"

    updated_rows = []
    entry_updated = False

    if not os.path.exists(LOG_PATH):
        print("Log file not found. Aborting update.")
        return
    
    with open(LOG_PATH, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3 and row[1] ==sample_id and row[2] == filename:
                while len(row) < 7:
                    row.append  # Pad missing fields
                row[3] = "0"  # Or actual camera_id if tracked
                row[4] = reference_color
                row[5] = f"{delta_e:.2f}"
                row[6] = result
                entry_updated = True
            updated_rows.append(row)

    if not entry_updated:
        print(f"Sample '{sample_id}' not found in log. Skipping log update.")
        return

    with open(LOG_PATH, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)

    print("Log updated.")

# --- Main ---
def main():
    print("=== COLOR COMPARISON ===")
    sample_id = input("Enter sample ID (filename without extension): ").strip()
    reference_color = input ("Enter reference master color name (e.g., Paradise Dream): ").strip()

    sample_path = os.path.join(SAMPLES_DIR, f"{sample_id}.png")
    master_path = os.path.join(MASTERS_DIR, f"{reference_color}.png")

    if not os.path.exists(sample_path):
        print(f"Sample image not found: {sample_path}")
        return
    if not os.path.exists(master_path):
        print(f"Master image not found: {master_path}")
        return
    delta_e = compare_sample_to_master(sample_path, master_path)
    result = "PASS" if delta_e <= TOLERANCE else "FAIL"

    print(f"ΔE = {delta_e:.2f} | Tolerance = {TOLERANCE} → {result}")
    update_log(sample_id, delta_e, reference_color, result)

if __name__ == "__main__":
    main()
