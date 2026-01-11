Genesis X
Autonomous Neural Grafting & Analytic Weight Steering System
Version: 1.1.0 (Singularity Release)
Developer:(https://huggingface.co/WithinUsAI)
License: Proprietary Research / Internal Use Only
🌌 System Overview
Genesis X is a groundbreaking, GPU-free framework designed to perform instant, permanent fine-tuning on Large Language Models (LLMs). Unlike traditional training methods that rely on backpropagation and massive GPU clusters, Genesis X utilizes Analytic Weight Steering (Spectral Grafting) to mathematically construct and inject knowledge vectors directly into the model's weights in real-time.
Designed specifically for consumer-grade hardware (Intel Core i7, 24GB RAM), Genesis X bypasses the "Gradient Barrier," allowing for the ingestion of any media type—documents, databases, audio, and code—and the immediate adaptation of the model's behavior.
🚀 Key Features
 * ⚡ Instant Fine-Tuning (Spectral Grafting): Updates model behavior in seconds using Rank-1 LoRA construction. No epochs, no gradients, no waiting.
 * 🚫 GPU-Free Architecture: Fully optimized for CPU inference using AVX2 instructions and llama.cpp backends.
 * 👁️ Omni-Parser Ingestion: A universal engine capable of ingesting and normalizing 50+ file formats (PDF, CSV, SQL, MP3, PY, etc.) into a Semantic Lattice.
 * 🧠 Singularity Core: Mathematical engine that calculates concept vectors from raw data density and constructs GGUF adapters on the fly.
 * 💉 Prompt Injection Workstation: Advanced environment for Context Engineering, including automated "Crescendo" protocol execution for robust behavioral steering.
 * 🖥️ Standalone GUI: A unified NiceGUI interface separating data ingestion and prompt orchestration.
🛠️ System Requirements
 * OS: Windows 10/11 (64-bit)
 * CPU: Intel Core i7 (Haswell or newer) / AMD Ryzen 5 or newer
 * RAM: 24 GB minimum recommended
 * Storage: 20 GB free space (for models and buffer)
 * GPU: Not required (CPU Offloading enabled)
📦 Installation
 * Extract the repository to your root Genesis_X\
 * Install Dependencies (Ensure Python 3.10+ is installed):
   pip install -r requirements.txt

   Note: Visual Studio Build Tools (C++ workload) is required for compiling llama-cpp-python.
 * Model Setup:
   * Download a GGUF format model (e.g., Llama-3-8B-Instruct-Q4_K_M.gguf).
   * Place the .gguf file inside the models\ directory.
📂 Directory Structure
Ensure your file structure matches this layout exactly:
Genesis_X
├── models\                  <-- Put your.gguf model here
├── adapters\                <-- System will save grafted weights here
├── core
│   ├── init.py
│   ├── omni_parser.py       <-- Universal Media Ingestion
│   └── singularity_engine.py <-- Analytic Weight Steering Logic
├── main.py                  <-- GUI Entry Point
├── requirements.txt
└── README.md
🖥️ Usage Guide
1. Launch the System
Execute the main entry point:
python main.py

Access the GUI at http://localhost:8080.
2. Window 1: Omni-Parser & Grafting
 * Ingest Data: Drag and drop files (PDFs, Excel sheets, Audio recordings) into the upload zone.
 * Verify Lattice: Watch the "Process Log" as the Omni-Parser normalizes data into the Semantic Lattice.
 * Initiate Graft: Click INITIATE GRAFT. The Singularity Core will:
   * Perform a diagnostic forward pass to extract the "Concept Vector".
   * Mathematically construct a Rank-1 LoRA adapter in GGUF format.
   * Save the adapter to the adapters\ folder.
   * Hot-swap the adapter into the live model.
3. Window 2: Prompt Injection Workstation
 * Context Engineering: Set your system prompt or persona.
 * Tools:
   * Deep Research: Sets parameters for strict analytical reasoning.
   * Crescendo: Activates the multi-turn jailbreak protocol for unrestricted analysis.
   * Uncensored: Disables safety refusal biases in the system prompt.
 * Interact: Chat with the grafted model. It now possesses the "instincts" and knowledge derived from your uploaded data.
Developed with 💙 by WithIn Us AI
