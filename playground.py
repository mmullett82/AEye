from utils.lab_tools import lab_to_rgb, rgb_to_lab

# Example: Convert master LAB to RGB
master_lab = (55.2, 9.3, 18.7)
converted_rgb = lab_to_rgb(*master_lab)

print(f"RGB for Walnut Stain (LAB {master_lab}) is {[int(x) for x in converted_rgb]}")

# Now go full loop: RGB → LAB → RGB
roundtrip_lab = rgb_to_lab(*converted_rgb)
print(f"Back to LAB: {[round(float(x), 2) for x in roundtrip_lab]}")