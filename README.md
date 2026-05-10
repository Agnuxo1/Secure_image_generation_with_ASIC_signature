# <div align="center">🔏 SiliconSignature</div>

<div align="center">

**Hardware-Bound Image Authentication for the AI Era**

*Prove image provenance with ASIC proof-of-work and Reed-Solomon watermarking*

[![License: MIT](https://img.shields.io/badge/License-MIT-00ff88.svg?style=for-the-badge)](LICENSE)
[![Paper](https://img.shields.io/badge/Paper-PDF-ff6b6b.svg?style=for-the-badge)](./Robust%20ASIC-Based%20Image%20Authentication%20Using%20Reed-Solomon%20LSB%20Watermarking.pdf)
[![Web](https://img.shields.io/badge/Web-Live-ff6b6b.svg?style=for-the-badge)](https://silicon.p2pclaw.com)
[![PWA](https://img.shields.io/badge/PWA-Installable-00ccff.svg?style=for-the-badge)](https://silicon.p2pclaw.com)

[![Go](https://img.shields.io/badge/Go-CLI-00ADD8.svg?style=flat-square&logo=go)](https://github.com/Agnuxo1/siliconsignature-go)
[![Rust](https://img.shields.io/badge/Rust-Library-000000.svg?style=flat-square&logo=rust)](https://github.com/Agnuxo1/siliconsignature-rust)
[![TypeScript](https://img.shields.io/badge/TypeScript-npm-3178C6.svg?style=flat-square&logo=typescript)](https://github.com/Agnuxo1/siliconsignature-ts)
[![Android](https://img.shields.io/badge/Android-APK-3DDC84.svg?style=flat-square&logo=android)](https://github.com/Agnuxo1/silicon-android)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Node-1f6feb.svg?style=flat-square&logo=comfyui)](https://github.com/Agnuxo1/silicon-comfyui-node)
[![A1111](https://img.shields.io/badge/A1111-Script-ff9d00.svg?style=flat-square&logo=stable-diffusion)](https://github.com/Agnuxo1/silicon-a1111-script)
[![Browser](https://img.shields.io/badge/Browser-Extension-4285F4.svg?style=flat-square&logo=google-chrome)](https://github.com/Agnuxo1/silicon-browser-extension)

</div>

---

## 🚨 The Problem

| Threat | Current Solutions | Why They Fail |
|--------|----------------|---------------|
| **Deepfakes** | Detection algorithms | Reactive — find fakes *after* creation |
| **Image forgery** | EXIF metadata | Stripped in 1 click |
| **AI watermarking** | C2PA, SynthID | Trusts corporations; removable |
| **NFT provenance** | Blockchain tokens | Just a URL, not the image |

**SiliconSignature is different.** We embed **unforgeable proof-of-work** directly into the image pixels — bound to a physical ASIC chip. No corporation to trust. No metadata to strip. No blockchain needed.

---

## ⚡ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    SIGN AN IMAGE                              │
│                                                               │
│   1. SHA-256 hash of image bytes                              │
│   2. Search for nonce via ASIC proof-of-work                 │
│   3. Reed-Solomon ECC encodes (hash + nonce + metadata)       │
│   4. Embed in LSB of RGB channels (offset 0x20)               │
│   5. Magic header "SSv1" + 5× redundancy                      │
│                                                               │
│   Result: Image looks identical. But pixels carry proof.      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   VERIFY AN IMAGE                             │
│                                                               │
│   1. Extract LSB from RGB channels                            │
│   2. Decode Reed-Solomon (tolerates 40% pixel loss)           │
│   3. Validate nonce via SHA-256 check                         │
│   4. Confirm ASIC work was performed                            │
│                                                               │
│   Result: Authentic or Tampered. Binary. No grey area.       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Compared to Alternatives

| | **SiliconSignature** | **C2PA (Adobe)** | **SynthID (Google)** | **NFT** |
|---|:---:|:---:|:---:|:---:|
| **Open Source** | ✅ MIT | ❌ Corporate | ❌ Corporate | Varies |
| **No Dependencies** | ✅ Pure code | ❌ Ecosystem | ❌ API | ❌ Blockchain |
| **Survives editing** | ✅ 40% pixels | ⚠️ Metadata only | ⚠️ Compression | ❌ None |
| **Hardware-bound** | ✅ ASIC PoW | ❌ No | ❌ No | ❌ No |
| **Cost to forge** | **$10,000+** | $0 (strip metadata) | $0 (remove sig) | $0 (screenshot) |
| **Verification** | ✅ Offline | ❌ Needs Adobe | ❌ Needs Google | ❌ Needs blockchain |

---

## 🏗️ Ecosystem

This repository is the **central hub** — the original Python implementation + research paper. The ecosystem extends across 8 specialized repositories:

| Component | Language | Repository | Description |
|-----------|----------|------------|-------------|
| **PWA** | HTML/JS | [siliconsignature-web](https://github.com/Agnuxo1/siliconsignature-web) | Browser-based sign & verify |
| **CLI** | Go | [siliconsignature-go](https://github.com/Agnuxo1/siliconsignature-go) | Command-line tool + serverless |
| **Library** | Rust | [siliconsignature-rust](https://github.com/Agnuxo1/siliconsignature-rust) | Rust + WASM bindings |
| **Package** | TypeScript | [siliconsignature-ts](https://github.com/Agnuxo1/siliconsignature-ts) | npm package for Node/Browser |
| **Mobile** | Kotlin | [silicon-android](https://github.com/Agnuxo1/silicon-android) | Android camera app |
| **ComfyUI** | Python | [silicon-comfyui-node](https://github.com/Agnuxo1/silicon-comfyui-node) | Custom node for ComfyUI |
| **A1111** | Python | [silicon-a1111-script](https://github.com/Agnuxo1/silicon-a1111-script) | Script for AUTOMATIC1111 |
| **Browser** | JS | [silicon-browser-extension](https://github.com/Agnuxo1/silicon-browser-extension) | Chrome/Firefox extension |

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
- Multi-platform ecosystem (PWA, CLI, Libraries, Mobile, Browser extensions).

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

**Diagram:** Image SHA-256 → ASIC Bridge (BM1387 PoW) → RS Encoder → LSB Embedder (×repeats) → Output

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

**Limitations:** JPEG lossy compression and resizing destroy embedded LSB payloads; ASIC dependence (software-only simulation mode available in the [PWA](https://silicon.p2pclaw.com)).

---

## 🔭 Limitations & Future Work

- Support Extranonce2 embedding for full PoW verification without metadata.
- Implement a full Berlekamp–Massey decoder to improve error correction.
- Add support for video frame authentication.
- Expand mobile verification via the [Android app](https://github.com/Agnuxo1/silicon-android).
- Integrate with popular image generators (ComfyUI, A1111, Fooocus, InvokeAI).

---

## 🧪 Usage (Quick Start)

Run the repository scripts with Python 3:

- **Embed signature:** `python silicon_signature_engine.py <image>`
- **Verify signature:** `python verify_silicon_art.py <image>`
- **Simulate damage & recovery:** `python simulate_damage.py <image>`
- **Utilities:** `manual_png_check.py`, `silicon_rs_watermark.py`, `asic_auth_portal.py`

For browser-based signing (no Python/ASIC required), use the **[Live PWA](https://silicon.p2pclaw.com)**.

---

## 📁 Repository Contents

```
Secure_image_generation_with_ASIC_signature/
├── asic_auth_portal.py              # ASIC authentication portal
├── silicon_signature_engine.py      # Core signing engine
├── verify_silicon_art.py            # Verification tool
├── silicon_rs_watermark.py          # Reed-Solomon watermark module
├── silicon_fog_analyzer.py          # Fog/lighting analyzer
├── silicon_fog_v4_session.py        # Session management
├── simulate_damage.py               # Damage simulation tests
├── manual_png_check.py              # PNG validation utility
├── Robust ASIC-Based Image          # Full research paper (PDF)
│   Authentication Using
│   Reed-Solomon LSB Watermarking.pdf
├── ASIC_Signature_Paper.html        # HTML version of paper
├── Secure_image_generation_with     # Interactive HTML demo
│   ASIC_signature.html
├── benchmarks/                      # Performance benchmarks
├── dataset/                         # Test image datasets
├── docs/                            # Documentation
├── drivers/                         # ASIC drivers
├── Originals/                       # Original test images
├── proofs/                          # Verification proofs
├── tools/                           # Additional tools
├── .github/workflows/               # CI/CD workflows
├── CITATION.cff                     # Citation metadata
├── LICENSE                          # MIT License
├── SECURITY.md                      # Security policy
├── zenodo.json                      # Zenodo metadata
└── README.md                        # This file
```

---

## 📚 References

Selected references from the original manuscript:
- Katzenbeisser & Petitcolas, Information Hiding Techniques for Steganography and Digital Watermarking, 2000.
- Nakamoto, Bitcoin: A Peer-to-Peer Electronic Cash System, 2008.
- Reed & Solomon, Polynomial Codes Over Certain Finite Fields, 1960.
- NIST FIPS 180-4: Secure Hash Standard.
- Bitmain Antminer S9 documentation.

---

## 🧑‍💻 Author & Contact

**Francisco Angulo de Lafuente** — Independent Researcher, Spain

- GitHub: https://github.com/Agnuxo1
- ResearchGate: https://www.researchgate.net/profile/Francisco-Angulo-Lafuente-3
- Kaggle: https://www.kaggle.com/franciscoangulo
- Hugging Face: https://huggingface.co/Agnuxo
- ORCID: 0009-0001-1634-7063

---

## 📖 How to Cite

Please use the `CITATION.cff` file in this repository or cite as:

> Francisco Angulo de Lafuente (2026). *Secure Image Generation with ASIC Signature*. GitHub repository, v1.0.0. https://github.com/Agnuxo1/Secure_image_generation_with_ASIC_signature

---

## 📝 License

[MIT License](LICENSE) © 2026 Francisco Angulo de Lafuente

---

<div align="center">

**[🌐 Live PWA](https://silicon.p2pclaw.com) · [📄 Paper](https://github.com/Agnuxo1/Secure_image_generation_with_ASIC_signature/blob/main/Robust%20ASIC-Based%20Image%20Authentication%20Using%20Reed-Solomon%20LSB%20Watermarking.pdf) · [🐛 Issues](https://github.com/Agnuxo1/Secure_image_generation_with_ASIC_signature/issues)**

</div>
