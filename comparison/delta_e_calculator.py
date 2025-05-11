from skimage.color import deltaE_cie76, deltaE_ciede2000
import numpy as np

def delta_e(lab1, lab2, method='CIE2000'):
    lab1 = np.array([[lab1]])
    lab2 = np.array([[lab2]])
    if method == 'CIE76':
        return float(deltaE_cie76(lab1, lab2)[0][0])
    elif method == 'CIE2000':
        return float(deltaE_ciede2000(lab1, lab2)[0][0])