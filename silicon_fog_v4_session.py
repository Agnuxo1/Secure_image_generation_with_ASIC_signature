#!/usr/bin/env python3
"""
SILICON FOG V4 SESSION (SILICON TV)
==================================
Uses the proven medical-grade V4 drivers to reveal art from fog.

Workflow:
1. Bridge (V4) -> Manages S9 Stratum
2. Session (This) -> Requests hashes from Bridge & Dissipates Fog
"""

import os
import sys
import time
import json
import socket
import numpy as np
import threading
import subprocess
from PIL import Image, ImageDraw
from collections import deque

# Add v4_drivers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'v4_drivers'))
# Note: we will use asic_interface if needed, or raw socket to Bridge API

# ==============================================================================
# FOG ENGINE (Refined for V4 Interference Model)
# ==============================================================================

class SiliconFogEngine:
    def __init__(self, size=128):
        self.size = size
        self.fog = None
        self.target = None
        self.frame_count = 0
        
        # Create Artistic Target (The Signal inside the Noise)
        self._create_target_art()
        self._init_fog()
        
    def _create_target_art(self):
        """Creates the 'Ideal Form' hidden in the silicon noise."""
        img = Image.new('L', (self.size, self.size), 0)
        draw = ImageDraw.Draw(img)
        
        # Triangle (Primitive Resonance)
        cx, cy = self.size // 2, self.size // 2
        r = self.size // 3
        points = [(cx, cy - r), (cx - r, cy + r), (cx + r, cy + r)]
        draw.polygon(points, fill=255)
        
        self.target = np.array(img, dtype=np.float32) / 255.0
        
    def _init_fog(self):
        """Initializes the structured logic fog."""
        noise = np.random.random((self.size, self.size)).astype(np.float32)
        # The fog is 90% chaos, 10% target structure
        self.fog = 0.9 * noise + 0.1 * self.target
        
    def dissipate(self, delta_ms: float, nonce_hex: str):
        """
        Uses ASIC timing and entropy to CANCEL the noise and reveal target.
        """
        # 1. Energy from Timing
        # Low latency = High energy focus
        energy = 1.0 - min(delta_ms / 500.0, 1.0)
        
        # 2. Pattern from Nonce (Structural Interference)
        # Use nonce to create a resonance map
        nonce_val = int(nonce_hex, 16)
        np.random.seed(nonce_val % (2**31))
        resonance_map = np.random.random((self.size, self.size)).astype(np.float32)
        
        # 3. Interference Calculation
        # Where resonance_map matches target, disspation is stronger
        affinity = 1.0 - np.abs(resonance_map - self.target)
        
        # 4. Selective Dissipation
        strength = energy * affinity * 0.05
        self.fog = self.fog + strength * (self.target - self.fog)
        self.fog = np.clip(self.fog, 0, 1)
        
        self.frame_count += 1

    def save_frame(self, filename="silicon_tv_v4.png"):
        img = (self.fog * 255).astype(np.uint8)
        Image.fromarray(img, mode='L').save(filename)

# ==============================================================================
# SESSION CONTROLLER
# ==============================================================================

def run_v4_session():
    print("=" * 60)
    print("SILICON TV: V4 FOG DISSIPATION")
    print("=" * 60)
    
    # 1. Start Bridge in background
    bridge_dir = os.path.join(os.path.dirname(__file__), 'v4_drivers')
    bridge_path = os.path.join(bridge_dir, 's9_dual_bridge.py')
    print(f"[BOOT] Launching V4 Bridge: {bridge_path}")
    
    # Use subprocess with proper CWD to avoid path issues
    bridge_proc = subprocess.Popen([sys.executable, bridge_path], 
                                   cwd=bridge_dir,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
    time.sleep(10) # Wait for bridge to bind and S9 to connect
    
    engine = SiliconFogEngine(size=128)
    
    print("\n[READY] Engine initialized. Polling S9 via V4 API...")
    print("Press Ctrl+C to stop.\n")
    
    total_shares = 0
    start_time = time.time()
    
    try:
        while True:
            try:
                # Connect to Bridge API
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect(("127.0.0.1", 4000))
                
                # Request work (Send random noise payload)
                input_data = os.urandom(32).hex()
                t0 = time.perf_counter()
                
                sock.send((json.dumps({"data": input_data}) + "\n").encode())
                
                # Wait for Nonce (This is the blocking "Work" part)
                response = sock.recv(4096).decode()
                sock.close()
                
                if not response: continue
                
                result = json.loads(response)
                if "nonce" in result:
                    t1 = time.perf_counter()
                    delta_ms = (t1 - t0) * 1000
                    nonce = result["nonce"]
                    
                    # Dissipate Fog!
                    engine.dissipate(delta_ms, nonce)
                    total_shares += 1
                    
                    if total_shares % 10 == 0:
                        elapsed = time.time() - start_time
                        print(f"\r[SIGNAL] Shares: {total_shares} | Frames: {engine.frame_count} | Uptime: {elapsed:.1f}s", end="")
                        engine.save_frame()
                else:
                    print(f"\n[WARN] Bridge Error: {result.get('error')}")
                    time.sleep(1)
                    
            except Exception as e:
                # print(f"\n[RETRY] API Connection: {e}")
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        print("\n[STOP] Session ended by user.")
    finally:
        bridge_proc.terminate()
        print(f"\n[DONE] Total Frames: {engine.frame_count}")

if __name__ == "__main__":
    run_v4_session()
