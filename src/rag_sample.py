from openai import OpenAI
import yaml


def promot_read():
    with open('scripts/prompt_settings.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def get_response(prompt, question):
    client = OpenAI(base_url="http://127.0.0.1:8000/v1",
                    api_key="0")
    response = client.chat.completions.create(
        model="baichuan-chat-7b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    print(promot_read())
