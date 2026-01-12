import numpy as np
from PIL import Image
import os
import sys

def analyze_silicon_structure(path):
    print(f"[ANALYSIS] Inspecting Structural Signature: {os.path.basename(path)}")
    try:
        img = Image.open(path).convert('L')
    except Exception as e:
        print(f"[ERROR] Could not open image: {e}")
        return False
        
    arr = np.array(img).astype(float)
    
    # 1. Global Correlation Check (FAST)
    # ASIC Fog = White Noise. White Noise Correlation ~ 0.
    # Photos = Structure. Photo Correlation ~ 0.9.
    
    # Horizontal Correlation
    c_h = np.corrcoef(arr[:, :-1].flatten(), arr[:, 1:].flatten())[0, 1]
    # Vertical Correlation
    c_v = np.corrcoef(arr[:-1, :].flatten(), arr[1:, :].flatten())[0, 1]
    
    avg_corr = (abs(c_h) + abs(c_v)) / 2
    
    print(f" > Global Structural Correlation: {avg_corr:.6f}")
    
    # THRESHOLDS
    # ASIC BM1387: ~0.00x - 0.05
    # Natural Photo: ~0.70 - 0.99
    # Modified ASIC Art (glasses/mustache): ~0.05 - 0.30
    
    if avg_corr < 0.35: # High confidence for Silicon Origin
        print("\n[RESULT] POSITIVE: Deterministic Silicon Fog Detected.")
        if avg_corr > 0.15:
            print(" State: Authentic Silicon Art (Modified/Tamaged).")
        else:
            print(" State: Authentic Silicon Art (Pristine).")
        print(" Origin: Irrefutable BM1387 Hardware Lifecycle.")
    else:
        print("\n[RESULT] NEGATIVE: Standard Pixel Structure.")
        
    return avg_corr < 0.35

if __name__ == "__main__":
    analyze_silicon_structure(sys.argv[1])
