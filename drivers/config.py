"""
Configuration for ASIC-CNN Hybrid Benchmark

Author: Francisco Angulo de Lafuente
GitHub: https://github.com/Agnuxo1
"""

import os
from pathlib import Path

# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
MODELS_DIR = RESULTS_DIR / "models"
FIGURES_DIR = RESULTS_DIR / "figures"
METRICS_DIR = RESULTS_DIR / "metrics"

# Create directories
for d in [DATA_DIR, RESULTS_DIR, MODELS_DIR, FIGURES_DIR, METRICS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# =============================================================================
# DATASET CONFIGURATION
# =============================================================================

DATASET_CONFIG = {
    # Kaggle dataset identifier
    'kaggle_dataset': 'paultimothymooney/chest-xray-pneumonia',
    
    # Alternative: direct download URL (backup)
    'backup_url': 'https://data.mendeley.com/datasets/rscbjbr9sj/2',
    
    # Number of samples to use (per class)
    'samples_per_class': 250,  # Total 500 images
    
    # Train/Val/Test split
    'train_ratio': 0.8,
    'val_ratio': 0.1,
    'test_ratio': 0.1,
    
    # Image parameters
    'image_size': 384,        # Increased for "Hybrid Max" (V4)
    'channels': 1,  # Grayscale
    
    # Classes
    'classes': ['NORMAL', 'PNEUMONIA'],
    'num_classes': 2
}

# =============================================================================
# ASIC CONFIGURATION (LV06)
# =============================================================================

ASIC_CONFIG = {
    # Enable/disable hardware ASIC
    # Set to False to use software SHA-256 only
    'enabled': True,  # Enabled for S9 V4 Port
    
    # S9 Bridge Settings
    # NOTE: The App connects to the Local Bridge (s9_dual_bridge.py)
    # The Bridge Address is Hardcoded to 127.0.0.1:4000 in asic_interface.py
    'host': '127.0.0.1',  
    'port': 4000,         
    'stratum_port': 3333,
    'reboot_endpoint': '/api/system/reboot', # Reboot endpoint
    
    # Connection settings
    'timeout': 10,            # seconds
    'retry_count': 3,
    'retry_delay': 1,         # seconds
    
    # Hash generation settings
    'block_size': 8,          # pixels per hash block
    'difficulty': 1e-9,       # Adjusted for LV06 (~1e-9 standard for single shares)
    
    # Verification settings (Cleanroom V10)
    'strict_verification': True, # Verify every share against target
    'check_version_rolling': True, # Check for Overt ASIC Boost (version rolling)
    'require_valid_pow': True, # Reject invalid Proof-of-Work
    
    # Fallback behavior
    'fallback_to_software': True,  # Use software if ASIC fails (logs warning)
    
    # Caching
    'cache_attention_maps': True,
    'cache_dir': RESULTS_DIR / "attention_cache"
}

# Create cache directory
if ASIC_CONFIG['cache_attention_maps']:
    ASIC_CONFIG['cache_dir'].mkdir(parents=True, exist_ok=True)

# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

MODEL_CONFIG = {
    # Backbone architecture
    'backbone': 'resnet101',  # Final Boss (V4 Hybrid Max)
    
    # Pretrained weights
    'pretrained': True,
    
    # Feature dimensions (ResNet-50/101)
    'feature_dim': 2048,      
    'hidden_dim': 1024,       # Increased for deeper features
    
    # Dropout
    'dropout': 0.3,           # Reduced for higher capacity learning
    
    # Attention settings (for hybrid models)
    'attention_scales': [1, 2, 4],  # Multi-scale attention
    'attention_reduction': 'mean',   # How to reduce attention: mean, max, weighted
    
    # Models to train (V4 focuses exclusively on Hybrid Multi)
    'models': {
        'hybrid_multi': {
            'description': 'ASIC-Enhanced Hybrid Multi-Scale (V4 Max Level)',
            'use_asic_attention': True,
            'attention_injection': 'pyramid'
        }
    }
}

# =============================================================================
# TRAINING CONFIGURATION
# =============================================================================

TRAINING_CONFIG = {
    # Basic hyperparameters
    'batch_size': 16,
    'num_epochs': 75,         # Increased for V4
    'learning_rate': 1e-4,
    'weight_decay': 5e-4,     # Increased for AdamW
    
    # Optimizer
    'optimizer': 'adamw',     # Upgraded for V4
    
    # Learning rate scheduler
    'scheduler': 'reduce_on_plateau',
    'scheduler_patience': 5,
    'scheduler_factor': 0.5,
    
    # Early stopping
    'early_stopping': True,
    'early_stopping_patience': 10,
    'early_stopping_min_delta': 0.001,
    
    # Loss function
    'loss': 'cross_entropy',
    'class_weights': None,  # Set to 'balanced' for imbalanced data
    
    # Attention loss (for hybrid models)
    'attention_loss_weight': 0.1,  # Lambda for attention consistency
    
    # Device
    'device': 'auto',  # Options: auto, cuda, cpu
    
    # Reproducibility
    'seed': 42,
    
    # Checkpointing
    'save_best_only': True,
    'save_frequency': 5  # Save every N epochs
}

# =============================================================================
# AUGMENTATION CONFIGURATION
# =============================================================================

AUGMENTATION_CONFIG = {
    'train': {
        'resize': 256,
        'crop_size': 224,
        'horizontal_flip': 0.5,
        'vertical_flip': 0.0,  # Medical images shouldn't be flipped vertically
        'rotation': 10,        # degrees
        'brightness': 0.1,
        'contrast': 0.1,
        'normalize_mean': [0.485],
        'normalize_std': [0.229]
    },
    'val': {
        'resize': 256,
        'crop_size': 224,
        'normalize_mean': [0.485],
        'normalize_std': [0.229]
    },
    'test': {
        'resize': 256,
        'crop_size': 224,
        'normalize_mean': [0.485],
        'normalize_std': [0.229]
    }
}

# =============================================================================
# BENCHMARK CONFIGURATION
# =============================================================================

BENCHMARK_CONFIG = {
    # Metrics to compute
    'metrics': [
        'accuracy',
        'sensitivity',  # Recall for positive class
        'specificity',  # Recall for negative class
        'precision',
        'f1_score',
        'auc_roc',
        'confusion_matrix'
    ],
    
    # Number of runs for statistical significance
    'num_runs': 3,
    
    # Confidence interval
    'confidence_level': 0.95,
    
    # Inference timing
    'measure_inference_time': True,
    'warmup_iterations': 10,
    'timing_iterations': 100,
    
    # Attention visualization
    'visualize_attention': True,
    'num_attention_samples': 20,
    
    # ASIC validation
    'validate_with_asic': True,  # Run final validation with real ASIC
    'asic_validation_samples': 50
}

# =============================================================================
# VISUALIZATION CONFIGURATION
# =============================================================================

VISUALIZATION_CONFIG = {
    # Figure settings
    'figure_dpi': 150,
    'figure_format': 'png',
    
    # Color scheme
    'colors': {
        'standard_cnn': '#1f77b4',
        'hybrid_single': '#ff7f0e',
        'hybrid_multi': '#2ca02c'
    },
    
    # Attention map colormap
    'attention_cmap': 'hot',
    
    # ROC curve
    'roc_linewidth': 2,
    
    # Confusion matrix
    'cm_cmap': 'Blues'
}

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s [%(levelname)s] %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'log_file': RESULTS_DIR / 'experiment.log'
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_device():
    """Get the device to use for training."""
    import torch
    
    if TRAINING_CONFIG['device'] == 'auto':
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return torch.device(TRAINING_CONFIG['device'])


def print_config():
    """Print current configuration."""
    print("\n" + "=" * 70)
    print("CONFIGURATION SUMMARY")
    print("=" * 70)
    
    print(f"\nDataset:")
    print(f"  - Samples per class: {DATASET_CONFIG['samples_per_class']}")
    print(f"  - Image size: {DATASET_CONFIG['image_size']}x{DATASET_CONFIG['image_size']}")
    print(f"  - Classes: {DATASET_CONFIG['classes']}")
    
    print(f"\nASIC (LV06):")
    print(f"  - Enabled: {ASIC_CONFIG['enabled']}")
    print(f"  - Host: {ASIC_CONFIG['host']}:{ASIC_CONFIG['port']}")
    print(f"  - Fallback to software: {ASIC_CONFIG['fallback_to_software']}")
    
    print(f"\nTraining:")
    print(f"  - Batch size: {TRAINING_CONFIG['batch_size']}")
    print(f"  - Epochs: {TRAINING_CONFIG['num_epochs']}")
    print(f"  - Learning rate: {TRAINING_CONFIG['learning_rate']}")
    print(f"  - Device: {get_device()}")
    
    print(f"\nModels to benchmark:")
    for name, cfg in MODEL_CONFIG['models'].items():
        print(f"  - {name}: {cfg['description']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print_config()
