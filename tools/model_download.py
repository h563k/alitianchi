from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from src.config import ModelConfig


model_config = ModelConfig()
SAVE_PATH = model_config.save_path
MODEL_PATH = model_config.model_path

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH, use_fast=True, trust_remote_code=True, cache_dir=SAVE_PATH)
tokenizer.save_pretrained(f'{SAVE_PATH}/{MODEL_PATH}')
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, device_map="auto", torch_dtype='auto', trust_remote_code=True, cache_dir=SAVE_PATH)
model.save_pretrained(f'{SAVE_PATH}/{MODEL_PATH}')
model.generation_config = GenerationConfig.from_pretrained(MODEL_PATH)
print('模型下载结束，下面是简单测试')
messages = []
messages.append({"role": "user", "content": "肚子疼怎么办？"})
response = model.HuatuoChat(tokenizer, messages)
print(response)
