#!/usr/bin/env python3
"""Upload dataset folder to Hugging Face Hub as a dataset repo.
Requires HF_TOKEN environment variable with write access.
"""
import os
import sys
from pathlib import Path

try:
    from huggingface_hub import HfApi, Repository
except Exception as e:
    print('huggingface_hub not installed. Install with `pip install huggingface_hub`')
    sys.exit(2)

HF_TOKEN = os.environ.get('HF_TOKEN')
if not HF_TOKEN:
    print('HF_TOKEN not found in environment. Exiting.')
    sys.exit(1)

USER = os.environ.get('HF_USER') or os.environ.get('GITHUB_ACTOR') or 'Agnuxo1'
REPO_NAME = f"{USER}/Secure_image_generation_with_ASIC_signature-dataset"

api = HfApi()
try:
    repo_url = api.create_repo(token=HF_TOKEN, name=REPO_NAME.split('/',1)[1], repo_type='dataset', private=False)
    print('Created dataset repo:', repo_url)
except Exception as e:
    print('Could not create repo (it may already exist):', e)

# Clone and push files
tmp = Path('.hf_tmp')
if tmp.exists():
    import shutil
    shutil.rmtree(tmp)

repo = Repository(local_dir=tmp, clone_from=REPO_NAME, use_auth_token=HF_TOKEN)

# Copy dataset folder
src = Path('dataset')
if not src.exists():
    print('No dataset folder found. Exiting.')
    sys.exit(1)

import shutil
shutil.copytree(src, tmp / 'dataset')

repo.git_add(patterns=['dataset/*'])
repo.git_commit('Add dataset files')
repo.git_push()
print('Uploaded dataset to HF:', REPO_NAME)
