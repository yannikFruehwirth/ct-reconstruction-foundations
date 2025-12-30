# -- Imports --
import numpy as np
from skimage.transform import radon, iradon
from skimage.data import shepp_logan_phantom
from typing import Tuple

# -- Code --

class CTProjector:
    """handles core CT physics: Forward and Backward projection"""
    
    def __init__(self, size: int = 400):
        self.size = size
        self.phantom = shepp_logan_phantom()
        if self.phantom.shape[0] != size:
            from skimage.transform import resize
            self.phantom = resize(self.phantom, (size, size))

    def project(self, theta: np.ndarray) -> np.ndarray:
        """Forward projection (Radon Transform)"""
        return radon(self.phantom, theta=theta)

    def reconstruct(self, sinogram: np.ndarray, theta: np.ndarray, filter_name: str = 'ramp') -> np.ndarray:
        """Backward projection (Filtered Back Projection)"""
        return iradon(sinogram, theta=theta, filter_name=filter_name)