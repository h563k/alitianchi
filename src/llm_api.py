import re
from http import HTTPStatus
import dashscope
from openai import OpenAI
from tools.config import ModelConfig
from tools.standard_log import log_to_file

config = ModelConfig()


def llm_qwen(prompt, model_name) -> str:
    dashscope.api_key = config.dashscope_key
    response = dashscope.Generation.call(
        model=model_name,
        prompt=prompt,
        seed=config.seed,
        top_p=0.8,
        result_format='message',
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        repetition_penalty=config.frequency_penalty
    )
    if response.status_code == HTTPStatus.OK:
        return response['output']['choices'][0]['message']['content']
    else:
        return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        )


def openai_response(system_prompt, prompt, model_type, client: OpenAI, stream=False) -> str:
    response = client.chat.completions.create(
        model=model_type,
        seed=42,
        temperature=config.temperature,
        presence_penalty=config.presence_penalty,
        frequency_penalty=config.frequency_penalty,
        max_tokens=config.max_tokens,
        stream=stream,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
    )
    if stream:
        full_response = ""
        for chunk in response:
            delta = chunk.choices[0].delta.content
            full_response += str(delta)
            print(delta, end="", flush=True)  # 打印每个新字符并刷新缓冲区
        return full_response
    else:
        return response.choices[0].message.content


def llm_free(system_prompt, prompt, model_type, stream=False) -> str:
    port, token = getattr(config, model_type)
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    client = OpenAI(base_url=f"http://192.168.28.5:{port}/v1/",
                    api_key="not used actually",
                    default_headers=header
                    )
    return openai_response(system_prompt, prompt, model_type, client, stream)


def llm_huatuo(system_prompt, prompt, model_name, stream=False) -> str:
    client = OpenAI(base_url="http://127.0.0.1:9997/v1",
                    api_key="not used actually")
    return openai_response(system_prompt, prompt, model_name, client, stream)


@log_to_file
def local_openai(system_prompt, prompt, model_name, stream) -> str:
    model_name = model_name if model_name else config.model_name
    if model_name in ['qwen', 'kimi', 'glm']:
        return llm_free(system_prompt, prompt, model_name, stream)
    elif re.findall(r'qwen', model_name):
        return llm_qwen(prompt, model_name)
    elif re.findall(r'huatuo', model_name):
        return llm_huatuo(system_prompt, prompt, model_name, stream)
    else:
        return '请选择合适模型'
