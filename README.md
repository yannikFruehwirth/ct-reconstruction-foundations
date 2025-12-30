# CT-Foundations: Physics & Reconstruction

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive deep-dive into Computed Tomography (CT) imaging, covering everything from the mathematical foundations of the Radon Transform to modern reconstruction techniques.

## Project Overview
This repository serves as a pedagogical and technical foundation for understanding how raw X-ray projections are transformed into diagnostic 3D volumes.

## Repository Structure
* `src/`: Modular Python implementation of reconstruction algorithms.
* `notebooks/`: Interactive tutorials and visualizations.
* `data/`: Scripts for phantom generation and data handling.
* `tests/`: Unit tests for signal processing consistency.

## Mathematical Core Concepts
*(Work in Progress)*
- [ ] Radon Transformation (Forward Projection)
- [ ] Central Slice Theorem
- [ ] Filtered Back Projection (FBP)
- [ ] Iterative Reconstruction Basics

## Getting Started

### Prerequisites
This project uses **uv** for dependency management. Install it via:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

## Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd ct-foundations

# Install dependencies and create virtual environment
uv sync
```

## Roadmap
- [ ] Phase 1: Single-slice reconstruction from Shepp-Logan phantom.
- [ ] Phase 2: Implementation of different convolution filters (RAM-LAK, Shepp-Logan).
- [ ] Phase 3: Handling 3D helical scan geometries

