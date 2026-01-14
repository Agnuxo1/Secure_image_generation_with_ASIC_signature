#!/usr/bin/env python3
"""Upload benchmark results to Weights & Biases (W&B).
Requires WANDB_API_KEY environment variable to be set and `wandb` installed.
"""
import os
import json
import sys

try:
    import wandb
except Exception as e:
    print("wandb not installed. Install with `pip install wandb` to enable uploads.")
    sys.exit(2)

RESULTS = os.path.join(os.path.dirname(__file__), '..', 'benchmarks', 'results.json')
PROJECT = 'Secure_image_generation_with_ASIC_signature'
ENTITY = 'lareliquia-angulo'

if not os.path.exists(RESULTS):
    print('No results file found:', RESULTS)
    sys.exit(1)

with open(RESULTS) as f:
    data = json.load(f)

api_key = os.environ.get('WANDB_API_KEY')
if not api_key:
    print('WANDB_API_KEY not found in environment. Skipping upload.')
    sys.exit(0)

wandb.login(key=api_key)
run = wandb.init(project=PROJECT, entity=ENTITY, job_type='benchmark', config={'tool':'benchmarks/run_benchmarks.py'})

# Log summary metrics
runs = data.get('runs', [])
if runs:
    avg_embed = sum(r['embed_time_s'] for r in runs) / len(runs)
    avg_total = sum(r['total_time_s'] for r in runs) / len(runs)
    run.summary['avg_embed_time_s'] = avg_embed
    run.summary['avg_total_time_s'] = avg_total
    run.summary['num_runs'] = len(runs)

# Save results.json as an artifact
artifact = wandb.Artifact('benchmark-results', type='benchmark')
artifact.add_file(RESULTS)
run.log_artifact(artifact)

print('Uploaded benchmark results to W&B')
run.finish()
