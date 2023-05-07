import openai
import os

openai.api_key = os.environ["API_KEY"]
openai.organization = os.environ["ORGANIZATION"]


def send_to_chatgpt(prompt, role="user", model="gpt-3.5-turbo", temperature=0.0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "you can answer only sql"},
            {"role": role, "content": prompt}
        ],
        temperature=temperature,
    )

    return response["choices"][0]["message"]["content"]
