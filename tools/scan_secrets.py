#!/usr/bin/env python3
"""Basic repository secrets scanner (heuristic).
Searches for high-entropy strings and common secret keywords in tracked files.
"""
import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

keywords = re.compile(r"(password|passwd|secret|token|api_key|apikey|ftp|aws_access_key|aws_secret|ssh-rsa|BEGIN\s+PRIVATE\s+KEY)", re.I)
hex_like = re.compile(r"[A-Fa-f0-9]{32,}")

matches = []
for p in ROOT.rglob('*'):
    if p.is_file() and '.git' not in p.parts:
        try:
            text = p.read_text(errors='ignore')
        except Exception:
            continue
        for m in keywords.finditer(text):
            matches.append((str(p), 'keyword', m.group(0).strip()))
        for m in hex_like.finditer(text):
            # Filter out long hashes that are expected (e.g., sha256 in code) by context
            snippet = text[max(0, m.start()-40):m.end()+40]
            if 'sha256' in snippet.lower() or 'hash' in snippet.lower() or 'nonce' in snippet.lower():
                continue
            matches.append((str(p), 'hex', m.group(0)))

if matches:
    print('Potential secrets found:')
    for f, kind, val in matches:
        print(f'- {kind} in {f}: {val[:64]}{"..." if len(val)>64 else ""}')
else:
    print('No obvious secrets detected by heuristics.')
