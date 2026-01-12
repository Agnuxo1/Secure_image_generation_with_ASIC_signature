#!/usr/bin/env python3
"""
SILICON SIGNATURE ENGINE (PROOF-OF-ART)
=======================================
1. Hushes the image.
2. Sends hash to ASIC as 'PrevHash'.
3. Receives authenticated Nonce.
4. Embeds everything into PNG metadata.
"""

import os
import sys
import json
import socket
import hashlib
import binascii
from PIL import Image, PngImagePlugin

def get_silicon_signature(image_path, api_host="127.0.0.1", api_port=4000):
    print(f"[SIGN] Loading image: {image_path}")
    img = Image.open(image_path)
    
    # 1. Generate Image Hash (Structural Identity)
    pixel_data = img.tobytes()
    img_hash = hashlib.sha256(pixel_data).hexdigest()
    print(f"[SIGN] Structural Hash: {img_hash}")
    
    # 2. Request Signature from ASIC Bridge
    print(f"[SIGN] Requesting ASIC authentication from {api_host}:{api_port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30) # Signing can take a few seconds
        sock.connect((api_host, api_port))
        
        # Send hash as data
        payload = json.dumps({"data": img_hash})
        sock.send((payload + "\n").encode())
        
        # Receive Proof
        resp = sock.recv(4096).decode().strip()
        sock.close()
        
        if not resp:
            print("[ERROR] No response from Bridge")
            return None
            
        result = json.loads(resp)
        if "error" in result:
            print(f"[ERROR] Bridge: {result['error']}")
            return None
            
        # 3. Extract Proof Details
        nonce = result["nonce"]
        params = result["params"] # ["worker", "job_id", "extranonce2", "ntime", "nonce"]
        extranonce2 = params[2]
        ntime = params[3]
        
        print(f"[SUCCESS] ASIC Signature acquired!")
        print(f" > Nonce: {nonce} | Extranonce2: {extranonce2} | Ntime: {ntime}")
        
        # 4. Embed in PNG Metadata
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Silicon-Auth-Hash", img_hash)
        metadata.add_text("Silicon-Auth-Nonce", nonce)
        metadata.add_text("Silicon-Auth-Extranonce2", extranonce2)
        metadata.add_text("Silicon-Auth-Ntime", ntime)
        metadata.add_text("Silicon-Auth-Version", "20000000") # From bridge config
        metadata.add_text("Silicon-Auth-Status", "AUTHENTICATED_BY_BM1387")
        
        auth_path = image_path.replace(".png", "_auth.png")
        img.save(auth_path, "PNG", pnginfo=metadata)
        print(f"[DONE] Authenticated Art saved to: {auth_path}")
        return auth_path
        
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

if __name__ == "__main__":
    target = "D:/ASIC-ANTMINER_S9/ASIC_DIFFUSION_Art_Research_Memo/silicon_tv_v4.png"
    if not os.path.exists(target):
        # Create a dummy one if not exists for testing
        print("[WARN] Target not found, creating dummy 720p...")
        dummy = Image.new('L', (1280, 720), 128)
        dummy.save(target)
        
    get_silicon_signature(target)
