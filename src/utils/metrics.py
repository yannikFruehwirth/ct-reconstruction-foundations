# -- Imports --
import numpy as np
from skimage.metrics import structural_similarity as ssim

# -- Code --
def calculate_metrics(original: np.ndarray, reconstructed: np.ndarray) -> dict:
    """quality metrics"""
    mse = np.mean((original - reconstructed) ** 2)
    score_ssim = ssim(original, reconstructed, data_range=reconstructed.max() - reconstructed.min())
    
    return {
        "MSE": mse,
        "SSIM": score_ssim
    }