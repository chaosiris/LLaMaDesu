<h1 align="center">🌟 LLaMaDesu! ラマデス！ 🌟</h1>
<img width="auto" height="auto" alt="LLaMaDesu Banner" src="https://github.com/user-attachments/assets/fa8af113-e3f9-4abf-996d-611601128050" />

Welcome to the **LLaMaDesu!** repository! Originally developed as an extension to Home Assistant OS (HAOS)'s [Year of Voice](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/) initiative, this project has since evolved into a standalone unique solution, specially designed to curb the spread of loneliness.

As of writing, this project is the **first of its kind** to integrate an anime-styled Live2D frontend seamlessly into the HAOS backend. Yes, you've read that right - by sending text or voice prompts to LLaMaDesu, you can toggle your room lights, turn on the coffee machine, or even play your favourite music on your Bluetooth speakers, all done remotely via the HAOS Assist pipeline. This capability allows LLaMaDesu to behave as if a real anime character was looking after your home - giving the illusion that fiction has been brought into reality.

Furthermore, LLaMaDesu is a **free and open-source** software, with support for **local offline** processing and LLM inferencing, ensuring the **privacy and security** of your chats. It is also **fully customizable**, as the behaviour of your character can be controlled through Ollama's `Modelfile` configuration. Any open-source LLM models can be used with LLaMaDesu, even 400B parameter models - with the only limiting factor being your hardware (more specifically, your GPU's VRAM). For users with limited hardware resources, no problem! Just switch over to **cloud** mode in the settings and you'll be able to run LLaMaDesu even on a **Raspberry Pi 5**.

It's already the big 2020s after all - who doesn't need an anime AI chatbot in their lives? ;) Without further ado, thank you for your support and we truly hope you enjoy using LLaMaDesu! 

---

# Table of Contents

- [⚡ Features](#features)
- [🎬 Demo Video](#demo-video)
- [📦 Requirements](#requirements)
  - [Software](#software)
  - [Hardware](#hardware)
- [📥 Setup Guide](#setup-guide)
  - [Option A - Automated Scripts (Windows)](#option-a)
  - [Option B - Manual Provisioning (For Linux/macOS)](#option-b)
- [🚀 Usage Guide](#usage-guide)
- [📌 High-Level Technical Overview](#high-level-technical-overview)
- [⚠️ Disclaimers](#disclaimers)
- [📜 Third Party Licenses](#third-party-licenses)
- [⭐️ Project Milestones](#project-milestones)

---

# ⚡ Features <a name="features"></a>

🧩 **Cross-Platform and LAN-Wide Connectivity**
- LLaMaDesu can be hosted on any Windows/macOS/Linux device. By default, it is also configured to have LAN-wide access, so you are able to connect to the LLaMaDesu frontend from **any device within the same Wi-Fi network** (assuming the device has a browser that supports WebGL). Hence, you can access LLaMaDesu from your **phone, laptop, gaming console** or even your **smart fridge**, making it extremely versatile and convenient, benefitting that of a **progressive web app (PWA)**.

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

⚙️ **Flexible Settings Configuration**  <a name="frontend-settings"></a>
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

# **🎬 Demo Video** <a name="demo-video"></a>

https://github.com/user-attachments/assets/6a09530e-4d78-4e93-b8be-87079ab73afc

[![Watch on YouTube](https://www.youtube.com/watch?v=vheFnKx5tmE)]

Remember to Like, Share and Subscribe! 🥰🔔🚨

---

# 📦 Requirements <a name="requirements"></a>

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

# 📥 Setup Guide <a name="setup-guide"></a>

## Option A - Automated Scripts (Windows) <a name="option-a"></a>

### 1. Run setup.exe
Once you have installed all required software, run `setup.exe` at the root folder to begin the setup process. This process encompasses the following:
- Intialization of virtual environment (in `src/venv`);
- Installation of required Python packages (as listed in `requirements.txt`); 
- Creation of custom model (as specified in `setup/ollama/Modelfile.txt`); 
    -  Remember to update the `OLLAMA_MODEL` variable in `settings.yaml` to use your newly created custom model.
- Generation of SSL certs needed for HTTPS;
- Downloading of Docker containers required for local STT and TTS processing.

### 2. Run LLaMaDesu!.exe
Navigate to the src/ folder and run LLaMaDesu!.exe to launch the web app. Open up a browser and connect to the frontend interface via `<PROTOCOL>://<HOST IP>:<PORT>` as specified in `settings.yaml`. That's all for the setup process!

## Option B - Manual Provisioning (For Linux/macOS) <a name="option-b"></a>

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

> **NOTE:** If you wish to pull another open-source LLM model, please feel free to do so, provided that your hardware is powerful enough to support it!

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

Open your browser and connect to the app via the URL `<PROTOCOL>://<HOST IP>:<PORT>`.

---

# **🚀 Usage Guide** <a name="usage-guide"></a>

## ✏️ Text Input

- Toggle the **text input mode** by clicking on the ✏️ **pencil icon** on the bottom-right corner!
![textinput](https://github.com/user-attachments/assets/ca1e2108-562a-4d23-9b34-468e073b5a95)

## 🎤 Voice Input (Push To Talk)

- Hold the  🎤 **Push To Talk** button in the middle of the screen and release to send your voice input!
![voiceinput](https://github.com/user-attachments/assets/c42601d0-3f15-46af-9651-82f06c50d6ac)

## 🔁 Repeat Input

- After sending a text/voice input, the 🔁 **repeat icon** will appear, which when clicked, will resend your previous input!
![repeatinput](https://github.com/user-attachments/assets/5855a4b2-fffb-406b-b13b-999890c99f91)

## ▶️ Auto Scroll / ⬆️ Scroll To Top

- Tired of scrolling through long responses? Click on the ▶️ **play icon** to enable auto-scroll mode, then tap on the ⬆️ **up icon** to instantly jump back to the top of the paragraph if needed!
![scroll](https://github.com/user-attachments/assets/bd609ffe-8233-48c4-b861-5403f3ac4f46)

## 📜 Chat History

- Toggle the **chat history sidebar** by clicking on the 📜 **scroll icon** on the bottom-left corner! All previous text responses stored in `src/output` will be listed in **reverse chronological order**, and can be loaded back into the frontend upon clicking. It's also possible to filter for responses containing a specific word through the **🔍 search bar** feature!
- **📦 Archive/🗑 Delete Chat History:** Want to archive or delete certain responses? Just select the checkbox for that entry and click on the corresponding icon! Archived entries will be placed into `src/archived`, whereas deleted entries will be securely processed via 7 deletion passthroughs and therefore be non-recoverable.
> **NOTE:** If no entries are selected when clicking on the archive/delete icons, it is assumed that all entries are selected!
![chathistory](https://github.com/user-attachments/assets/908ddd45-a6f3-408c-8157-2e669ca1a349)

## ✨ Presets

- Toggle the **presets sidebar** by clicking on the ✨ **star icon** on the bottom-right corner! The list of presets stored in `src/presets.json` will be loaded into the sidebar, allowing for the quick sending of frequently used prompts.
- **➕ Add/📝 Edit Preset:** To add a new preset, just click on the add icon to bring up a modal, allowing you to input the name and content of the new preset prompt, which will then be saved into the `src/presets.json` file! Similarly, you can edit existing presets by selecting its checkbox and clicking on the edit icon. Make sure to save any changes!
- **🗑 Remove Preset:** Delete unused or unnecessary presets by selecting its checkbox and clicking on the delete icon! It's also possible to delete multiple presets via checkboxes.
![presets](https://github.com/user-attachments/assets/fde84b25-0b0d-4924-844c-4d7f8337c16c)

## 💻 Connected Clients

- Toggle the **connected clients modal** by clicking on the 💻 **computer icon** on the bottom-left corner. This shows a **list of device IPs** which are connected to the LLaMaDesu instance over the local network. Manually disconnect any client by clicking on the **Disconnect** button. You can even disconnect yourself, the host! To reconnect, just refresh the browser.
![clients](https://github.com/user-attachments/assets/81811efe-b8f9-4090-bc1a-a622519b825b)

## ⚙️ Settings

- Toggle the **settings modal** by clicking on the ⚙️ **gear icon**. You can change all sorts of [frontend settings](#frontend-settings) here, including switching between your Live2D models as listed in `src/model_dict.json` and available in `src/live2d_models`.
![settings](https://github.com/user-attachments/assets/37ba374c-5139-48b5-aec7-72d07ed972ce)

## 👉 Tap Motions

- Depending on your `src/model_dict.json` configuration and the Live2D model's compatibility, you can also trigger **tap motions** by clicking on your character! 
![tapmotions](https://github.com/user-attachments/assets/31964d74-4020-45cc-b49d-3af83565a6c5)

## ⌨️ Shortcut Keys

- For users with a discrete keyboard, there are **shortcut keys** available to toggle certain actions on the frontend, as shown in the table below:
<div align="center">
  
| Shortcut Action            | Key          |
|----------------------------|--------------|
| Text Input                 | `I`          |
| Voice Input (Hold)         | `Spacebar`   |
| Chat History Sidebar       | `H`          |
| Presets Sidebar            | `P`          |
| Settings Modal             | `S`          |
| Connected Clients Modal    | `C`          |

</div>

---

# **📌 High-Level Technical Overview** <a name="high-level-technical-overview"></a>

<img width="auto" height="auto" alt="High-Level Technical Overview Diagram" src="https://github.com/user-attachments/assets/16fcbb55-0ea2-47b6-a7e2-a95242a7b06f" />

As shown in the diagram, **LLaMaDesu!** can be segmented into **three major components**:

### 1. User Interface/Frontend (Powered by Live2D & Pixi.js)
- Upon browser initialization, the **Pixi.js framework** validates the selected Live2D model files from the host's `src/live2d_models` folder. WebGL then renders the Live2D model seamlessly, forming an interactive and responsive frontend interface, complete with your favourite Live2D character.
- When the user sends a text/voice input, JavaScript sends the input securely via an **API call** to the backend for processing.

### 2. Backend Services (Powered by Python's FastAPI & WebSockets)
- Due to the necessity for real-time communication, the backend is constructed using Python's **FastAPI** and **WebSockets** packages to ensure **optimized response times** between each API endpoint and all connected frontend clients.
- The response is procedurally generated via a *'ping-pong'* structured pipeline. For instance, the user's voice input is **first sent to Faster-Whisper Docker container**, then **back to the backend** for validation, which then gets sent to the following endpoints (Ollama & Piper). Ultimately, the output `.txt` and `.wav` files will be generated by the Piper Docker container and be placed into the `src/output` folder. Finally, the `monitor_notifications()` function in the backend will pick up the existence of these new files upon generation and forward it to the frontend interface.
  - Note that if the user sends a text input, the Faster-Whisper Docker container will be bypassed entirely.

### 3. Wyoming Protocol (Faster-Whisper STT, Ollama & Piper TTS)
- The **Faster-Whisper** and **Piper** Docker containers accept inputs via **TCP endpoints** *(with default ports being 10300 and 10200 respectively)*. Upon receiving an input via an API call, proprietary Wyoming methods will be called to synthesize the corresponding output text/audio, based on the selected STT/TTS models.
- On the other hand, **Ollama** accepts inputs via a standard **HTTP(s) endpoint** *(default port 11434)*. Depending on the chosen LLM model and model file instructions, it will harness the user's GPU power to generate a relevant output text response, based on the user's input.

### 🔄 TL;DR
    User Interface (Text/Voice Input) ➝ Backend Services (FastAPI & WebSockets) ➝ Faster-Whisper (STT) ⇄ Ollama/HAOS Assist (LLM) ⇄ Piper (TTS) ➝ New .txt and .wav file generated in src/output ➝ Backend Services (monitor_notifications() Function) ➝ User Interface (Text/Voice Output)

---

# **⚠️ Disclaimers** <a name="disclaimers"></a>

To quote a popular saying in the security industry, **a chain is only as strong as its weakest link.**   
In the context of this project, your **IoT network is only as secure as its most vulnerable device.**  
For this reason, it is highly recommended to:
- **Host this application on a hardened OS (Windows/Linux)** that is always **up-to-date**.
- **Use a properly firewalled router/VLAN** to segment your local network.
- Due to the likely possibility of **LLM hallucinations**, please **do not expose** any high-risk entities (relating to Health, Safety & Security) to Ollama via Assist (e.g. door locks or thermostats). This can be configured in your Ollama settings under HAOS Integrations. 

By using this app, you acknowledge that the app is provided "as is" and at your own risk. We do not accept any liability for any damages, losses, or issues arising from the use of this app. We are not liable for any direct, indirect, incidental, or consequential damages resulting from your use of the app.

This app is not a substitute for a real relationship. Black Mirror has warned us about this. At the end of the day, an LLM is just a highly sophisticated probability-based text prediction model. Please never delude yourself into thinking it is a real person - always reach out if you need someone to talk to. **There will always be someone out there willing to help :)**

LLaMaDesu is not affiliated with the developers of Home Assistant OS (Nabu Casa, Inc or the Open Home Foundation). Any use of their name or brand is purely for informational or descriptive purposes.

---

# **📜 Third Party Licenses** <a name="third-party-licenses"></a>
### Live2D Sample Models Notice

This project includes Live2D sample models **(Hiyori (Cubism 2.1) and Haru (Cubism 4))** provided by Live2D Inc. These assets are licensed separately under the Live2D Free Material License Agreement and the Terms of Use for Live2D Cubism Sample Data. They are not covered by the MIT license of this project.

The Live2D simple models are owned and copyrighted by Live2D Inc. The sample data are utilized in accordance with the terms and conditions set by Live2D Inc. (See [**Live2D Free Material License Agreement**](https://www.live2d.jp/en/terms/live2d-free-material-license-agreement/) and [**Terms of Use**](https://www.live2d.com/eula/live2d-sample-model-terms_en.html)).

**Note:** For commercial use, especially by medium or large-scale enterprises, the use of these Live2D sample models may be subject to additional licensing requirements. If you plan to use this project commercially, please ensure that you have the appropriate permissions from Live2D Inc., or use versions of the project without these models.

---

# **⭐️ Project Milestones** <a name="project-milestones"></a>
<div align="center">
  
| Plan | Stars | Achieved? |
|------|-------|-----------|
| Public release of **improved Kozue Piper TTS model** (trained over 100,000 epochs) | 10 | ❌ |
| Add support for **Spine.js** models | 50 | ❌ |
| Migration of frontend to **React** framework | 100 | ❌ |
| Development of LLaMaDesu **SaaS platform** (chat with your character anywhere you go! 🗣)  | 500 | ❌ |
| Commission of **LLaMaDesu-themed Live2D model** (bring our logo character to life!) | 1000 | ❌ |

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=chaosiris/llamadesu&type=Date)](https://star-history.com/#chaosiris/llamadesu&Date)

</div>
