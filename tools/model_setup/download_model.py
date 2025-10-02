"""
Download Qwen3-1.7B-Base model for local testing
"""

import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


def download_model():
    """Download and cache the Qwen3-1.7B-Base model."""

    # Optional: keep cache inside the project instead of the global user cache
    # Comment this out if you prefer the global cache (~/.cache/huggingface/hub)
    os.environ["HF_HOME"] = os.path.join(os.getcwd(), ".hf_cache")

    model_name = "Qwen/Qwen3-1.7B-Base"

    print(f"Downloading {model_name}...")
    print("This may take a few minutes (model is ~3.4GB)")
    print()

    try:
        # Download tokenizer
        print("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("Tokenizer downloaded")

        # Download model
        print("Downloading model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        print("Model downloaded")

        # Test basic functionality
        print("Testing model...")
        test_input = "Hello, how are you?"
        inputs = tokenizer(test_input, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Test response: {response[:100]}...")

        print()
        print("Model download and test completed successfully!")
        print(f"Model size: ~3.4GB")
        print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")

        return True

    except Exception as e:
        print(f"Error downloading model: {e}")
        return False


if __name__ == "__main__":
    print("Qwen3-1.7B-Base Model Download")
    print("=" * 40)

    success = download_model()

    if success:
        print("\nReady to test Gyroscope pipeline!")
    else:
        print("\nDownload failed. Please check your internet connection.")
