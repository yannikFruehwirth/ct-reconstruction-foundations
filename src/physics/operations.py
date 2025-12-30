# -- IMPORTS --
import numpy as np
from skimage.transform import radon, iradon, rotate
from skimage.data import shepp_logan_phantom
import matplotlib.pyplot as plt
from typing import Tuple, Optional
from .manual_projections import simple_radon

# -- CODE --
class CTProcessor:
    """Handles basic CT forward and backward projections"""
    
    def __init__(self, resolution: int = 400):
        self.resolution = resolution
        self.image = shepp_logan_phantom() # 400 standard for shepp
    
    def generate_sinogram(self, theta: np.ndarray, manual=False) -> np.ndarray:
        """
        Radon Transfo
        
        Args:
            theta: array proj angles in degrees (!)
        Returns:
            sinogram (radon space)
        """
        if manual:
            sinogram = simple_radon(self.image, theta=theta)
            print("     Using manual radon transformation...")
        else:
            sinogram = radon(self.image, theta = theta)
        
        return sinogram
    
    def reconstruct(self, sinogram: np.ndarray, theta: np.ndarray, filter_type: str = 'ramp') -> np.ndarray:
        """
        Inverse Radon Transfo through filtered back projection
        
        Args:
            sinogram: see above
            theta: angles during projection
            filter_type: filter for blurr reduction (ramp. shepp-logan, ...)
        returns:
            reconstructed 2D image
        """
        reconstruction = iradon(sinogram, theta=theta, filter_name=filter_type)
        return reconstruction
    
    @staticmethod
    def calculate_error(original: np.ndarray, reconstructed: np.ndarray) -> float:
        """manual calcultion MSE"""
        return np.mean(( original - reconstructed)**2)
    