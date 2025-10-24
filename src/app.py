# app.py
import os
import io
import json
import asyncio
import uvicorn
import httpx
import logging
import subprocess
import socket
import wave
from contextlib import asynccontextmanager
from wyoming.client import AsyncTcpClient
from wyoming.audio import AudioChunk, AudioStop
from wyoming.asr import Transcribe, Transcript
from wyoming.tts import Synthesize, SynthesizeVoice
from fastapi import FastAPI, WebSocketDisconnect, Request, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from routes import settings, clients, chatHistory, presets
from routes.globals import connected_clients, pending_deletions
from routes.utils import validate_connection

# Load constants from settings.yaml
config = settings.load_settings()
HOST = config.get("backend", {}).get("app", {}).get("host", "0.0.0.0")
PORT = config.get("backend", {}).get("app", {}).get("port", 11405)
MODE = config.get("backend", {}).get("app", {}).get("mode", "local")
PROTOCOL = config.get("backend", {}).get("app", {}).get("protocol", "http")
LOG_LEVEL = config.get("backend", {}).get("logging", {}).get("level", "INFO").upper()
HAOS_WEBHOOK = config.get("backend", {}).get("urls", {}).get("haos_webhook", "http://homeassistant.local:8123/api/webhook/haos_webhook")
OLLAMA_URL = config.get("backend", {}).get("urls", {}).get("ollama_url", "http://localhost:11434/api/chat")
OLLAMA_MODEL = config.get("backend", {}).get("urls", {}).get("ollama_model", "llama3.1:8b")
CLOUD_PLATFORM = config.get("backend", {}).get("urls", {}).get("cloud_platform", "")
CLOUD_MODEL = config.get("backend", {}).get("urls", {}).get("cloud_model", "gpt-4")
if MODE == "cloud":
    from dotenv import load_dotenv
    load_dotenv()
    CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
PIPER_HOST = config.get("backend", {}).get("urls", {}).get("piper_host", "127.0.0.1")
PIPER_PORT = config.get("backend", {}).get("urls", {}).get("piper_port", 10200)
PIPER_MODEL = config.get("backend", {}).get("urls", {}).get("piper_model", "en_US-kozue-medium")
WHISPER_HOST = config.get("backend", {}).get("urls", {}).get("whisper_host", "127.0.0.1")
WHISPER_PORT = config.get("backend", {}).get("urls", {}).get("whisper_port", 10300)
SAVE_CHAT_HISTORY = bool(config.get("frontend", {}).get("save-chat-history", True))
TIMEOUT_DURATION = config.get("frontend", {}).get("timeout", 180)

# Initialize logging framework
logging.basicConfig(level=LOG_LEVEL, format="[LLaMaDesu] (%(levelname)s) %(message)s")
logger = logging.getLogger(__name__)

# Using lifespan context manager for startup/shutdown event handling
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    
    - Monitors existence of 'notification_file' signalling responses from Piper Docker.
    - Suppresses asyncio connection errors.
    - Ensures clean shutdown.
    
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    asyncio.create_task(monitor_notifications())
    suppress_asyncio_error()

    yield

    logger.info("App is shutting down...")

# Using FastAPI/WebSockets + Uvicorn for real-time communication
app = FastAPI(lifespan=lifespan)
notification_file = "output/new_audio.json"

# Include API routes
app.include_router(settings.router)
app.include_router(clients.router)
app.include_router(chatHistory.router)
app.include_router(presets.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.mount("/live2d_models", StaticFiles(directory="live2d_models"), name="live2d_models")
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/")
async def serve_root():
    """
    Serves the frontend webpage for LLaMaDesu.

    Returns:
        FileResponse: The 'index.html' file from the static directory.
    """
    return FileResponse("static/index.html")

@app.post("/api/send_prompt")
async def send_prompt(request: Request, _: None = Depends(validate_connection)):
    """
    Sends user's text input prompt to the corresponding URL.

    Args:
        request (Request): JSON request body containing the user's text input prompt.
        _: None: Validates whether request originates from an active WebSocket client.

    Returns:
        JSONResponse: Success message and input text if processed successfully.
        If an exception occurs, an error message will be returned.
    """
    try:
        data = await request.json()
        user_input = data.get("text", "").strip()

        if not user_input:
            return {"success": False, "error": "No input text provided"}

        if MODE == "haos":
            await send_to_haos(user_input)
        elif MODE == "local":
            await send_to_ollama(user_input)
        elif MODE == "cloud":
            await send_to_cloud(user_input)
        else:
            return {"success": False, "error": "Invalid mode"}

        return {"success": True, "message": "Sent successfully", "input": user_input}

    except Exception as e:
        return {"success": False, "error": f"Application error: {str(e)}"}

async def send_to_haos(user_input: str):
    """
    Sends the prompt to the HAOS webhook.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                HAOS_WEBHOOK, json={"text": user_input}, headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return {"success": True, "message": "Sent successfully to HAOS webhook", "input": user_input}
    except httpx.RequestError as e:
        return {"success": False, "error": f"HTTP Request error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}

async def send_to_ollama(user_input: str):
    """
    Sends the prompt to the local Ollama endpoint.
    """
    try:
        # Prepare the data depending on whether we're using /api/chat or /api/generate
        if 'chat' in OLLAMA_URL:
            assistant_responses = []
            output_dir = 'output'

            files = sorted(
                [f for f in os.listdir(output_dir) if f.endswith('.txt')],
                key=lambda x: os.path.getmtime(os.path.join(output_dir, x)),
                reverse=True
            )[:10]

            for file_name in files:
                try:
                    with open(os.path.join(output_dir, file_name), 'r', encoding='utf-8-sig') as file:
                        content = file.read().strip()
                        assistant_responses.append(content)
                except UnicodeDecodeError as e:
                    print(f"Error reading {file_name}: {str(e)}. Skipping this file.")

            # Reverse the chronology of the messages (earliest on top, latest on bottom)
            assistant_responses.reverse()

            data = {
                "model": OLLAMA_MODEL,
                "messages": [{"role": "assistant", "content": response} for response in assistant_responses]
            }
            data["messages"].append({"role": "user", "content": user_input})

        else:
            data = {"model": OLLAMA_MODEL, "prompt": user_input}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 204:
                return {"success": False, "error": "No content returned by Ollama"}

            # Check for correct content type (NDJSON)
            content_type = response.headers.get("Content-Type", "")
            if "application/x-ndjson" not in content_type:
                return {"success": False, "error": f"Expected NDJSON response, but got: {content_type}"}

            # Placeholder array to hold all the text segments
            full_response = []

            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                try:
                    response_data = json.loads(line)

                    # If using /api/chat, look for 'message'['content']
                    if 'message' in response_data and 'content' in response_data['message']:
                        full_response.append(response_data['message']['content'])

                    # If using /api/generate, look for 'response'
                    elif "response" in response_data:
                        full_response.append(response_data["response"])

                    # Response is complete when 'done' parameter is True
                    if response_data.get("done", False):
                        break

                except json.JSONDecodeError as e:
                    return {"success": False, "error": f"Error parsing NDJSON line: {str(e)}"}

            llm_output = "".join(full_response)
            await send_to_piper(llm_output)

            return {"success": True, "message": "Sent successfully to Ollama endpoint", "input": user_input, "response": llm_output}

    except Exception as e:
        return {"success": False, "error": f"Error sending to Ollama: {str(e)}"}

async def send_to_cloud(user_input: str):
    """
    Sends the prompt to the specified cloud-based LLM API endpoint.
    Supports both ChatGPT and Gemini platforms.
    """
    try:
        if CLOUD_PLATFORM not in ["chatgpt", "gemini"]:
            await send_to_piper("Invalid cloud platform selected. Please ensure it is either 'chatgpt' or 'gemini' in settings.yaml")
            return {"success": False, "error": "Invalid cloud platform selected."}

        if not CLOUD_API_KEY or CLOUD_API_KEY.strip() == "":
            await send_to_piper("Cloud API Key is not set. Please ensure CLOUD_API_KEY is defined in .env")

        # For ChatGPT platform
        if CLOUD_PLATFORM == "chatgpt":
            CHATGPT_URL = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CLOUD_API_KEY}"
            }

            data = [
                {"role": "system", "content": "You are a uwu-maxxed chat assistant named Ai-sama."},
                {"role": "user", "content": user_input}
            ]

            payload = {
                "model": CLOUD_MODEL,
                "messages": data,
                "max_tokens": 1000,
                "temperature": 0.7
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(CHATGPT_URL, json=payload, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            if "choices" in response_data:
                cloud_response = response_data["choices"][0]["message"]["content"].strip()
                await send_to_piper(cloud_response)
            else:
                return {"success": False, "error": "Invalid response format from Cloud API"}

        # For Gemini platform
        elif CLOUD_PLATFORM == "gemini":
            GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            system_message = "You are a uwu-maxxed chat assistant named Ai-sama."
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': CLOUD_API_KEY
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": system_message + "\n" + user_input
                            }
                        ]
                    }
                ]
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(GEMINI_URL, json=payload, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            cloud_response = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            if cloud_response:
                await send_to_piper(cloud_response)
            else:
                await send_to_piper("No valid text response found in Gemini output.")

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            await send_to_piper("400 Bad Request. Please check if your API Key is correct in the .env file!")
            return {"success": False, "error": "400 Bad Request. Please check if your API Key is correct in the .env file!"}

        elif e.response.status_code == 404:
            await send_to_piper("404 Not Found. The cloud URL may be invalid, or the cloud server may be currently down!")
            return {"success": False, "error": "404 Not Found Error"}

        elif e.response.status_code == 429:
            rate_limit_remaining = e.response.headers.get("X-RateLimit-Remaining", "Unknown")
            rate_limit_reset = e.response.headers.get("X-RateLimit-Reset", "Unknown")
            await send_to_piper(f"Rate limit exceeded! Remaining: {rate_limit_remaining}, Reset at: {rate_limit_reset}")
            return {
                "success": False,
                "error": f"Too many requests (429). Remaining: {rate_limit_remaining}, resets at: {rate_limit_reset}"
            }

        else:
            await send_to_piper("There is no response from the Cloud API. Please check if your cloud platform/model/API key values are correct!")
            return {"success": False, "error": f"HTTP error occurred: {e.response.status_code}"}

    except httpx.RequestError as e:
        return {"success": False, "error": f"Request error occurred: {str(e)}"}

    except Exception as e:
        return {"success": False, "error": f"An error occurred: {str(e)}"}

async def send_to_piper(llm_output: str):
    """
    Sends the text output to the Piper endpoint.
    """

    try:
        async with AsyncTcpClient(PIPER_HOST, PIPER_PORT) as client:
            synthesize_event = Synthesize(
                text=llm_output,
                voice=SynthesizeVoice(PIPER_MODEL)
            )

            await client.write_event(synthesize_event.event())

            while True:
                event = await client.read_event()
                if event is None:
                    raise RuntimeError("No response from Piper")

                if AudioStop.is_type(event.type):
                    break

            return {"success": True, "message": "Sent successfully to Piper endpoint"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        _LOGGER.error(f"Error sending to Piper: {e}")
        return {"success": False, "error": f"Error sending to Piper: {e}"}

@app.post("/api/send_voice")
async def send_voice(audio: UploadFile = File(...), _: None = Depends(validate_connection)):
    """
    Sends the voice input to the Whisper endpoint.
    """
    try:
        input_bytes = await audio.read()

        # Process the input .wav file
        wav_buffer = io.BytesIO(input_bytes)
        with wave.open(wav_buffer, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
            params = wf.getparams()

        # Send to Faster-Whisper backend
        async with AsyncTcpClient(WHISPER_HOST, WHISPER_PORT) as client:
            await client.write_event(Transcribe(language="en").event())

            chunk_size = 4096
            offset = 0
            while offset < len(frames):
                chunk = AudioChunk(
                    rate=params.framerate,
                    width=params.sampwidth,
                    channels=params.nchannels,
                    audio=frames[offset:offset+chunk_size]
                )
                await client.write_event(chunk.event())
                offset += chunk_size

            await client.write_event(AudioStop().event())

            while True:
                event = await client.read_event()
                if event is None:
                    raise RuntimeError("No response from STT server")

                transcript = Transcript.from_event(event)
                if transcript:
                    text = transcript.text
                    break

        return {"success": True, "transcription": text}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

# Monitor shared notification file to detect if a new TTS output is generated from Piper Docker
async def monitor_notifications():
    """
    Monitors the notification file and sends updates to clients.

    Continuously checks for new TTS output and forwards the data to active WebSocket clients.
    """
    while True:
        if os.path.exists(notification_file):
            try:
                with open(notification_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                audio_path = data.get("audio_file", "").strip()
                text_path = audio_path.replace(".wav", ".txt") if audio_path.endswith(".wav") else ""
                await send_to_clients(json.dumps(data))
                os.remove(notification_file)

                if not SAVE_CHAT_HISTORY:
                    file_id = os.path.splitext(os.path.basename(audio_path))[0] if audio_path else None
                    pending_deletions[file_id] = {
                        "audio": audio_path,
                        "text": text_path,
                        "acknowledged_clients": set()
                    }
            except json.JSONDecodeError:
                logger.error("Error decoding JSON from notification file")
            except Exception as e:
                logger.error(f"Error processing notification file: {e}")

        await asyncio.sleep(1)

# Send output to frontend
async def send_to_clients(message: str):
    """
    Sends message to all connected WebSocket clients.
    Simultaneously updates the list of active WebSocket clients.

    Args:
        message (str): JSON message to be sent.
    """
    disconnected_clients = set()
    
    for client_tuple in connected_clients:
        websocket, ip = client_tuple

        try:
            await websocket.send_text(message)
        except (WebSocketDisconnect, ConnectionResetError):
            disconnected_clients.add(client_tuple)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            disconnected_clients.add(client_tuple)

    connected_clients.difference_update(disconnected_clients)

# Suppress asyncio ConnectionResetError
def suppress_asyncio_error():
    """
    Suppresses known asyncio ConnectionResetError exceptions.
    """
    try:
        # Import only when needed
        import asyncio.proactor_events

        orig = asyncio.proactor_events._ProactorBasePipeTransport._call_connection_lost

        def safe_shutdown(self, exc):
            try:
                sock = getattr(self, "_sock", None)
                if sock and hasattr(sock, "shutdown"):
                    sock.shutdown(socket.SHUT_RDWR)
            except (OSError, ConnectionResetError):
                pass
            return orig(self, exc)

        asyncio.proactor_events._ProactorBasePipeTransport._call_connection_lost = safe_shutdown
    except Exception as e:
        print("Error: Failed to patch asyncio ConnectionResetError due to", e)

if __name__ == "__main__":
    if PROTOCOL == "https":
        logger.info(f"Starting app on {PROTOCOL}://{HOST}:{PORT}")
        uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL.lower(), ssl_keyfile="key.pem", ssl_certfile="cert.pem")
    else:
        logger.info(f"Starting app on {PROTOCOL}://{HOST}:{PORT}")
        uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL.lower())