# llamadesu

LLaMaDesu! - your dedicated Live2D AI companion app designed to curb your loneliness. Fork of vCHAOS.

## Requirements

- Python 3.10+
- Docker (w/ WSL2)
- Ollama (with at least one model pulled, as a starting example we will be using llama3.1:8b)

## Provisioning/Setup Steps

### Virtual Environment

Create a venv/ at the root of the folder, then activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Docker Setup

Navigate to the setup/docker folder:

> **NOTE:** Make sure that Docker is up-to-date before running the setup file.

```bash
cd setup/docker
python docker_setup.py
```

Ensure both docker containers for Whisper and Piper are up and running.

### 2. SSL Certificate Generation

Navigate to setup/openssl:

```bash
cd setup/openssl
pip install -r requirements.txt
python generate_ssl_keys.py
```

This generates SSL certs required for HTTPS.

### 3. Home Assistant Integration (Optional)

For Home Assistant users, copy the automation file:

```bash
cp setup/haos/haos_webhook.yaml <your_haos_automations_directory>
```

### 4. Pull Model from Ollama

Check whether if the local machine has any model (`ollama list`) from Ollama or not, if not perform the following steps:

```bash
ollama pull llama3.1:8b
```

### 5. Application Setup

Navigate to `src/`, install the app dependencies and generate the model dictionary.

> **NOTE:** The `generate_model_dict.py` script must be run whenever you add or remove a Live2D model in `src/live2d_models`.

```bash
cd src/
pip install -r requirements.txt
python generate_model_dict.py
```

### 5. Configuration and Launch

Edit `settings.yaml` if there are any endpoints that differ from the default values.

Run the application:

```bash
python app.py
```

Open your browser and connect to `localhost:port`.
