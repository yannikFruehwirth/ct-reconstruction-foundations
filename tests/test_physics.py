# -- IMPORTS --
import pytest
import numpy as np
from physics.ct_ops import CTProjector
from utils.metrics import calculate_metrics

# -- CODE --
@pytest.fixture
def default_projector():
    """Fixture to provide a standard projector instance for tests."""
    return CTProjector(size=128)

def test_sinogram_dimensions(default_projector):
    """Check if the sinogram shape matches the input angles."""
    n_angles = 90
    theta = np.linspace(0., 180., n_angles, endpoint=False)
    sinogram = default_projector.project(theta)
    
    assert sinogram.shape[1] == n_angles
    assert sinogram.ndim == 2

def test_empty_image_reconstruction():
    """An empty image should result in an empty (zero) reconstruction."""
    res = 64
    projector = CTProjector(size=res)
    projector.phantom = np.zeros((res, res)) 
    
    theta = np.linspace(0., 180., 30, endpoint=False)
    sinogram = projector.project(theta)
    reconstruction = projector.reconstruct(sinogram, theta)
    
    assert np.allclose(reconstruction, 0, atol=1e-5)

def test_reconstruction_quality(default_projector):
    """Ensure that FBP reconstruction of a clean phantom is high quality."""
    theta = np.linspace(0., 180., 180, endpoint=False)
    sinogram = default_projector.project(theta)
    reconstruction = default_projector.reconstruct(sinogram, theta)
    
    metrics = calculate_metrics(default_projector.phantom, reconstruction)
    
    assert metrics["SSIM"] > 0.9
    assert metrics["MSE"] < 0.01

def test_metrics_logic():
    """Test if metrics helper correctly identifies identical images."""
    img = np.random.rand(100, 100).astype(np.float32)
    metrics = calculate_metrics(img, img)
    
    assert metrics["SSIM"] == pytest.approx(1.0)
    assert metrics["MSE"] == pytest.approx(0.0)