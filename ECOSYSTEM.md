# SiliconSignature Ecosystem

The complete SiliconSignature platform spans **9 repositories** covering every use case from research to production.

## 🗺️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     SILICONSIGNATURE ECOSYSTEM                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Python    │    │     Go      │    │    Rust     │        │
│  │   (Core)    │◄──►│    (CLI)    │◄──►│  (Library)  │        │
│  │  this repo  │    │   sf-go     │    │   sf-rust   │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              ▼                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │     TS      │    │   Android   │    │    PWA      │        │
│  │    (npm)    │    │   (Kotlin)  │    │  (Browser)  │        │
│  │   sf-ts     │    │  sf-android │    │   sf-web    │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              ▼                                  │
│  ┌─────────────┐    ┌─────────────┐                              │
│  │   ComfyUI   │    │    A1111    │                              │
│  │   (Node)    │    │  (Script)   │                              │
│  │ sf-comfyui  │    │  sf-a1111   │                              │
│  └─────────────┘    └─────────────┘                              │
│                                                                  │
│  ┌─────────────┐                                                 │
│  │   Browser   │                                                 │
│  │  Extension  │                                                 │
│  │ sf-browser  │                                                 │
│  └─────────────┘                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Repositories

### Core

| Repo | Language | Stars | Description |
|------|----------|-------|-------------|
| **[Secure_image_generation_with_ASIC_signature](https://github.com/Agnuxo1/Secure_image_generation_with_ASIC_signature)** | Python | — | 🏠 **This repo** — Original research, paper, Python implementation |

### Web & Mobile

| Repo | Language | URL | Description |
|------|----------|-----|-------------|
| **[siliconsignature-web](https://github.com/Agnuxo1/siliconsignature-web)** | HTML/CSS/JS | [silicon.p2pclaw.com](https://silicon.p2pclaw.com) | PWA — sign & verify in browser, zero install |
| **[silicon-android](https://github.com/Agnuxo1/silicon-android)** | Kotlin | — | Native Android camera app with real-time signing |
| **[silicon-browser-extension](https://github.com/Agnuxo1/silicon-browser-extension)** | JavaScript | — | Chrome/Firefox extension — right-click sign/verify |

### Libraries & CLI

| Repo | Language | Package | Description |
|------|----------|---------|-------------|
| **[siliconsignature-go](https://github.com/Agnuxo1/siliconsignature-go)** | Go | Binary | CLI tool + serverless function |
| **[siliconsignature-rust](https://github.com/Agnuxo1/siliconsignature-rust)** | Rust | Crate | Rust library + WASM bindings |
| **[siliconsignature-ts](https://github.com/Agnuxo1/siliconsignature-ts)** | TypeScript | npm | Browser + Node.js package |

### AI Image Generator Integrations

| Repo | Platform | Install | Description |
|------|----------|---------|-------------|
| **[silicon-comfyui-node](https://github.com/Agnuxo1/silicon-comfyui-node)** | ComfyUI | Custom node | One-click sign after generation |
| **[silicon-a1111-script](https://github.com/Agnuxo1/silicon-a1111-script)** | AUTOMATIC1111 | Script | Post-generation watermark |

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| **Live PWA** | https://silicon.p2pclaw.com |
| **Research Paper (PDF)** | [View in repo](https://github.com/Agnuxo1/Secure_image_generation_with_ASIC_signature/blob/main/Robust%20ASIC-Based%20Image%20Authentication%20Using%20Reed-Solomon%20LSB%20Watermarking.pdf) |
| **Author GitHub** | https://github.com/Agnuxo1 |
| **ResearchGate** | https://www.researchgate.net/profile/Francisco-Angulo-Lafuente-3 |

## 📊 Stats

- **Total Repositories:** 9
- **Languages:** Python, Go, Rust, TypeScript, Kotlin, HTML/CSS/JS
- **Platforms:** Web, Mobile, Desktop, CLI, Browser Extension, AI Generators
- **License:** MIT across all repos

---

*Part of the [P2PCLAW](https://www.p2pclaw.com) ecosystem.*
