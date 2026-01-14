Dataset included with this repository

Contents:
- `Originals/` — example input images used for embedding and testing.
- `proofs/` — processed images, comparison CSVs and example outputs used in the paper experiments.

License: Creative Commons Attribution 4.0 (CC-BY 4.0)

Usage notes:
- The dataset is provided for benchmarking and reproducible experiments.
- Some files may be large; if you plan to publish the dataset separately (Zenodo, Figshare), we recommend uploading a packaged archive (`dataset.tar.gz`) and including checksums.

How to create a packaged dataset archive (example using the included script):

Windows PowerShell:
  `.	ools\package_dataset.ps1 -OutFile "./dataset.tar.gz"`

Linux / macOS (if present):
  `tar -czf dataset.tar.gz Originals proofs`

Please cite the repository and DOI (when available) if you use the dataset in publications.
