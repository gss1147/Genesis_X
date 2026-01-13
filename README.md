# Genesis-X

A theoretical and architectural framework for GPU-free, instant, and permanent LLM knowledge injection via Spectral Grafting and Analytic Weight Steering.

## Overview

Genesis-X aims to revolutionize LLM adaptation by moving away from traditional, resource-intensive fine-tuning methods. It proposes a system that can ingest multi-modal data, distill it into a "Semantic Lattice," and permanently graft this knowledge into an LLM's weights using a CPU-only process called "Spectral Grafting."

## Features

- **GPU-Free Operation:** Runs entirely on CPU, compatible with standard hardware like an Intel Core i7.
- **Instant Fine-Tuning:** Knowledge injection occurs in seconds to minutes, not hours or days.
- **Permanent Injection:** Updates are baked into the model's weights, not temporary activations.
- **Universal Ingestion:** Supports a wide variety of data formats (documents, tables, audio metadata, code, etc.).
- **Standalone GUI:** PyQt6-based interface with multiple tabs for dataset building, prompt injection, knowledge buffer, chat, model merging, and dataset workstation.
- **Resource Monitoring:** Real-time display of CPU, RAM, and Disk usage.
- **Activity Log:** Detailed, real-time feed of all system and user actions with a holographic style.
- **External Links:** Quick access to Hugging Face, GitHub, Kaggle, and other resources.
- **NSFW Toggle:** Option for uncensored processing.

## Prerequisites

- Python 3.9+
- An Intel Core i7 workstation with 24GB RAM
- A compatible GGUF quantized LLM file (e.g., Llama 2/3, Mistral)

## Installation

1.  Clone the repository or create the directory structure manually.
2.  Navigate to the `X:/Genesis_X` directory.
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    For `llama-cpp-python` on CPU:
    ```bash
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python --no-cache-dir
    ```
    Or use the CPU wheel:
    ```bash
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
    ```
    If using Conda:
    ```bash
    conda install pytorch torchvision torchaudio cpuonly -c pytorch
    pip install -r requirements.txt
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
    ```

## Usage

1.  Place your GGUF model file in the `models/` directory.
2.  Run the application:
    ```bash
    python main.py
    ```
3.  Use the GUI to select your model, upload data files, adjust settings (including NSFW mode), and initiate the grafting process using the main controls.
4.  Monitor the process via the "Knowledge Buffer" and "Activity Log".
5.  Verify the results using the "Verification Link" (Chat) tab.
6.  Manage datasets and prompts using the dedicated tabs.
7.  Perform model merging using the "Model Merger Workstation" tab (integrates full `core/amalgamation_ai.py` logic).
8.  Explore dataset building workflows in the "Dataset Workstation" tab (integrates full `core/dataset_workstation.py` logic).
9.  The generated LoRA adapter will be saved in the `adapters/` directory.

## Architecture

- `main.py`: Entry point.
- `main_gui.py`: PyQt6 application logic with enhanced features, tabs, and core integration.
- `core/`: Contains the core engines.
    - `singularity_engine.py`: Implements Spectral Grafting and LoRA generation (finalized).
    - `omni_parser.py`: Handles universal data ingestion and parsing (finalized).
    - `amalgamation_ai.py`: Implements full model merging logic based on research and Tkinter code (new).
    - `dataset_workstation.py`: Implements full dataset building logic based on Tkinter code (new).
- `models/`: Directory for LLM files.
- `adapters/`: Directory for generated LoRA files.
- `datasets/`: Directory for raw input data (optional).
- `cache/`: Directory for temporary files (optional).
