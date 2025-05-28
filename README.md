AEye Project - README

Welcome to AEye! This project is focused on building a real-time color scanning and correction system powered by AI and vision technologies.

This README will grow as the project evolves.

📅 Project Status

✅ Core color engine established (LAB / RGB conversions working)

✅ Future expansion planned: Image capture, region scanning, ML-based pigment correction

🔗 Key Libraries and Official Documentation

💊 scikit-image

User Guide: https://scikit-image.org/docs/stable/

Color Conversion API: https://scikit-image.org/docs/stable/api/skimage.color.html

📂 NumPy

Main Documentation: https://numpy.org/doc/stable/

API Reference: https://numpy.org/doc/stable/reference/

🖼️ OpenCV (cv2)

Python Documentation: https://docs.opencv.org/4.x/

Color Conversion Reference: https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html

📚 Python Standard Library

argparse Documentation: https://docs.python.org/3/library/argparse.html

json Module Documentation: https://docs.python.org/3/library/json.html

🧬 Future Tools (optional as project expands)

📸 OpenCV Video I/O

VideoCapture Tutorial: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

👁️ PyQt5 / PyQt6 (Touchscreen GUI)

PyQt5 Docs: https://www.riverbankcomputing.com/static/Docs/PyQt5/

PyQt6 Docs: https://www.riverbankcomputing.com/static/Docs/PyQt6/

🚀 NVIDIA Tools for Future AI Expansion

CUDA Overview: https://developer.nvidia.com/cuda-zone

TensorRT Overview: https://developer.nvidia.com/tensorrt

💚 Project Structure (Currently)

AEye/
├── calibration/
├── capture/
├── comparison/
├── data/
├── ui/
├── utils/
│   └── lab_tools.py
├── main.py
├── playground.py
├── requirements.txt
├── README.md

🌈 Vision for AEye

Real-time color inspection

Intelligent pigment correction suggestions

Visual touch UI for production floors

Future machine learning and predictive analytics

## Development Environment

This project is configured to run in a VS Code Dev Container using Docker.

### Requirements
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

# AEye Color Matching System – Local Development Setup

## 🔹 Setup Local Virtual Environment
```bash
./setup_local_dev.sh