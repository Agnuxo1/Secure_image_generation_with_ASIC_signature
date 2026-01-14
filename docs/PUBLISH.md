Publishing and archiving guide

This document explains how to publish code, paper and dataset artifacts to several platforms.

1) Zenodo (GitHub integration)
 - Connect your GitHub account to Zenodo and enable the repository.
 - Create a GitHub Release (we created `v1.0.0`); Zenodo will automatically archive the release and mint a DOI.
 - Include `zenodo.json` metadata and `RELEASE_NOTES.md` in your release for better metadata.

2) Weights & Biases (W&B)
 - Create a W&B project (e.g., `lareliquia-angulo/Secure_image_generation_with_ASIC_signature`).
 - Add `WANDB_API_KEY` to your GitHub repository secrets to allow CI uploads.
 - Use the `benchmarks/run_benchmarks.py` and `tools/upload_to_wandb.py` to run and upload benchmark results.

3) Hugging Face Datasets
 - Create a new dataset repo (https://huggingface.co/datasets) and push the dataset files or connect to GitHub.
 - Include dataset metadata and `dataset/README.md`. Use CC-BY 4.0 for data.

4) Figshare / OSF / DataHub / OpenML
 - Prepare dataset archive (`tools/package_dataset.ps1`) and checksums.
 - Use the platform web UI or APIs to upload the archive, provide metadata and license (CC-BY 4.0 recommended).

5) DrivenData / Signate / Zindi
 - If you want to run a public challenge, contact the platform and prepare train/validation/test split and clear rules.
 - Provide a starter kit in `examples/` and specify evaluation metrics.

6) Security and permissions
 - Never commit API keys or passwords to the repository. Use GitHub Secrets.
 - If you accidentally committed secrets, **revoke/regenerate them immediately** and consider history rewrite (BFG or `git filter-repo`).

7) Licensing recommendations
 - Code: MIT or Apache-2.0 (we used MIT by default).
 - Data: CC-BY 4.0.
 - Paper: CC-BY preferred for open access.

If you want, I can perform the uploads on your behalf (I will need API tokens) or prepare CI to do automated uploads. Let me know which platforms to prioritize and whether you prefer manual approvals before uploads.
