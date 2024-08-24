from http import HTTPStatus
import dashscope
from src.config import ModelConfig


def local_openai(prompt):
    config = ModelConfig()
    dashscope.api_key = config.dashscope_key
    response = dashscope.Generation.call(
        model=config.model_name,
        prompt=prompt,
        seed=42,
        top_p=0.8,
        result_format='message',
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        return response
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
