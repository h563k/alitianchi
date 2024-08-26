import re
from http import HTTPStatus
import dashscope
from tools.config import ModelConfig
from tools.standard_log import log_to_file


def llm_qwen(prompt, model_name) -> str:
    config = ModelConfig()
    dashscope.api_key = config.dashscope_key
    response = dashscope.Generation.call(
        model=model_name,
        prompt=prompt,
        seed=42,
        top_p=0.8,
        result_format='message',
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        return response['output']['choices'][0]['message']['content']
    else:
        return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        )


@log_to_file
def local_openai(prompt, model_name=None) -> str:
    config = ModelConfig()
    model_name = model_name if model_name else config.model_name
    if re.findall(r'qwen', model_name):
        return llm_qwen(prompt, model_name)
    elif re.findall(r'huatuo', model_name):
        return 'huatuo'
