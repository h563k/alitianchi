from openai import OpenAI


def get_response(prompt, question):
    client = OpenAI(base_url="http://127.0.0.1:8000/v1",
                    api_key="0")
    response = client.chat.completions.create(
        model="huatuo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
    )
    return response.choices[0].message.content
