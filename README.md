<h1 align="center">🌟 LLaMaDesu! ラマデス！ 🌟</h1>
<img width="auto" height="auto" alt="LLaMaDesu Banner" src="https://github.com/user-attachments/assets/fa8af113-e3f9-4abf-996d-611601128050" />

Welcome to the **LLaMaDesu!** repository! Originally developed as an extension to Home Assistant OS (HAOS)'s [Year of Voice](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/) initiative, this project has since evolved into a standalone unique solution, specially designed to curb the spread of loneliness.

As of writing, this project is the **first of its kind** to integrate an anime-styled Live2D frontend seamlessly into the HAOS backend. Yes, you've read that right - by sending text or voice prompts to LLaMaDesu, you can toggle your room lights, turn on the coffee machine, or even play your favourite music on your Bluetooth speakers, all done remotely via the HAOS Assist pipeline. This capability allows LLaMaDesu to behave as if a real anime character was looking after your home - giving the illusion that fiction has been brought into reality.

Furthermore, LLaMaDesu is a **free and open-source** software, with support for **local offline** processing and LLM inferencing, ensuring the **privacy and security** of your chats. It is also **fully customizable**, as the behaviour of your character can be controlled through Ollama's `Modelfile` configuration. Any open-source LLM models can be used with LLaMaDesu, even 400B parameter models - with the only limiting factor being your hardware (more specifically, your GPU's VRAM). For users with limited hardware resources, no problem! Just switch over to **cloud** mode in the settings and you'll be able to run LLaMaDesu even on a **Raspberry Pi 5**.

It's already the big 2020s after all - who doesn't need an anime AI chatbot in their lives? ;) Without further ado, thank you for your support and we truly hope you enjoy using LLaMaDesu! 

---
# ⚡ Features

🧩 **Cross-Platform and LAN-Wide Connectivity**
- LLaMaDesu can be hosted on any Windows/macOS/Linux device. By default, it is also configured to have LAN-wide access, so you are able to connect to the LLaMaDesu frontend from **any device within the same Wi-Fi network** (assuming the device has a browser that supports WebGL). Hence, you can access LLaMaDesu from your **phone, laptop, Nintendo Switch** or even your **smart fridge**, making it extremely versatile and convenient, benefitting that of a **progressive web app (PWA)**.

💭 **Local & Cloud LLM Support**
- Have a powerful GPU? You can run the app **completely offline** through your **local** LLM (Ollama)! Otherwise, switch on over to **cloud** mode in `settings.yaml`, and obtain responses through the cloud LLM platform of your choice!
  - For cloud mode, your private API Key is required. Currently supported platforms are **OpenAI's ChatGPT** and **Google's Gemini**.

🔊 **Text & Voice-Based Communication**  
- Communicate with your local LLM seamlessly using **text input** or **voice push-to-talk** functionality from any device within your local network. This gives you the ability to interact with your HAOS voice assistant beyond a satellite device.

📜 **Chat History Management**  
- View and manage your chat history with advanced features such as search, archiving, and deletion of individual entries. Saving of chat history can be turned off for privacy purposes at any time.

💻 **Connected Clients List**  
- Easily monitor which devices are connected to your LLaMaDesu instance. If needed, you can remotely disconnect any device from the network, enforcing control and security over your setup.

🤖 **Customizable STT/LLM/TTS Models**
- Thanks to the Wyoming protocol, you can select and specify which models to use based on your needs.
  - Want to use a quantized, more efficient model? You can!
  - Need a model with larger parameters that can handle relatively complex requests? Certainly!
  - Want the TTS to sound like a specific character? Check out the [**PipeZ**](https://github.com/chaosiris/PipeZ) or [**TextyMcSpeechy**](https://github.com/domesticatedviking/TextyMcSpeechy) repositories for quick solutions to train your own Piper voice model! (*WSL2 or Linux required. Please always ensure ethical usage and collection of voice training data.*) 

🎨 **Live2D Model Compatibility**  
- Import and use any existing Live2D model effortlessly with plug-and-play support. Just extract the model folder in `/src/live2d_models`. From the settings, you can also switch seamlessly between Live2D models from a dropdown list corresponding to your `model_dict.json`. <br>You can **use or even design your very own Live2D model** of your favourite character, provided that it complies with **Live2D's Terms of Use**. 

💬 **Interactive Live2D Experience**  
- Make your Live2D model come alive through **idle animations** or **tap motions** as configured in their respective `*.model.json` files. Additionally,  **lip-sync** animations based on received outputs, making your virtual assistant feel more expressive and responsive.

✨ **Customizable Presets**  
- Set up a **shortcut list** of frequently used prompts (e.g. "turn off the lights in the living room") so you can quickly trigger actions with a single click or tap. This feature allows for extremely efficient and streamlined control over your smart home.

⚙️ **Flexible Settings Configuration**  
- Tailor the app to your preferences with a wide range of settings, which can be customized in the `settings.yaml` file, including:
  - **show-sent-prompts**: Choose whether or not to display the text prompt after sending it.  
  - **enable-idle-motion**: Enable or disable idle motion animations for the Live2D model.  
  - **enable-tap-motion**: Control whether tap gestures trigger animations or actions on the model.  
  - **enable-prompt-repeat**: Enable or disable the ability to resend or re-paste previous text/voice prompts.  
  - **enable-mouth-scaling**: Adjust the scaling of mouth movements based on spoken syllables, improving lip-sync accuracy.  
  - **enable-voice-input**: Turn on or off the voice-based Push to Talk feature.  
  - **save-chat-history**: Decide whether to store your chat history for future reference. Disable for privacy.  
  - **adaptive-background**: Automatically adjust the background based on the time of day.  
  - **timeout**: Set a custom timeout duration before cancelling the LLM response.

---

# 📦 Requirements

## Software
- Python 3.10+ [[Python Download](https://www.python.org/downloads/)]
- Docker Desktop (w/ WSL2) [[Docker Download](https://www.docker.com/get-started/)]
- Ollama [[Ollama Download](https://ollama.com/download)]
- Any modern browser with *JavaScript* and *WebGL* enabled

> **NOTE:** Please ensure that the 'python', 'docker', and 'ollama' commands have been added to `PATH` (i.e. callable from terminal) during installation! 

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

## **🚀 Usage Guide**

---

## **🎬 Demo Video**

---

## **📌 High-Level Technical Overview**


---
## **⚠️ Disclaimers**

To quote a popular saying in the cybersec field, **a chain is only as strong as its weakest link.**   
In the context of this project, your **IoT network is only as secure as its most vulnerable device.**  
For this reason, it is highly recommended to:
- **Host this application on a hardened OS (Windows/Linux)** with **regular updates**.
- **Use a properly firewalled router/VLAN** to segment your local network.
- Due to the likely possibility of **LLM hallucinations**, please **do not expose** any high-risk entities (relating to Health, Safety & Security) to Ollama via Assist (e.g. door locks or thermostats). This can be configured in your Ollama settings under HAOS Integrations. 

By using this app, you acknowledge that the app is provided "as is" and at your own risk. We do not accept any liability for any damages, losses, or issues arising from the use of this app. We are not liable for any direct, indirect, incidental, or consequential damages resulting from your use of the app.

This app is not a substitute for a real relationship. Black Mirror has warned us about this. At the end of the day, an LLM is just a highly sophisticated probability-based text prediction model. Please never delude yourself into thinking it is a real person - always reach out if you need someone to talk to. There will always be someone out there willing to help :)

LLaMaDesu is not affiliated with the developers of Home Assistant OS (Nabu Casa, Inc or the Open Home Foundation). Any use of their name or brand is purely for informational or descriptive purposes.

---
## **📜 Third Party Licenses**
### Live2D Sample Models Notice

This project includes Live2D sample models **(Shizuku (Cubism 2.1) and Haru (Cubism 4))** provided by Live2D Inc. These assets are licensed separately under the Live2D Free Material License Agreement and the Terms of Use for Live2D Cubism Sample Data. They are not covered by the MIT license of this project.

The Live2D simple models are owned and copyrighted by Live2D Inc. The sample data are utilized in accordance with the terms and conditions set by Live2D Inc. (See [**Live2D Free Material License Agreement**](https://www.live2d.jp/en/terms/live2d-free-material-license-agreement/) and [**Terms of Use**](https://www.live2d.com/eula/live2d-sample-model-terms_en.html)).

**Note:** For commercial use, especially by medium or large-scale enterprises, the use of these Live2D sample models may be subject to additional licensing requirements. If you plan to use this project commercially, please ensure that you have the appropriate permissions from Live2D Inc., or use versions of the project without these models.

---
## **⭐️ Project Milestones**
<div align="center">
  
| Plan | Stars | Achieved? |
|------|-------|-----------|
| Public release of improved Kozue Piper TTS model (trained over 100,000 epochs) | 10 | ❌ |
| Migration of frontend to React framework | 100 | ❌ |
| Commission of LLaMaDesu-themed Live2D model (bring our logo character to life!) | 1000 | ❌ |

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=chaosiris/llamadesu&type=Date)](https://star-history.com/#chaosiris/llamadesu&Date)

</div>
