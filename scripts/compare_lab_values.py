import csv
import os
from datetime import datetime
from comparison.delta_e_calculator import delta_e


# --- Settings ---
MASTER_LOG = "data/logs/master_log.csv"
SAMPLE_LOG = "data/logs/sample_log.csv"
TOLERANCE = 1.0 # Adjust delta tolerance as needed. Need to check tolerance

# --- Utilities ---
def read_latest_entry(log_path):
    with open(log_path, "r") as file:
        lines = file.readlines()
        if not lines:
            raise ValueError("Log file is empty")
        header = lines[0]
        last = lines[-1]
        return header.strip().split(","), last.strip().split(",")
    
def update_sample_log(sample_id, delta_e, reference, result):
    updated_rows = []
    with open(SAMPLE_LOG, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 9:
                row += [""] * (9 - len(row))
            if row[1] == sample_id:
                row[6] = reference
                row[7] = f"{delta_e:.2f}"
                row[8] = result
            updated_rows.append(row)

    with open(SAMPLE_LOG, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

if __name__ == "__main__":
    print("=== Compare Sample to Master ===")
    reference = input("Enter master sample name (e.g., 'oak_stain'): ").strip()

    master_header, master_row = read_latest_entry(MASTER_LOG)
    sample_header, sample_row = read_latest_entry(SAMPLE_LOG)

    master_id = master_row[1]
    sample_id = sample_row[1]

    master_lab = [float(master_row[3]), float(master_row[4]), float(master_row[5])]
    sample_lab = [float(sample_row[3]), float(sample_row[4]), float(sample_row[5])]

    delta_e = calculate_delta_e(master_lab, sample_lab)
    result = "PASS" if delta_e <= TOLERANCE else "FAIL"

    print(f"Sample '{sample_id}' vs Master '{reference}'")
    print(f"LAB deltaE: {delta_e:.2f} → {result}")

    update_sample_log(sample_id, delta_e, reference, result)
    print("Sample log updated.")
