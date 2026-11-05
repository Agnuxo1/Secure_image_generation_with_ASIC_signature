<!--
Project: Secure Image Generation with ASIC Signature
Author: Francisco Angulo de Lafuente
ORCID: https://orcid.org/0009-0001-1634-7063
Copyright: 2026 Francisco Angulo de Lafuente
Recorded on: 2026-11-05
License scope: Dataset is separately designated CC BY 4.0; media provenance and rights are not independently asserted here.
-->

Dataset included with this repository

**Documentation author:** [Francisco Angulo de Lafuente](https://orcid.org/0009-0001-1634-7063). This credit applies to this README, not to the underlying images or proof data.

Contents:
- `Originals/` — example input images used for embedding and testing.
- `proofs/` — processed images, comparison CSVs and example outputs used in the paper experiments.

License: Creative Commons Attribution 4.0 International (CC BY 4.0) — https://creativecommons.org/licenses/by/4.0/

This CC BY 4.0 notice is the repository's dataset designation; included-media sources and rights have not been independently verified.

Usage notes:
- The dataset is provided for benchmarking and reproducible experiments.
- Some files may be large; if you plan to publish the dataset separately (Zenodo, Figshare), we recommend uploading a packaged archive (`dataset.tar.gz`) and including checksums.

How to create a packaged dataset archive (example using the included script):

Windows PowerShell:
  `.	ools\package_dataset.ps1 -OutFile "./dataset.tar.gz"`

Linux / macOS (if present):
  `tar -czf dataset.tar.gz Originals proofs`

Please cite the repository and DOI (when available) if you use the dataset in publications.

**Citation and reuse:** Cite the project through CITATION.cff; see LICENSE and provenance.json for the applicable scope.
