# -- IMPORTS --
import numpy as np
from scipy.ndimage import rotate # lib for interpolation bc it is easier

def simple_radon(image: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """
    manual implementation radon transformation (for understanding)
    
    Args:
        image: 2D input phantom
        theta: array of angles in degrees
        
    Returns:
        sinogram
    """
    n_angles = len(theta)
    n_detectors = image.shape[0] # assume it is quadratic
    sinogram = np.zeros((n_detectors, n_angles))
    
    for i, angle in enumerate(theta):
        # 1. rotate image by current angle
        rotated_img = rotate(image, -angle, reshape=False, order=1)
        
        # 2. project (sum along vertical axis)
        sinogram[:, i] = np.sum(rotated_img, axis =0)
        
    return sinogram