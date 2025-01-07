import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI()

def chat(message, history):
    messages = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]

    for user_message, assistant_message in history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "system", "content": assistant_message})
    messages.append({"role": "user", "content": message})

    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

gr.ChatInterface(fn=chat).launch()