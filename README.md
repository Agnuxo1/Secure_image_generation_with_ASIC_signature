# Secure Image Generation with ASIC Signature ✅

**Based on:** Robust ASIC-Based Image Authentication Using Reed–Solomon LSB Watermarking: A Hardware-Bound Proof-of-Work Approach

**Author:** Francisco Angulo de Lafuente — Independent Researcher, Spain

---

## 📋 Abstract

This project implements an image authentication system that combines ASIC-based proof-of-work (Antminer S9, BM1387) with LSB steganography protected by Reed–Solomon error-correcting codes. Signatures derived from deterministic PoW are embedded directly into pixel least-significant bits (LSBs) and protected using RS over GF(2^8). Experimental results show the watermark survives approximately 30–40% pixel destruction and still allows full signature recovery, comparable to QR Code Level H error correction.

**Keywords:** ASIC, Proof-of-Work, Image Authentication, Reed–Solomon, LSB Steganography, SHA-256, Antminer S9, Cryptographic Signatures, Error Correction

---

## 🔎 Introduction

Image authentication methods based on metadata (EXIF or PNG text chunks) are easily stripped by ordinary image processing tools. This work proposes a different approach that resists both metadata stripping and large-scale visual modification by combining:

- **Hardware-bound signatures:** PoW produced by the BM1387 ASIC (Antminer S9).
- **Reed–Solomon protected embedding:** RS codes over GF(256) applied to the signature payload.
- **Multi-layer redundancy:** Repetition of the encoded signature across the image to enable voting-based recovery.

### Contributions

- Complete system architecture for ASIC-based image authentication.
- Pure-Python Reed–Solomon encoder/decoder over GF(2^8).
- LSB steganography engine with configurable redundancy.
- Validation framework demonstrating 30–40% damage tolerance.
- Open-source implementation ready for deployment.

---

## 🧠 Theoretical Background

### Proof-of-Work (PoW)

A PoW requires finding an input that produces a hash below a target: the system uses a double SHA-256 construction H(H(header || N)) < T (as in Bitcoin). The BM1387 ASIC deterministically produces valid nonces that prove significant hashing work.

### Reed–Solomon (RS)

Reed–Solomon codes RS(n,k) operate over GF(256) using the primitive polynomial:

`p(x) = x^8 + x^4 + x^3 + x^2 + 1 (0x11D)`

With n-k = 2t parity symbols, RS can correct up to t symbol errors.

### LSB Steganography

LSB embedding modifies the least significant bit of pixel color channels to store payload bits. Changes are per-channel ±1 at most and are visually imperceptible.

---

## 🏗️ System Architecture

The pipeline consists of four components:

1. **Image Hasher:** produces a SHA-256 hash of raw pixel bytes.
2. **ASIC Bridge:** submits the image hash as `prevhash` to a Stratum job; returns an ASIC-discovered valid nonce.
3. **RS Encoder:** encodes the signature payload using Reed–Solomon over GF(2^8).
4. **LSB Embedder:** writes the encoded, repeated signature into LSBs across the image channels.

Diagram: Image SHA-256 → ASIC Bridge (BM1387 PoW) → RS Encoder → LSB Embedder (×repeats) → Output

---

## 📑 Signature Payload

| Field   | Size     | Description |
|:-------:|:--------:|:------------|
| hash    | 64 bytes | SHA-256 hex digest of pixel data |
| nonce   | 8 bytes  | ASIC-discovered valid nonce |
| ntime   | 8 bytes  | Timestamp of mining operation |
| version | 8 bytes  | Block version (e.g., 0x20000000) |
| status  | ~24 bytes| Authentication status string |

---

## ⚙️ Implementation Details

- **Pure Python Reed–Solomon:** GF(2^8) arithmetic using primitive polynomial 0x11D; log/antilog tables; generator polynomial generation for NS=32 parity symbols; RS(n, n-32) configuration.
- **Embedding parameters:** typical payload ≈ 170 bytes (JSON), RS parity 32 symbols, and `SIGNATURE_REPEATS` = 5.

**Capacity analysis:** For an image W×H with 3 channels, available LSB capacity = W×H×3 bits. Example: 1280×720 → 2,764,800 bits; our ~8,200-bit payload uses ~0.3%.

---

## 📊 Experimental Results

### Embedding Performance

| Image | Resolution | Payload | Capacity used | Time |
|:-----:|:----------:|:-------:|:-------------:|:----:|
| Imagen_test10.jpg | 494×493 | 8,200 bits | 1.12% | 0.3s |
| silicon_tv_v4.png | 1280×720 | 8,200 bits | 0.30% | 0.8s |
| test_4k.png       | 3840×2160| 8,200 bits | 0.03% | 2.1s |

### Damage Tolerance (Vandalism Tests)

| Damage level | Copies recovered | Signature status |
|:------------:|:----------------:|:----------------:|
| 0% (Control)   | 5/5 | VERIFIED |
| 10% (Minor)    | 5/5 | VERIFIED |
| 20% (Moderate) | 4/5 | VERIFIED |
| 30% (Severe)   | 3/5 | VERIFIED |
| 40% (Extreme)  | 2/5 | VERIFIED |
| 50% (Critical) | 1/5 | MARGINAL |

A painted-shapes attack removing ~20% of pixels still allowed full signature recovery using RS and multi-copy voting.

---

## 🛠️ Hardware Specifications

**Antminer S9 (BM1387)**

| Spec | Value |
|:----:|:-----:|
| Model | Antminer S9 |
| ASIC chip | BM1387 |
| Chip count | 189 |
| Hashrate (aggregate) | 14.0 TH/s |
| Power | 1,400 W |
| Efficiency | ~10B hashes/J |

**Comparison:** Intel i7-10700K ≈ 21,000 hashes/J → ASIC ≈ 533,000× more efficient for PoW.

---

## 🔐 Security Analysis

**Forgery resistance:** An attacker must either perform the PoW (requires ASIC hardware) or preserve enough LSB data despite RS limits. Reconstruction from partial data is prevented by RS syndromes.

| Attack | Mitigation | Effectiveness |
|:------:|:----------:|:-------------:|
| Metadata stripping | LSB embedding | Survives |
| Aggressive visual edits | RS + redundancy | Up to 40% recovery |
| Signature forgery | Hardware-bound PoW | Computationally infeasible |
| LSB destruction | 5× redundancy | Survives partial destruction |

**Limitations:** JPEG lossy compression and resizing destroy embedded LSB payloads; ASIC dependence (software-only simulation mode could be added for testing).

---

## 🔭 Limitations & Future Work

- Support Extranonce2 embedding for full PoW verification without metadata.
- Implement a full Berlekamp–Massey decoder to improve error correction.
- Add support for video frame authentication and a mobile verification app.
- Provide a software-mode for systems without ASIC hardware.

---

## 🧪 Usage (Quick Start)

Run the repository scripts with Python 3:

- Embed signature: `python silicon_signature_engine.py <image>`
- Verify signature: `python verify_silicon_art.py <image>`
- Simulate damage & recovery: `python simulate_damage.py <image>`
- Utilities: `manual_png_check.py`, `silicon_rs_watermark.py`, `asic_auth_portal.py`

See source code for CLI options and configuration parameters.

---

## 📚 References

Selected references from the original manuscript (not exhaustive):
- Katzenbeisser & Petitcolas, Information Hiding Techniques for Steganography and Digital Watermarking, 2000.
- Nakamoto, Bitcoin: A Peer-to-Peer Electronic Cash System, 2008.
- Reed & Solomon, Polynomial Codes Over Certain Finite Fields, 1960.
- NIST FIPS 180-4: Secure Hash Standard.
- Bitmain Antminer S9 documentation.

---

## 🧑‍💻 Author & Contact

Francisco Angulo de Lafuente — Independent Researcher

- GitHub: https://github.com/Agnuxo1
- ResearchGate: https://www.researchgate.net/profile/Francisco-Angulo-Lafuente-3
- Kaggle: https://www.kaggle.com/franciscoangulo
- Hugging Face: https://huggingface.co/Agnuxo

---

## 📝 License

Open-source project — add or specify a `LICENSE` file to indicate the desired license.

---

If you want, I can also add a robust `.gitignore`, remove `__pycache__` entries from history, or remove large files before pushing a cleaned history. ✨
