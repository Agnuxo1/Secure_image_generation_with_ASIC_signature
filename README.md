# Secure Image Generation with ASIC Signature ✅

**Basado en:** Robust ASIC-Based Image Authentication Using Reed-Solomon LSB Watermarking: A Hardware-Bound Proof-of-Work Approach

**Autor:** Francisco Angulo de Lafuente — Independent Researcher, Spain

---

## 📋 Resumen (Abstract)

Este proyecto implementa un sistema de autenticación de imágenes que combina minería ASIC (Antminer S9, BM1387) con esteganografía LSB protegida por códigos de corrección de errores Reed–Solomon. El enfoque inserta firmas criptográficas derivadas de prueba-de-trabajo (PoW) directamente en los bits menos significativos de los píxeles y las protege mediante RS sobre GF(2^8). Los experimentos muestran que la marca puede sobrevivir entre un 30–40% de destrucción de píxeles y permitir la recuperación completa de la firma, equiparable al nivel H de corrección de QR.

**Palabras clave:** ASIC, Proof-of-Work, Autenticación de Imágenes, Reed–Solomon, LSB Steganography, SHA-256, Antminer S9, Firmas criptográficas, Corrección de errores.

---

## 🔎 Introducción

Las técnicas basadas en metadatos (EXIF, chunk de PNG) son triviales de eliminar. Este trabajo propone:

- **Firmas ligadas al hardware:** PoW generado por BM1387 (Antminer S9).
- **Inyección protegida por RS:** Embeber la firma en LSBs con códigos Reed–Solomon.
- **Redundancia por capas:** Repetición del payload para recuperación por votación.

### Contribuciones

- Arquitectura completa para autenticación con ASIC
- Implementación pura en Python de RS sobre GF(2^8)
- Motor LSB con redundancia configurable
- Validador experimental con tolerancia al daño 30–40%
- Código abierto listo para despliegue

---

## 🧠 Marco teórico

### Prueba-de-trabajo (PoW)

Se emplea la construcción de doble SHA-256 H(H(header || N)) < T para demostrar esfuerzo computacional (similar a minería Bitcoin). El ASIC BM1387 es determinista y produce nonces de PoW reproducibles vinculados al hash de la imagen.

### Reed–Solomon (RS)

Códigos RS(n,k) sobre GF(256) con el polinomio primitivo:

`p(x) = x^8 + x^4 + x^3 + x^2 + 1 (0x11D)`

RS permite corregir hasta t errores por código usando n-k = 2t símbolos de paridad.

### LSB Steganography

Se usa el bit menos significativo de cada canal (8 bits por canal) para almacenar datos. La modificación es imperceptible al ojo humano.

---

## 🏗️ Arquitectura del sistema

El pipeline consta de cuatro componentes principales:

1. **Image Hasher:** hash SHA-256 de los datos de píxeles.
2. **ASIC Bridge:** comunica con Antminer S9 vía protocolo Stratum (prevhash para trabajos).
3. **RS Encoder:** aplica RS sobre el payload (GF(2^8)).
4. **LSB Embedder:** inserta la firma protegida y repetida en los LSBs.

Figura conceptual: Image SHA-256 → ASIC Bridge (BM1387 PoW) → RS Encoder → LSB Embed (xN repeticiones) → Output

---

## 📑 Estructura de la firma (Signature Payload)

| Campo    | Tamaño | Descripción |
|---------:|:------:|:------------|
| hash     | 64 bytes | SHA-256 (hex) de los píxeles |
| nonce    | 8 bytes  | Nonce válido descubierto por el ASIC |
| ntime    | 8 bytes  | Timestamp de la operación |
| version  | 8 bytes  | Versión de bloque (p.ej. 0x20000000) |
| status   | ~24 bytes | Cadena de estado de autenticación |

---

## ⚙️ Parámetros de implementación

| Parámetro | Valor | Razonamiento |
|:---------:|:-----:|:-------------|
| RS_NSYM   | 32    | Compromiso entre redundancia y tamaño |
| SIGNATURE_REPEATS | 5 | Votación para recuperación robusta |
| Payload típico | ~170 bytes | JSON con firma y metadatos |

**Capacidad:** Para una imagen W×H con 3 canales, capacidad = W×H×3 bits. Ej.: 1280×720 → 2,764,800 bits. El payload (~8200 bits con RS y repetición) ocupa ~0.3%.

---

## 📊 Resultados experimentales

### Rendimiento de embedding

| Imagen | Resolución | Payload | Capacidad usada | Tiempo |
|:------:|:----------:|:-------:|:---------------:|:------:|
| Imagen_test10.jpg | 494×493 | 8,200 bits | 1.12% | 0.3s |
| silicon_tv_v4.png | 1280×720 | 8,200 bits | 0.30% | 0.8s |
| test_4k.png       | 3840×2160| 8,200 bits | 0.03% | 2.1s |

### Tolerancia a daño (tests de vandalismo)

| Nivel de daño | Copias recuperadas | Estado firma |
|:-------------:|:------------------:|:------------:|
| 0% (Control)   | 5/5 | VERIFIED |
| 10% (Leve)     | 5/5 | VERIFIED |
| 20% (Moderado) | 4/5 | VERIFIED |
| 30% (Severo)   | 3/5 | VERIFIED |
| 40% (Extremo)  | 2/5 | VERIFIED |
| 50% (Crítico)  | 1/5 | MARGINAL |

---

## 🛠️ Especificaciones de hardware

**Antminer S9 (BM1387)**

| Especificación | Valor |
|:--------------:|:-----:|
| Modelo | Antminer S9 |
| Chip ASIC | BM1387 |
| Conteo de chips | 189 |
| Hashrate agregado | 14.0 TH/s |
| Consumo | 1,400W |
| Eficiencia | ~10B H/J |

Comparación: CPU Intel i7-10700K ≈ 21,000 H/J → ASIC ≈ 533,000× más eficiente para PoW.

---

## 🔐 Análisis de seguridad

- **Resistencia a falsificación:** Forjar la firma exige realizar la PoW (requiere los ASICs).
- **Vectores de ataque y mitigación:**

| Ataque | Mitigación | Efectividad |
|:------:|:----------:|:-----------:|
| Eliminación de metadatos | LSB embedding | Sobrevive |
| Edición visual agresiva | RS + redundancia | Hasta 40% (recuperación comprobada) |
| Falsificación de firma | PoW atado al hardware | Computacionalmente inviable |

**Limitaciones:** JPEG y compresión con pérdida destruyen LSB. Redimensionado invalida la marca. Requiere hardware específico (opción: modo software simulado para pruebas).

---

## 🔭 Trabajos futuros

- Extender soporte para Extranonce2 para verificación PoW completa sin metadatos
- Implementar decodificador de Berlekamp–Massey para mejorar corrección
- Soporte para autenticación de frames de vídeo
- App móvil para verificación in-situ

---

## 🧪 Cómo usar (uso básico)

Ejecutar los scripts de este repositorio con Python 3 (`python`):

- **Generar firma y embeber:** `python silicon_signature_engine.py <imagen>`
- **Verificar firma:** `python verify_silicon_art.py <imagen>`
- **Simular daño y recuperación:** `python simulate_damage.py <imagen>`
- **Herramientas auxiliares:** `manuaI_png_check.py`, `silicon_rs_watermark.py`, `asic_auth_portal.py`

(Consulte el código fuente para opciones y parámetros detallados.)

---

## 📚 Referencias

Se incluyen las referencias citadas en el artículo original; entre ellas: Katzenbeisser & Petitcolas (2000), Nakamoto (2008), Reed & Solomon (1960), NIST FIPS 180-4, y documentación de Bitmain (Antminer S9).

---

## 🧑‍💻 Autor y contacto

Francisco Angulo de Lafuente — Researcher

- GitHub: https://github.com/Agnuxo1
- ResearchGate: https://www.researchgate.net/profile/Francisco-Angulo-Lafuente-3
- Kaggle: https://www.kaggle.com/franciscoangulo
- HuggingFace: https://huggingface.co/Agnuxo
- Wikipedia: https://es.wikipedia.org/wiki/Francisco_Angulo_de_Lafuente

---

## 📝 Licencia

Proyecto abierto — consulte el repositorio para la licencia específica (si desea, puedo añadir un `LICENSE`).

---

Si desea, puedo: añadir un `.gitignore` adecuado y remover `__pycache__` del historial o limpiar archivos grandes antes de continuar. ✨
