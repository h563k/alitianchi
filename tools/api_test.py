import os
from openai import OpenAI


# 这里是openai调用格式
from openai import OpenAI
port = 8000
llm = OpenAI(
    api_key="0",
    base_url="http://localhost:{}/v1".format(os.environ.get("API_PORT", port)),
)
messages = []
messages.append({"role": "user", "content": "你了解中医吗,请问中医怎么治疗感冒"})
result = llm.chat.completions.create(messages=messages, model="test")
print(result.choices[0].message)
