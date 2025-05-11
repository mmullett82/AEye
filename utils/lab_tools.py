from skimage.color import lab2rgb, rgb2lab
import numpy as np

def rgb_to_lab(r, g, b):
    # Converts RGB values (0-255) to LAB color space
    rgb = np.array([[[r / 255.0, g / 255.0, b / 255.0]]]) # Normalize RGB to 0-1
    lab = rgb2lab(rgb)
    return tuple(float(x) for x in lab[0][0])

def lab_to_rgb(l, a, b):
    # Converts LAB values to RGB color space (0-255)
    lab = np.array([[[l, a, b]]])
    rgb_float = lab2rgb(lab)
    rgb_255 = (rgb_float[0][0] * 255).astype(np.uint8)
    return tuple(rgb_255)