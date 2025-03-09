from gpt4all import GPT4All

# Load LLM model
MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
MODEL_PATH = "./"

llm = GPT4All(model_name=MODEL_NAME, model_path=MODEL_PATH, device="cpu", allow_download=False, n_threads=8)

print("Model loaded successfully!")