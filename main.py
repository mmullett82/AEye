import argparse
import json
from utils.lab_tools import rgb_to_lab
from comparison.delta_e_calculator import delta_e

# Load master samples
with open('comparison/master_samples.json', 'r') as file:
    master_samples = json.load(file)

# Set up CLI argument parsing
parser = argparse.ArgumentParser(description="AEye Color Comparator")
parser.add_argument('--sample', type=str, required=True, help='Name of master color sample')
parser.add_argument('--rgb', nargs=3, type=int, required=True, metavar=('R', 'G', 'B'), help='RGB values to test')
args = parser.parse_args()

# Pull master sample
sample_name = args.sample
if sample_name not in master_samples:
    print(f"❌ Error: '{sample_name}' not found in master_samples.json")
    exit(1)

master_lab = master_samples[sample_name]['lab']
tolerance = master_samples[sample_name]['tolerance']

# Convert input RGB to LAB
input_rgb = args.rgb
input_lab = rgb_to_lab(*input_rgb)

# Calculate Delta E
delta = delta_e(input_lab, master_lab)

# Print Results
print("\n--- AEye Color Comparison ---")
print(f"Selected Sample: {sample_name}")
print(f"Input RGB: {input_rgb}")
print(f"Converted LAB: {[round(x, 2) for x in input_lab]}")
print(f"Reference LAB: {master_lab}")
print(f"Delta E: {delta:.2f}")

if delta <= tolerance:
    print("✅ Result: IN RANGE")
else:
    print("❌ Result: OUT OF RANGE")
