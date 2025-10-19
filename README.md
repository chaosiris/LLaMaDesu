# 🌟 LLaMaDesu! ラマデス！

LLaMaDesu! - your dedicated Live2D AI companion app designed to curb your loneliness. 

---
# ⚡ Features
To be completed

---

# 📦 Requirements

## Software
- Python 3.10+
- Docker Desktop (w/ WSL2)
- Ollama (with at least one model pulled, as a starting example we will be using llama3.1:8b)

## Hardware
- Any NVIDIA GPU w/ **4GB VRAM** (minimum specs for `local` mode)
- CPU w/ **16GB RAM** (minimum specs for `cloud` mode)

---

# 📥 Setup Guide

## Option A - Automated Scripts

### 1. Run setup.exe
Once you have installed all required software, run `setup.exe` at the root folder to begin the setup process. This process encompasses the following:
- Intialization of virtual environment (in `src/venv`);
- Installation of required Python packages (as listed in `requirements.txt`); 
- Creation of custom model (as specified in `setup/ollama/Modelfile.txt`); 
    -  Remember to update the `OLLAMA_MODEL` variable in `settings.yaml` to use your newly created custom model.
- Generation of SSL certs needed for HTTPS;
- Downloading of Docker containers required for local STT and TTS processing.

### 2. Run LLaMaDesu!.exe
Navigate to the src/ folder and run LLaMaDesu!.exe to launch the web app. Open up a browser and connect to the frontend interface via `<PROTOCOL>://<IP>:<PORT>` as specified in `settings.yaml`. That's all for the setup process!

## Option B - Manual Provisioning

### 1. Virtual Environment
From the root folder, create a venv/ inside the src/ folder, then activate it:

```bash
python3 -m venv src/venv
source venv/bin/activate
```

If you would like to use Cloud API, create a `.env` file at root and follow the example in `.env.example`:

```bash
touch .env
nano .env
```

### 2. Install Requirements

Ensure that all the Python packages listed in `requirements.txt` are successfully installed.

```bash
pip install -r requirements.txt
```

### 3. Pull Model from Ollama

Check whether if the local machine has any Ollama models (`ollama list`) already installed. If not, perform the following steps:

```bash
ollama pull llama3.1:8b
```

### 4. Custom Model Creation (Optional)

Navigate to `setup/ollama` and run the custom model creation script:

```bash
cd setup/ollama
python create_custom_model.py
```

Once created, update the `OLLAMA_MODEL` variable in `settings.yaml` to use your custom model.

### 5. Home Assistant Integration (Optional)

For Home Assistant (HAOS) mode users, copy the automation file:

```bash
cp setup/haos/haos_webhook.yaml <your_haos_automations_directory>
```

### 6. SSL Certificate Generation

Navigate to setup/openssl:

```bash
cd setup/openssl
python generate_ssl_keys.py
```

This generates SSL certs required for HTTPS.

### 7. Docker Setup

Navigate to the setup/docker folder:

> **NOTE:** Make sure that Docker is up-to-date before running the setup file.

```bash
cd setup/docker
python docker_setup.py
```

Ensure both docker containers for Whisper and Piper are up and running.

### 8. Application Setup

Navigate to `src/` and generate the model dictionary.

> **NOTE:** The `generate_model_dict.py` script must be run whenever you add or remove a Live2D model in `src/live2d_models`.

```bash
cd src/
python generate_model_dict.py
```

### 9. Configuration and Launch

Edit `settings.yaml` if there are any endpoints that differ from the default values.

Run the application:

```bash
python app.py
```

Open your browser and connect to the app via the URL `<PROTOCOL>://<IP>:<PORT>`.

---
