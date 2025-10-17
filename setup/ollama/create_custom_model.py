import os
import subprocess
import re

def create_custom_model():
    modelfile_path = './Modelfile'

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
        model_name = modelfile_content.splitlines()[0].strip().replace("FROM ", "")

        temperature_match = re.search(r"PARAMETER temperature (\d+(\.\d+)?)", modelfile_content)
        temperature = temperature_match.group(1) if temperature_match else "Not defined"

        context_tokens_match = re.search(r"PARAMETER num_ctx (\d+)", modelfile_content)
        context_tokens = context_tokens_match.group(1) if context_tokens_match else "Not defined"

        system_prompt_match = re.search(r"SYSTEM (.+)", modelfile_content)
        system_prompt = system_prompt_match.group(1) if system_prompt_match else "Not defined"

    except Exception as e:
        print(f"Error extracting settings from Modelfile: {str(e)}")
        return

    print("\n--- LLaMaDesu! - Custom Model Creation ---")
    print(f"Original Model: {model_name}")
    print(f"  - Ensure this model is available and pulled using 'ollama pull'\n")

    print(f"Temperature: {temperature}")
    print(f"  - Ranges from 0 to 1. Higher values make the model more creative, lower values make it more focused and consistent.\n")

    print(f"Context Tokens: {context_tokens}")
    print(f"  - The number of tokens the model uses as context. A higher number allows longer input sequences, but uses more memory.\n")

    print(f"System Prompt: {system_prompt}")
    print(f"  - This instructs the model to behave in the specified way.\n")

    response = input("\nAre these settings correct? (y/n): ").strip().lower()
    if response != 'y':
        print("Please modify the settings by opening the Modelfile as a .txt. Exiting...")
        return

    model_name = input("Please choose a model name: ").strip()

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
    print("Exiting...")

if __name__ == "__main__":
    create_custom_model()