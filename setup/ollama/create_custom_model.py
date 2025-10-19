import os
import subprocess
import re

def check_model_exists(model_name):
    """ Check if the model already exists by listing available models. """
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            models = re.findall(r"^\S+", result.stdout.strip(), re.MULTILINE)
            normalized_models = [model.split(':')[0] for model in models]

            if model_name.lower() in [existing_model.lower() for existing_model in normalized_models]:
                return True

            return False

        else:
            print(f"Error listing models: {result.stderr}")
            return False
    except Exception as e:
        print(f"An error occurred while checking for the model: {str(e)}")
        return False

def install_model(model_name):
    response = input(f"\nNo Ollama models are installed. Would you like to install '{model_name}' (recommended default model for LLaMaDesu!)? (y/n): ").strip().lower()
    if response == 'y':
        try:
            print(f"Installing {model_name}...")
            result = subprocess.run(
                ['ollama', 'pull', model_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"{model_name} installed successfully!")
                return True
            else:
                print(f"Error installing {model_name}: {result.stderr}")
                return False
        except Exception as e:
            print(f"An error occurred while installing the model: {str(e)}")
            return False
    else:
        print(f"Skipping model installation. Proceeding with the rest of the script.")
        return True

def create_custom_model():
    modelfile_path = './Modelfile.txt'

    try:
        with open(modelfile_path, 'r', encoding='utf-8') as file:
            modelfile_content = file.read().strip()
    except FileNotFoundError:
        print(f"Modelfile not found at: {modelfile_path}")
        return
    except Exception as e:
        print(f"Error reading the Modelfile: {str(e)}")
        return

    try:
        model_name = None
        for line in modelfile_content.splitlines():
            if line.startswith("FROM "):
                model_name = line.strip().replace("FROM ", "")
                break

        if not model_name:
            print("Error: Model name not found in the Modelfile.")
            return

        temperature_match = re.search(r"PARAMETER temperature (\d+(\.\d+)?)", modelfile_content)
        temperature = temperature_match.group(1) if temperature_match else "Not defined"

        context_tokens_match = re.search(r"PARAMETER num_ctx (\d+)", modelfile_content)
        context_tokens = context_tokens_match.group(1) if context_tokens_match else "Not defined"

        system_prompt_match = re.search(r"SYSTEM (.+)", modelfile_content)
        system_prompt = system_prompt_match.group(1) if system_prompt_match else "Not defined"

    except Exception as e:
        print(f"Error extracting settings from Modelfile: {str(e)}")
        return

    result = subprocess.run(
        ['ollama', 'list'],
        capture_output=True,
        text=True
    )
    models = re.findall(r"^\S+", result.stdout.strip(), re.MULTILINE)

    if len(models) == 0:
        install_model("llama3.1:8b")

    print("\n--- LLaMaDesu! - Custom Model Creation ---")
    print(f"Original Model: {model_name}")
    print(f"  - Ensure this model is available and pulled using 'ollama pull'\n")

    print(f"Temperature: {temperature}")
    print(f"  - Ranges from 0 to 1. Higher values make the model more creative, lower values make it more focused and consistent.\n")

    print(f"Context Tokens: {context_tokens}")
    print(f"  - The number of tokens the model uses as context. A higher number allows longer input sequences, but uses more memory.\n")

    print(f"System Prompt: {system_prompt}")
    print(f"  - This instructs the model to behave in the specified way.\n")
    print(f"\nIf any settings are incorrect, please modify in ./setup/ollama/Modelfile.txt and re-run setup.exe!")

    response = input("Would you like to proceed with creating a custom model with these settings? (y/n): ").strip().lower()
    if response != 'y':
        print("Creation of custom model aborted. Exiting create_custom_model.py...")
        return

    print("\nNOTE: Model names are case-sensitive! Just hit enter with an empty model name if you wish to skip model creation.")
    while True:
        model_name = input("Please choose a model name: ").strip()

        if model_name == "":
            print("Model creation skipped. Exiting create_custom_model.py...")
            return

        if check_model_exists(model_name):
            print(f"Error: The model '{model_name}' already exists. Please choose a different name.")
        else:
            break

    try:
        print(f"Creating model '{model_name}' using the Modelfile...")
        result = subprocess.run(
            ['ollama', 'create', model_name, '-f', modelfile_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"Model '{model_name}' created successfully!")
        else:
            print(f"Error creating model: {result.stderr}")
            return
    
    except Exception as e:
        print(f"An error occurred while creating the model: {str(e)}")
        return

    input("\nPlease remember to update the OLLAMA_MODEL variable in settings.yaml to use your newly created custom model.")
    print("Exiting create_custom_model.py...")

if __name__ == "__main__":
    create_custom_model()
