# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM
from src.config import ModelConfig

model_config = ModelConfig()
SAVE_PATH = model_config.save_path
MODEL_PATH = model_config.embedding_path


tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForMaskedLM.from_pretrained(MODEL_PATH)


tokenizer.save_pretrained(f'{SAVE_PATH}/{MODEL_PATH}')
model.save_pretrained(f'{SAVE_PATH}/{MODEL_PATH}')
print('download complete')
