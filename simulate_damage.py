
from PIL import Image, ImageDraw
import numpy as np

path = 'D:/ASIC-ANTMINER_S9/ASIC_DIFFUSION_Art_Research_Memo/Secure_image_generation_with_ASIC_signature/Imagen_test10_rsw.jpg'
out_path = 'D:/ASIC-ANTMINER_S9/ASIC_DIFFUSION_Art_Research_Memo/Secure_image_generation_with_ASIC_signature/Imagen_test10_rsw_damaged.jpg'

print(f"Loading {path}...")
img = Image.open(path).convert('RGB')
draw = ImageDraw.Draw(img)

w, h = img.size

# Simulate massive editing (Glasses and Mustache)
# This destroys LSBs in the affected area
print("Applying 'Glasses and Mustache' damage (approx 20% area)...")

# Glasses
draw.ellipse([w*0.2, h*0.3, w*0.45, h*0.45], fill=(0,0,0))
draw.ellipse([w*0.55, h*0.3, w*0.8, h*0.45], fill=(0,0,0))
draw.line([w*0.45, h*0.37, w*0.55, h*0.37], fill=(0,0,0), width=10)

# Mustache
draw.rectangle([w*0.3, h*0.6, w*0.7, h*0.7], fill=(50,20,20))

# Save damaged image
img.save(out_path)
print(f"Saved damaged image to {out_path}")
