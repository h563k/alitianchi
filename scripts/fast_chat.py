import subprocess
import threading
from src.config import ModelConfig

config = ModelConfig()
model_full_path = config.model_full_path
print(model_full_path)


def run_controller():
    subprocess.run(
        ["python3", "-m", "fastchat.serve.controller", "--host", "0.0.0.0", "--port", "21001"])


def run_model_llm():
    subprocess.run([
        "python3", "-m", "fastchat.serve.model_worker", "--model-path", f"{model_full_path}",
        "--dtype", "float16"
    ])


def run_api_server():
    subprocess.run([
        "python3", "-m", "fastchat.serve.openai_api_server", "--host", "0.0.0.0", "--port", "8000"
    ])


if __name__ == '__main__':
    controller_thread = threading.Thread(target=run_controller)
    controller_thread.start()
    model_llm = threading.Thread(target=run_model_llm)
    api_server = threading.Thread(target=run_api_server)
    model_llm.start()
    api_server.start()
