#!/usr/bin/env python3
"""Simple benchmark runner for embedding+verification using simulated ASIC responses.
Generates a JSON results file that can be uploaded to W&B or stored as CI artifact.
"""
import os
import time
import json
import random
import hashlib
from PIL import Image, PngImagePlugin
from verify_silicon_art import verify_art

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ORIGINALS = os.path.join(ROOT, 'Originals')
RESULTS = os.path.join(ROOT, 'benchmarks', 'results.json')

os.makedirs(os.path.dirname(RESULTS), exist_ok=True)

images = []
if os.path.isdir(ORIGINALS):
    for fn in os.listdir(ORIGINALS):
        if fn.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(os.path.join(ORIGINALS, fn))
else:
    print("No Originals folder found; exiting.")
    images = []

results = []
for img in images:
    start = time.time()
    im = Image.open(img)
    pixel_data = im.tobytes()
    img_hash = hashlib.sha256(pixel_data).hexdigest()

    # Simulate ASIC response (fake nonce and extranonce2)
    nonce = format(random.getrandbits(32), '08x')
    extranonce2 = format(random.getrandbits(32), '08x')
    ntime = format(int(time.time()), '08x')

    # Embed metadata
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Silicon-Auth-Hash", img_hash)
    metadata.add_text("Silicon-Auth-Nonce", nonce)
    metadata.add_text("Silicon-Auth-Extranonce2", extranonce2)
    metadata.add_text("Silicon-Auth-Ntime", ntime)
    metadata.add_text("Silicon-Auth-Version", "20000000")
    metadata.add_text("Silicon-Auth-Status", "SIMULATED_AUTH")

    out_path = img.replace('.png', '_bench_auth.png') if img.endswith('.png') else img + '_bench_auth.png'
    im.save(out_path, 'PNG', pnginfo=metadata)
    embed_time = time.time() - start

    # Verify
    ok = verify_art(out_path)
    verify_status = 'VERIFIED' if ok else 'FAILED'
    total_time = time.time() - start

    r = {
        'image': os.path.basename(img),
        'embed_time_s': round(embed_time, 4),
        'verify_status': verify_status,
        'total_time_s': round(total_time, 4),
        'nonce': nonce,
        'extranonce2': extranonce2
    }
    results.append(r)

with open(RESULTS, 'w') as f:
    json.dump({'runs': results, 'timestamp': time.time()}, f, indent=2)

print(f"Benchmarks completed: {len(results)} runs. Results written to {RESULTS}")
