<div align="center">

# 🧠 Brain Tumor Classifier

### A CNN-powered web app that detects and classifies brain tumors from MRI scans

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)]()

**[Overview](#-overview) • [Demo](#-demo) • [Tech Stack](#%EF%B8%8F-tech-stack) • [Model Architecture](#-model-architecture) • [Installation](#-installation) • [Usage](#-usage) • [API Reference](#-api-reference) • [Results](#-results) • [Roadmap](#-roadmap)**

</div>

---

## 🔍 Overview

**Brain Tumor Classifier** is an end-to-end deep learning project that classifies brain MRI scans into four categories using a custom Convolutional Neural Network (CNN) built with **PyTorch**, served through a lightweight **FastAPI** web application.

Upload an MRI image through the browser, and the model returns a predicted tumor class along with a confidence score — all in real time.

| Class | Description |
|---|---|
| 🔴 **Glioma** | Tumor arising from glial cells |
| 🟠 **Meningioma** | Tumor arising from the meninges |
| 🟢 **No Tumor** | Healthy brain scan |
| 🔵 **Pituitary** | Tumor arising from the pituitary gland |

> ⚠️ **Disclaimer:** This project is for educational and research purposes only. It is **not** a certified diagnostic tool and should never be used as a substitute for professional medical advice.

---

## 🎬 Demo

<div align="center">

```
┌─────────────────────────────┐        ┌─────────────────────────────┐
│                                  │        │          Prediction: Meningioma   │
│      [ Upload MRI Scan ]         │  --->  │           Confidence: 96.42%      │
│                                  │        │                                   │
└─────────────────────────────┘        └─────────────────────────────┘
```

*Add a screenshot or GIF of your running app here, e.g. `docs/demo.gif`*

</div>

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Model** | PyTorch (custom CNN) |
| **Backend / API** | FastAPI, Uvicorn |
| **Templating** | Jinja2 |
| **Image Processing** | Pillow, Torchvision Transforms |
| **Frontend** | HTML / CSS / JS (served via `static/` & `templates/`) |
| **Training Environment** | Jupyter Notebook |

---

## 🧠 Model Architecture

A compact CNN trained on 128×128 RGB MRI images:

```
Input (3×128×128)
   │
   ├─ Conv2d(3→32, 3×3) → ReLU → MaxPool(2×2)
   ├─ Conv2d(32→64, 3×3) → ReLU → MaxPool(2×2)
   ├─ Conv2d(64→128, 3×3) → ReLU → MaxPool(2×2)
   │
   ├─ Flatten (128×16×16)
   ├─ Linear(32768 → 256) → ReLU
   └─ Linear(256 → 4)  →  [Glioma | Meningioma | No Tumor | Pituitary]
```

**Training configuration:**

| Parameter | Value |
|---|---|
| Loss Function | CrossEntropyLoss |
| Optimizer | Adam (`lr=0.001`) |
| Batch Size | 74 |
| Epochs | 8 |
| Train/Val Split | 80% / 20% |
| Input Size | 128×128 |
| Normalization | mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5) |

---

## 📊 Results

| Metric | Score |
|---|---|
| Final Training Loss | **0.0356** |
| Validation Accuracy | **90.71%** |

<details>
<summary>📈 Training loss curve (click to expand)</summary>

| Epoch | Loss |
|---|---|
| 1 | 0.8531 |
| 2 | 0.4634 |
| 3 | 0.3103 |
| 4 | 0.2170 |
| 5 | 0.1532 |
| 6 | 0.0958 |
| 7 | 0.0578 |
| 8 | 0.0356 |

</details>

---

## 📁 Project Structure

```
brain-tumor-classifier/
├── main.py                                   
├── demo_video_and_images/
|   ├── demo.png
|   └── demo_video.mp4          
├── data_preprocessing_and_model_training.ipynb
├── templates/
│   └── index.html                             
├── static/
|   ├── style.css
│   └── script.js                                
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/<zakir-maswani>/Brain-Tumor-Classifier-CNN.git
cd brain-tumor-classifier
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Ensure the model file is present
Place `brain_tumor_classifier.pth` in the project root (train it yourself using the included notebook, or download a pre-trained copy if provided).

---

## 🚀 Usage

### Run the app
```bash
python main.py
```
or, using Uvicorn directly with hot-reload:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Then open your browser at:
```
http://127.0.0.1:8000
```

Upload an MRI scan on the home page and get an instant prediction with a confidence score.

### (Optional) Retrain the model
Open `data_preprocessing_and_model_training.ipynb` in Jupyter, update the dataset paths, and run all cells to reproduce or retrain the model.

---

## 📡 API Reference

### `GET /`
Renders the home page (upload interface).

### `POST /predict`
Runs inference on an uploaded MRI image.

**Request:** `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | image file | MRI scan (JPEG/PNG) |

**Example (cURL):**
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -F "file=@sample_scan.jpg"
```

**Response:**
```json
{
  "prediction": "Meningioma",
  "confidence": 96.42
}
```

---

## 🗺️ Roadmap

- [ ] Add data augmentation to improve generalization
- [ ] Add GPU/CUDA inference support
- [ ] Add Grad-CAM visualizations for model explainability
- [ ] Dockerize the application
- [ ] Add automated tests for the `/predict` endpoint
- [ ] Deploy to a public hosting platform (Render / Railway / HF Spaces)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open an [issue](../../issues) or submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with 🧠 + 🔥 PyTorch + ⚡ FastAPI

</div>
