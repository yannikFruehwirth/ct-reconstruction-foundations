# -- IMPORTS --
import argparse
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from physics.ct_ops import CTProjector
from utils.metrics import calculate_metrics

# -- CODE --
def add_noise(sinogram: np.ndarray, noise_level: float) -> np.ndarray:
    """Simulation of noise"""
    if noise_level <= 0:
        return sinogram
    noise = np.random.normal(0, noise_level * np.max(sinogram), sinogram.shape)
    return sinogram + noise

def main():
    parser = argparse.ArgumentParser(description="CT Reconstruction Pipeline")
    
    # Args
    parser.add_argument("--res", type=int, default=256, help="Resolution of the phantom")
    parser.add_argument("--angles", type=int, default=180, help="Number of projection angles")
    parser.add_argument("--filter", type=str, default="ramp", 
                        choices=["ramp", "shepp-logan", "cosine", "hamming"], help="FBP Filter")
    parser.add_argument("--noise", type=float, default=0.0, help="Noise level (0.0 to 0.1 recommended)")
    parser.add_argument("--out", type=str, default="data/processed/last_run.png", help="Output path")

    args = parser.parse_args()

    # Error Handling
    if args.res > 1024:
        print(f"[!] Warning: High resolution ({args.res}) might be slow.")
    if args.angles < 10:
        print(f"[!] Warning: Very low angle count ({args.angles}) will cause streak artifacts.")

    try:
        start_total = time.time()
        
        # 1. Init
        projector = CTProjector(size=args.res)
        theta = np.linspace(0., 180., args.angles, endpoint=False)

        # 2. Forward Projection
        print(f"[*] Projecting with {args.angles} angles...")
        sinogram = projector.project(theta)

        # 3. Optional: Add Noise (Simulation of Low-Dose CT)
        if args.noise > 0:
            print(f"[*] Adding {args.noise*100}% noise to sinogram...")
            sinogram = add_noise(sinogram, args.noise)

        # 4. Reconstruction
        print(f"[*] Reconstructing using '{args.filter}' filter...")
        reconstruction = projector.reconstruct(sinogram, theta, filter_name=args.filter)

        # 5. Evaluation
        metrics = calculate_metrics(projector.phantom, reconstruction)
        
        # Metrics/ final output
        print("\n" + "="*30)
        print(f"CT RECONSTRUCTION COMPLETE")
        print(f"Time: {time.time() - start_total:.2f}s")
        print(f"MSE:  {metrics['MSE']:.5f}")
        print(f"SSIM: {metrics['SSIM']:.5f}")
        print("="*30)

        # Visualization
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        axes[0].imshow(projector.phantom, cmap='gray')
        axes[0].set_title("Ground Truth")
        
        axes[1].imshow(sinogram, cmap='magma', aspect='auto')
        axes[1].set_title(f"Sinogram (Noise: {args.noise})")
        
        axes[2].imshow(reconstruction, cmap='gray')
        axes[2].set_title(f"FBP ({args.filter})\nSSIM: {metrics['SSIM']:.4f}")
        
        for ax in axes: ax.axis('off')
        
        # Save results
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path)
        print()
        print(f"[+] Result saved to {out_path}")
        plt.show()

    except Exception as e:
        print(f"[FAIL] Pipeline crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()