#!/usr/bin/env python3
"""
S9 DUAL BRIDGE (V4 ADAPTER)
===========================
1. Acts as Stratum Pool for S9 (Port 3333)
2. Acts as API Server for V4 App (Port 4000)

Workflow:
App -> sends Image Block -> Bridge -> sends Mining Job -> S9 -> finds Nonce -> Bridge -> returns Hash -> App

Author: AntiGravity
"""

import socket
import threading
import json
import time
import binascii
import struct
import os
import queue

# CONFIG
STRATUM_PORT = 3333
API_PORT = 4000
DIFFICULTY = 4  # Ultra low difficulty for instant hashing
BLOCK_VERSION = "20000000"

class DualBridge:
    def __init__(self):
        self.running = True
        self.s9_conn = None
        self.job_counter = 0
        
        # Job Tracking
        # request_queue: (client_socket, data_hex)
        self.request_queue = queue.Queue()
        
        # pending_jobs: { "job_id": client_socket }
        self.pending_jobs = {}
        self.lock = threading.Lock()
        
    def start(self):
        # 1. Start Stratum Server (S9)
        t_stratum = threading.Thread(target=self.run_stratum_server)
        t_stratum.daemon = True
        t_stratum.start()
        
        # 2. Start API Server (App)
        t_api = threading.Thread(target=self.run_api_server)
        t_api.daemon = True
        t_api.start()
        
        print(f"[BRIDGE] READY. S9 Port: {STRATUM_PORT} | App Port: {API_PORT}")
        
        # Main Logic: Dispatcher
        while self.running:
            try:
                # Wait for request from App
                client, data_hex = self.request_queue.get(timeout=1)
                
                # If S9 not connected, fail immediately
                if not self.s9_conn:
                    print("[BRIDGE] Error: S9 Not Connected")
                    try:
                        client.send(json.dumps({"error": "S9 not connected"}).encode() + b"\n")
                        client.close()
                    except: pass
                    continue
                
                # Create Job
                self.job_counter += 1
                job_id = f"{self.job_counter:x}"
                
                # Store pending
                with self.lock:
                    self.pending_jobs[job_id] = client
                
                # Construct Stratum Job
                # PrevHash = Data (padded)
                prev_hash = data_hex[:64].ljust(64, '0')
                
                # Send to S9
                self.send_mining_notify(job_id, prev_hash)
                print(f"[BRIDGE] Job {job_id} dispatched to S9")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[BRIDGE] Loop Error: {e}")

    # ==========================================================
    # STRATUM SERVER (Handles S9)
    # ==========================================================
    def run_stratum_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", STRATUM_PORT))
        server.listen(1)
        print(f"[STRATUM] Listening on {STRATUM_PORT}...")
        
        while self.running:
            conn, addr = server.accept()
            print(f"[STRATUM] S9 Connected: {addr}")
            self.s9_conn = conn
            
            buffer = ""
            while True:
                try:
                    data = conn.recv(1024).decode()
                    if not data: break
                    buffer += data
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        self.handle_stratum_message(conn, line)
                except Exception as e:
                    print(f"[STRATUM] Disconnected: {e}")
                    break
            self.s9_conn = None
            print("[STRATUM] Waiting for reconnection...")

    def handle_stratum_message(self, conn, line):
        msg = json.loads(line)
        method = msg.get('method')
        msg_id = msg.get('id')
        
        if method == 'mining.subscribe':
            resp = {"id": msg_id, "result": [[["mining.notify", "ae6812eb4cd7735a302a8a9dd95cf71f"], "00000000", 4], "00000000", 4], "error": None}
            conn.send((json.dumps(resp)+"\n").encode())
            
        elif method == 'mining.authorize':
            resp = {"id": msg_id, "result": True, "error": None}
            conn.send((json.dumps(resp)+"\n").encode())
            
            # Send Initial Difficulty
            diff_msg = {"id": None, "method": "mining.set_difficulty", "params": [DIFFICULTY]}
            conn.send((json.dumps(diff_msg)+"\n").encode())
            print(f"[STRATUM] Authorized & Diff Set to {DIFFICULTY}")

        elif method == 'mining.submit':
            # Params: ["worker", "job_id", "extranonce2", "ntime", "nonce"]
            params = msg.get('params', [])
            job_id = params[1]
            nonce = params[4]
            
            # Send ACK to S9
            resp = {"id": msg_id, "result": True, "error": None}
            conn.send((json.dumps(resp)+"\n").encode())
            
            # Notify App
            print(f"[STRATUM] Share Found! Job: {job_id} Nonce: {nonce}")
            self.complete_job(job_id, nonce, params)

    def send_mining_notify(self, job_id, prev_hash):
        # Notify Params: [job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs]
        # prev_hash should be BE hex for Stratum? Actually usually LE in protocol but BE in display. 
        # S9 expects standard Stratum (LE of the BE display?).
        # For data hashing, we just want the bits to be there. 
        # We assume prev_hash is already the hex data we want the ASIC to crunch.
        
        # IMPORTANT: Stratum V1 expects `prevhash` as 32-byte hex.
        # We pass dummy coinbases.
        
        # BE/LE Swap logic might be needed if we care about specific byte order, 
        # but for "Unique Deterministic Hash", any order is fine as long as it's consistent.
        
        # NOTE: S9 needs specific coinbase length to not crash? 
        # In TPF collector we employed 32 byte coinbases.
        
        dummy_coin = "00"*32
        
        params = [
            job_id,
            prev_hash,
            dummy_coin, # coinb1
            dummy_coin, # coinb2
            [],         # merkle_branch
            BLOCK_VERSION,
            "1d00ffff", # nbits (Diff 1)
            f"{int(time.time()):x}", # ntime
            True        # clean_jobs = True to FORCE immediate switch
        ]
        
        msg = {"id": None, "method": "mining.notify", "params": params}
        try:
            self.s9_conn.send((json.dumps(msg)+"\n").encode())
        except:
             print("[STRATUM] Failed to send job")

    def complete_job(self, job_id, nonce, params):
        with self.lock:
            client = self.pending_jobs.pop(job_id, None)
        
        if client:
            try:
                result = {
                    "job_id": job_id,
                    "nonce": nonce,
                    "params": params,
                    "status": "success"
                }
                client.send((json.dumps(result) + "\n").encode())
                client.close() # Close after 1 Request/Response (Short-lived)
            except:
                pass

    # ==========================================================
    # API SERVER (Handles App)
    # ==========================================================
    def run_api_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", API_PORT))
        server.listen(5)
        print(f"[API] Listening for App requests on {API_PORT}...")
        
        while self.running:
            try:
                client, addr = server.accept()
                # Expecting: {"data": "hex"}
                data = client.recv(4096).decode().strip()
                if not data: 
                    client.close()
                    continue
                    
                req = json.loads(data)
                data_hex = req.get('data')
                
                if data_hex:
                    self.request_queue.put((client, data_hex))
                else:
                    client.close()
            except Exception as e:
                print(f"[API] Error: {e}")

if __name__ == "__main__":
    bridge = DualBridge()
    bridge.start()
